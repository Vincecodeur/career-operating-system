import asyncio
import logging
from contextlib import suppress
from typing import Callable

from sqlalchemy.orm import Session

from app.ai.context_service import AIContextService
from app.ai.models import JobOfferAIExplanation
from app.ai.providers.gemini_provider import GeminiProvider
from app.ai.schemas import AIExplanationContext
from app.ai.services import AIExplanationService
from app.auth.models import User
from app.core.database import SessionLocal
from app.core.settings import settings
from app.jobs.models import JobOffer
from app.matching.service import calculate_matching_result
from app.profile.models import Profile
from app.settings.service import SettingsService


logger = logging.getLogger(__name__)


class AIExplanationScheduler:
    """
    Scheduler léger pour automatiser la génération d'explications IA
    (DEC-089).

    Responsabilités :
    - déclencher un run quotidien à intervalle configurable ;
    - sélectionner les offres/profils candidats selon les critères
      de DEC-089 (pas d'explication existante, quality_level COMPLETE,
      score au-dessus du seuil configuré, consentement AI accordé) ;
    - persister les explications générées avec succès ;
    - ne jamais bloquer sur l'échec d'une seule paire (profil, offre).

    Suit exactement le même squelette que DiscoveryScheduler
    (app/jobs/scheduler.py), pour rester cohérent avec le pattern déjà
    établi dans ce projet.

    La logique métier de génération reste dans AIExplanationService,
    GeminiProvider et le moteur de matching déterministe
    (calculate_matching_result) - ce scheduler ne fait qu'orchestrer.
    """

    def __init__(
        self,
        enabled: bool | None = None,
        interval_minutes: int | None = None,
        session_factory: Callable[[], Session] = SessionLocal,
    ):
        self.enabled = (
            settings.AI_EXPLANATION_SCHEDULER_ENABLED
            if enabled is None
            else enabled
        )

        self.interval_minutes = (
            settings.AI_EXPLANATION_INTERVAL_MINUTES
            if interval_minutes is None
            else interval_minutes
        )

        self.session_factory = session_factory

        self._task: asyncio.Task | None = None
        self._stop_event: asyncio.Event | None = None

    @property
    def interval_seconds(self) -> int:
        return max(
            self.interval_minutes,
            1,
        ) * 60

    def start(self) -> bool:
        """
        Démarre le scheduler si la configuration l'autorise.

        Retourne True si une tâche planifiée a été lancée.
        Retourne False si le scheduler est désactivé ou déjà actif.
        """
        if not self.enabled:
            logger.info(
                "AI explanation scheduler is disabled."
            )
            return False

        if self._task is not None and not self._task.done():
            logger.info(
                "AI explanation scheduler is already running."
            )
            return False

        self._stop_event = asyncio.Event()
        self._task = asyncio.create_task(
            self._run_loop()
        )

        logger.info(
            "AI explanation scheduler started with interval %s "
            "minute(s).",
            self.interval_minutes,
        )

        return True

    async def stop(self) -> None:
        """
        Arrête proprement le scheduler.
        """
        if self._task is None:
            return

        if self._stop_event is not None:
            self._stop_event.set()

        self._task.cancel()

        with suppress(asyncio.CancelledError):
            await self._task

        self._task = None
        self._stop_event = None

        logger.info(
            "AI explanation scheduler stopped."
        )

    def run_once(self) -> dict:
        """
        Exécute un run de génération d'explications IA immédiatement.

        Cette méthode est volontairement synchrone pour rester simple
        et facilement testable avec Pytest, comme
        DiscoveryScheduler.run_once().
        """
        db = self.session_factory()

        generated = 0
        skipped_no_consent = 0
        skipped_below_threshold = 0
        failed = 0

        try:
            user_id = self._resolve_primary_user_id(db)

            if user_id is None:
                return {
                    "generated": 0,
                    "skipped_no_consent": 0,
                    "skipped_below_threshold": 0,
                    "failed": 0,
                }

            minimum_score = self._resolve_minimum_score(
                db,
                user_id,
            )

            active_profiles = db.query(Profile).filter(
                Profile.user_id == user_id,
                Profile.is_active == True,  # noqa: E712
            ).all()

            complete_offers = db.query(JobOffer).filter(
                JobOffer.quality_level == "COMPLETE",
            ).all()

            ai_context_service = AIContextService(
                db,
                user_id,
            )

            explanation_service = self._build_explanation_service()

            for profile in active_profiles:
                context_preview = (
                    ai_context_service.get_ai_context_preview(
                        profile.id
                    )
                )

                if (
                    context_preview is None
                    or not context_preview.ai_call_allowed
                ):
                    skipped_no_consent += 1
                    continue

                for job_offer in complete_offers:
                    existing = db.query(
                        JobOfferAIExplanation
                    ).filter(
                        JobOfferAIExplanation.profile_id
                        == profile.id,
                        JobOfferAIExplanation.job_offer_id
                        == job_offer.id,
                    ).first()

                    if existing is not None:
                        continue

                    matching_result = calculate_matching_result(
                        profile_id=profile.id,
                        job_offer_id=job_offer.id,
                        db=db,
                    )

                    if not matching_result.is_calculable:
                        # Offre redevenue PARTIAL entre-temps, ou tout
                        # autre cas où le score n'est pas fiable :
                        # jamais traitée par l'IA (DEC-089, cohérent
                        # avec is_calculable introduit en 7.1.31).
                        continue

                    if (
                        matching_result.matching_score
                        < minimum_score
                    ):
                        skipped_below_threshold += 1
                        continue

                    try:
                        result = self._generate_and_persist(
                            db=db,
                            profile_id=profile.id,
                            job_offer=job_offer,
                            matching_result=matching_result,
                            explanation_service=explanation_service,
                        )

                        if result:
                            generated += 1
                        else:
                            failed += 1
                    except Exception:
                        logger.exception(
                            "AI explanation generation failed for "
                            "profile_id=%s job_offer_id=%s.",
                            profile.id,
                            job_offer.id,
                        )
                        failed += 1

            return {
                "generated": generated,
                "skipped_no_consent": skipped_no_consent,
                "skipped_below_threshold": skipped_below_threshold,
                "failed": failed,
            }
        finally:
            db.close()

    def _generate_and_persist(
        self,
        db: Session,
        profile_id: int,
        job_offer: JobOffer,
        matching_result,
        explanation_service: AIExplanationService,
    ) -> bool:
        context = AIExplanationContext(
            job_title=job_offer.title,
            score=int(matching_result.matching_score),
            strengths=matching_result.strengths,
            weaknesses=matching_result.weaknesses,
            recommendation=(
                matching_result.opportunity_analysis.recommendation
            ),
            verdict=matching_result.opportunity_analysis.verdict,
            summary=matching_result.opportunity_analysis.summary,
        )

        explanation_result = explanation_service.generate_explanation(
            context
        )

        if not explanation_result.success:
            logger.warning(
                "AI explanation unavailable for profile_id=%s "
                "job_offer_id=%s: %s",
                profile_id,
                job_offer.id,
                explanation_result.error_message,
            )
            return False

        explanation = explanation_result.explanation

        job_offer_ai_explanation = JobOfferAIExplanation(
            profile_id=profile_id,
            job_offer_id=job_offer.id,
            summary=explanation.summary,
            detailed_explanation=explanation.detailed_explanation,
            action_plan=explanation.action_plan,
            provider_name=explanation.provider_name,
            model_name=explanation.model_name,
            prompt_version=explanation.prompt_version,
            generated_at=explanation.generated_at,
        )

        db.add(job_offer_ai_explanation)
        db.commit()

        return True

    @staticmethod
    def _build_explanation_service() -> AIExplanationService:
        provider = GeminiProvider(
            api_key=settings.GEMINI_API_KEY,
            model_name=settings.GEMINI_MODEL_NAME,
            timeout_seconds=settings.GEMINI_TIMEOUT_SECONDS,
        )

        return AIExplanationService(
            provider=provider,
            provider_name=GeminiProvider.provider_name,
            model_name=settings.GEMINI_MODEL_NAME,
        )

    @staticmethod
    def _resolve_minimum_score(
        db: Session,
        user_id: int,
    ) -> int:
        settings_service = SettingsService(db)

        discovery_preferences = (
            settings_service.get_discovery_preferences_settings(
                user_id
            )
        )

        return discovery_preferences[
            "discovery_minimum_matching_score"
        ]

    @staticmethod
    def _resolve_primary_user_id(
        db: Session,
    ) -> int | None:
        # Logique identique à DiscoveryScheduler._resolve_primary_user_id
        # (app/jobs/scheduler.py), dupliquée volontairement ici pour
        # garder AIExplanationScheduler indépendant de DiscoveryScheduler
        # (pas de couplage entre les deux domaines de scheduling).
        if not settings.PRIMARY_USER_EMAIL:
            logger.warning(
                "PRIMARY_USER_EMAIL is not configured: AI explanation "
                "generation will be skipped."
            )
            return None

        user = db.query(User).filter(
            User.email == settings.PRIMARY_USER_EMAIL
        ).first()

        if user is None:
            logger.warning(
                "PRIMARY_USER_EMAIL (%s) does not match any user: AI "
                "explanation generation will be skipped.",
                settings.PRIMARY_USER_EMAIL,
            )
            return None

        return user.id

    async def _run_loop(self) -> None:
        """
        Boucle interne du scheduler.

        Exécute un run immédiatement au démarrage, puis attend
        l'intervalle configuré avant le prochain run.
        """
        if self._stop_event is None:
            self._stop_event = asyncio.Event()

        while not self._stop_event.is_set():
            try:
                result = self.run_once()

                logger.info(
                    "Scheduled AI explanation run completed: %s",
                    result,
                )
            except Exception:
                logger.exception(
                    "Scheduled AI explanation run failed."
                )

            try:
                await asyncio.wait_for(
                    self._stop_event.wait(),
                    timeout=self.interval_seconds,
                )
            except asyncio.TimeoutError:
                continue
