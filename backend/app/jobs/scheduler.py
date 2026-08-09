import asyncio
import logging
from contextlib import suppress
from typing import Callable

from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.settings import settings
from app.jobs.discovery_service import DiscoveryService


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

        self.connector_names = (
            settings.DISCOVERY_CONNECTORS
            if connector_names is None
            else connector_names
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
        Exécute une synchronisation Job Discovery immédiatement.

        Cette méthode est volontairement synchrone pour rester simple
        et facilement testable avec Pytest.
        """
        db = self.session_factory()

        try:
            discovery_service = DiscoveryService(db)

            return discovery_service.import_from_connector_names(
                connector_names=self.connector_names,
                source_type="API",
            )
        finally:
            db.close()

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