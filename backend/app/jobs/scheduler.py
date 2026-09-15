import asyncio
import logging
from contextlib import suppress
from typing import Callable

from sqlalchemy.orm import Session

from app.auth.models import User
from app.core.database import SessionLocal
from app.core.settings import settings
from app.jobs.discovery_service import DiscoveryService
from app.settings.service import SettingsService


logger = logging.getLogger(__name__)


class DiscoveryScheduler:
    """
    Scheduler léger pour automatiser le Job Discovery.

    Responsabilités :
    - déclencher DiscoveryService à intervalle configurable ;
    - utiliser les connecteurs configurés ;
    - ouvrir et fermer une session de base de données ;
    - ne contenir aucune logique métier de normalisation ou de persistance.

    La logique métier reste dans :
    - DiscoveryService ;
    - NormalizationService ;
    - JobOfferRepository.
    """

    def __init__(
        self,
        enabled: bool | None = None,
        interval_minutes: int | None = None,
        connector_names: list[str] | None = None,
        session_factory: Callable[[], Session] = SessionLocal,
    ):
        self.enabled = (
            settings.DISCOVERY_ENABLED
            if enabled is None
            else enabled
        )

        self.interval_minutes = (
            settings.DISCOVERY_INTERVAL_MINUTES
            if interval_minutes is None
            else interval_minutes
        )

        # None is kept as a sentinel meaning "no explicit override was
        # given at construction time". This allows run_once() to
        # resolve the real connector list dynamically on every call,
        # from UserSettings.discovery_connectors (per-user, editable
        # in the Settings UI) rather than freezing it once at process
        # startup from the DISCOVERY_CONNECTORS environment variable.
        # An explicit override (used by all existing tests and by any
        # future manual/scripted call) always takes priority and
        # bypasses this resolution entirely.
        self.connector_names = connector_names

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
                "Discovery scheduler is disabled."
            )
            return False

        if self._task is not None and not self._task.done():
            logger.info(
                "Discovery scheduler is already running."
            )
            return False

        self._stop_event = asyncio.Event()
        self._task = asyncio.create_task(
            self._run_loop()
        )

        logger.info(
            "Discovery scheduler started with interval %s minute(s).",
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
            "Discovery scheduler stopped."
        )

    def run_once(self) -> dict:
        """
        ExÃƒÂ©cute une synchronisation Job Discovery immÃƒÂ©diatement.

        Cette mÃƒÂ©thode est volontairement synchrone pour rester simple
        et facilement testable avec Pytest.
        """
        db = self.session_factory()

        try:
            user_id = self._resolve_primary_user_id(db)

            connector_names = self._resolve_connector_names(
                db,
                user_id,
            )

            discovery_service = DiscoveryService(db)

            return discovery_service.import_from_connector_names(
                connector_names=connector_names,
                source_type="API",
                user_id=user_id,
            )
        finally:
            db.close()

    def _resolve_connector_names(
        self,
        db: Session,
        user_id: int | None,
    ) -> list[str]:
        """
        Resolves the connector list to use for this run, in priority
        order:
        1. an explicit override passed to the constructor (tests,
           manual/scripted calls) - always wins, never touches the
           database;
        2. UserSettings.discovery_connectors for the resolved primary
           user (per-user preference, editable in the Settings UI,
           DEC-070/DEC-082) - used only if non-empty;
        3. the DISCOVERY_CONNECTORS environment variable - safety net
           only, covers the case where no primary user is configured
           or that user has not saved any connector yet.
        """
        if self.connector_names is not None:
            return self.connector_names

        if user_id is not None:
            settings_service = SettingsService(db)

            job_discovery_settings = (
                settings_service.get_job_discovery_settings(
                    user_id
                )
            )

            configured_connectors = job_discovery_settings[
                "discovery_connectors"
            ]

            if configured_connectors:
                return configured_connectors

        return settings.DISCOVERY_CONNECTORS


    @staticmethod
    def _resolve_primary_user_id(
        db: Session,
    ) -> int | None:
        if not settings.PRIMARY_USER_EMAIL:
            logger.warning(
                "PRIMARY_USER_EMAIL is not configured: connectors "
                "requiring per-user credentials will be skipped."
            )
            return None

        user = db.query(User).filter(
            User.email == settings.PRIMARY_USER_EMAIL
        ).first()

        if user is None:
            logger.warning(
                "PRIMARY_USER_EMAIL (%s) does not match any user: "
                "connectors requiring per-user credentials will be "
                "skipped.",
                settings.PRIMARY_USER_EMAIL,
            )
            return None

        return user.id

    async def _run_loop(self) -> None:
        """
        Boucle interne du scheduler.

        Exécute une synchronisation immédiatement au démarrage,
        puis attend l'intervalle configuré avant la prochaine exécution.
        """
        if self._stop_event is None:
            self._stop_event = asyncio.Event()

        while not self._stop_event.is_set():
            try:
                result = self.run_once()

                logger.info(
                    "Scheduled discovery completed: %s",
                    result,
                )
            except Exception:
                logger.exception(
                    "Scheduled discovery failed."
                )

            try:
                await asyncio.wait_for(
                    self._stop_event.wait(),
                    timeout=self.interval_seconds,
                )
            except asyncio.TimeoutError:
                continue