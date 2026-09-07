import email
import imaplib
import logging
from datetime import datetime
from email.message import Message

from app.jobs.connectors.connector_interface import ConnectorInterface
from app.jobs.raw_offer_schema import RawOffer


logger = logging.getLogger(__name__)


class LinkedInEmailConnector(ConnectorInterface):
    """
    Connecteur LinkedIn pour le pipeline Job Discovery, basé sur la
    lecture des emails de notification ("job alerts") reçus dans une
    boîte mail IMAP dédiée, plutôt que sur un appel API ou du scraping
    du site LinkedIn.

    Contexte (voir docs/linkedin-email-connector-design.md et DEC-084
    et suivantes) : LinkedIn ne propose aucune API publique permettant
    de rechercher des offres pour un usage individuel, et le scraping
    direct du site est explicitement interdit par ses conditions
    d'utilisation, avec des précédents de poursuites réelles (LinkedIn
    Corp. v. Nubela/Proxycurl, 2025). Lire des emails reçus dans sa
    propre boîte mail ne constitue pas un accès aux serveurs LinkedIn.

    Cette implémentation gère la mécanique IMAP (connexion, recherche
    des emails non lus, marquage comme lus). L'extraction du contenu
    structuré depuis le HTML de chaque email est volontairement
    isolée dans _extract_offers_from_email(), à compléter une fois
    qu'un exemple réel d'email de notification LinkedIn est
    disponible - le format HTML exact n'est pas encore connu.
    """

    SOURCE_NAME = "LinkedIn"

    DEFAULT_SENDER_FILTER = "jobs-noreply@linkedin.com"

    def __init__(
        self,
        imap_host: str | None = None,
        imap_port: int | None = None,
        email_address: str | None = None,
        app_password: str | None = None,
        folder: str = "INBOX",
        sender_filter: str | None = None,
        timeout: int = 10,
    ):
        self.imap_host = imap_host
        self.imap_port = imap_port or 993
        self.email_address = email_address
        self.app_password = app_password
        self.folder = folder
        self.sender_filter = (
            sender_filter or self.DEFAULT_SENDER_FILTER
        )
        self.timeout = timeout

    def fetch_job_offers(self) -> list[RawOffer]:
        if not self._has_valid_credentials():
            return []

        try:
            connection = imaplib.IMAP4_SSL(
                self.imap_host,
                self.imap_port,
                timeout=self.timeout,
            )
        except (OSError, imaplib.IMAP4.error):
            logger.warning(
                "LinkedInEmailConnector: unable to connect to "
                "IMAP host %s.",
                self.imap_host,
            )
            return []

        try:
            connection.login(
                self.email_address,
                self.app_password,
            )
        except imaplib.IMAP4.error:
            logger.warning(
                "LinkedInEmailConnector: IMAP login failed for %s.",
                self.email_address,
            )
            self._safe_logout(connection)
            return []

        try:
            status, _ = connection.select(self.folder)

            if status != "OK":
                logger.warning(
                    "LinkedInEmailConnector: unable to select "
                    "folder %s.",
                    self.folder,
                )
                return []

            message_ids = self._search_unread_sender_emails(
                connection
            )

            raw_offers: list[RawOffer] = []

            for message_id in message_ids:
                offers_from_email = self._process_single_email(
                    connection,
                    message_id,
                )

                raw_offers.extend(offers_from_email)

            return raw_offers
        except imaplib.IMAP4.error:
            logger.warning(
                "LinkedInEmailConnector: IMAP error while "
                "processing mailbox."
            )
            return []
        finally:
            self._safe_logout(connection)

    def _has_valid_credentials(self) -> bool:
        return bool(
            self.imap_host
            and self.email_address
            and self.app_password
        )

    def _search_unread_sender_emails(
        self,
        connection: imaplib.IMAP4_SSL,
    ) -> list[bytes]:
        status, data = connection.search(
            None,
            "UNSEEN",
            "FROM",
            f'"{self.sender_filter}"',
        )

        if status != "OK" or not data or not data[0]:
            return []

        return data[0].split()

    def _process_single_email(
        self,
        connection: imaplib.IMAP4_SSL,
        message_id: bytes,
    ) -> list[RawOffer]:
        status, data = connection.fetch(
            message_id,
            "(RFC822)",
        )

        if status != "OK" or not data or not data[0]:
            return []

        raw_email_bytes = data[0][1]

        parsed_message = email.message_from_bytes(
            raw_email_bytes
        )

        offers = self._extract_offers_from_email(
            parsed_message
        )

        connection.store(
            message_id,
            "+FLAGS",
            "\\Seen",
        )

        return offers

    def _extract_offers_from_email(
        self,
        message: Message,
    ) -> list[RawOffer]:
        """
        Extracts one or more job offers from a single LinkedIn
        notification email.

        NOT YET IMPLEMENTED: the exact HTML structure of LinkedIn job
        alert emails is not yet known. This method must be completed
        once a real sample email is available (see
        docs/linkedin-email-connector-design.md). Until then, it
        returns an empty list for every email, so the connector
        remains safe to enable without producing incorrect data.

        Once implemented, this method must:
        - retrieve the HTML body from the message
        - parse out each job posting (title, company, city, region,
          country, source_url pointing to the real LinkedIn job
          listing, publication date if available)
        - map each one to a RawOffer, with source_name="LinkedIn",
          retrieved_at=datetime.utcnow()
        """
        logger.info(
            "LinkedInEmailConnector: email extraction not yet "
            "implemented, skipping message."
        )

        return []

    @staticmethod
    def _safe_logout(
        connection: imaplib.IMAP4_SSL,
    ) -> None:
        try:
            connection.close()
        except imaplib.IMAP4.error:
            pass

        try:
            connection.logout()
        except imaplib.IMAP4.error:
            pass
