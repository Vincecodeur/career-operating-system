import email
import imaplib
import logging
import re
from datetime import datetime
from email.message import Message

from bs4 import BeautifulSoup

from app.jobs.connectors.connector_interface import ConnectorInterface
from app.jobs.raw_offer_schema import RawOffer


logger = logging.getLogger(__name__)


JOB_VIEW_URL_PATTERN = re.compile(r"/jobs/view/(\d+)")


class LinkedInEmailConnector(ConnectorInterface):
    """
    Connecteur LinkedIn pour le pipeline Job Discovery, basé sur la
    lecture des emails de notification ("job alerts" / offres
    similaires) reçus dans une boîte mail IMAP dédiée, plutôt que sur
    un appel API ou du scraping du site LinkedIn.

    Contexte (voir docs/linkedin-email-connector-design.md et
    DEC-084 et suivantes) : LinkedIn ne propose aucune API publique
    permettant de rechercher des offres pour un usage individuel, et
    le scraping direct du site (y compris le simple suivi
    automatisé des liens contenus dans ces emails, au-delà de 2-3
    pages sans connexion) est explicitement interdit par ses
    conditions d'utilisation et activement détecté. Lire des emails
    reçus dans sa propre boîte mail ne constitue pas un accès aux
    serveurs LinkedIn.

    Limite assumée : les emails de notification LinkedIn ne
    contiennent ni description, ni type de contrat, ni salaire.
    Seuls titre, entreprise, ville, mode de travail et URL sont
    disponibles. raw_description est donc généré automatiquement à
    partir de ces champs plutôt que d'être vide (RawOffer l'exige).
    Ceci dégrade structurellement le score de matching de ces offres
    par rapport aux offres provenant de sources avec description
    complète (France Travail, Greenhouse) - point connu et accepté,
    une solution de complément manuel de l'offre après import est
    envisagée séparément.
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
        notification email ("job alert" / "similar jobs" style).

        Each job appears as a "job card": a link to
        linkedin.com/.../jobs/view/{id}/... wrapping the job title,
        followed by a line formatted as "Company · City (WorkMode)".

        Returns an empty list (never raises) if the HTML body is
        missing or has an unexpected structure, so a malformed or
        unrelated email never breaks the discovery pipeline.
        """
        try:
            html_body = self._get_html_body(message)

            if not html_body:
                return []

            soup = BeautifulSoup(html_body, "html.parser")

            return self._parse_job_cards(soup)
        except Exception:
            logger.exception(
                "LinkedInEmailConnector: unexpected error while "
                "parsing email body, skipping this email."
            )
            return []

    def _parse_job_cards(
        self,
        soup: BeautifulSoup,
    ) -> list[RawOffer]:
        offers_by_job_id: dict[str, RawOffer] = {}

        job_links = soup.find_all(
            "a",
            href=JOB_VIEW_URL_PATTERN,
        )

        for link in job_links:
            href = link.get("href", "")

            match = JOB_VIEW_URL_PATTERN.search(href)

            if match is None:
                continue

            job_id = match.group(1)

            title = link.get_text(strip=True)

            if not title:
                # invisible wrapper links around the job card share
                # the same href but carry no text at all
                continue

            if title.lower().endswith("logo"):
                # the company logo link also wraps the job URL and
                # carries visible text (e.g. "Acme Corp logo"), but
                # is not the job title - never let it override an
                # already-found real title for the same job id
                continue

            company, city, work_mode = (
                self._extract_company_and_location(link)
            )

            if company is None and city is None:
                # No "Company · City" line was found near this link.
                # This happens for the header/trigger link some
                # LinkedIn "similar jobs" emails include at the top
                # (pointing to the job the user originally viewed),
                # which carries visible text but is not itself a job
                # card in the list. Real job cards always have this
                # line, so its absence means this is not an offer.
                continue

            if job_id in offers_by_job_id:
                # a second valid-looking link for a job id already
                # recorded (should not normally happen once the logo
                # link is excluded, but keep the first valid match
                # rather than silently overwriting it)
                continue

            description = (
                f"Offre découverte via alerte email LinkedIn. "
                f"Titre : {title}. "
                f"Entreprise : {company or 'inconnue'}. "
                f"Lieu : {city or 'inconnu'}."
            )

            offers_by_job_id[job_id] = RawOffer(
                source_name=self.SOURCE_NAME,
                source_job_id=job_id,
                source_url=href,
                title=title,
                company=company,
                raw_description=description,
                city=city,
                region=None,
                country=None,
                work_mode_raw=work_mode,
                retrieved_at=datetime.utcnow(),
            )

        return list(offers_by_job_id.values())

    @staticmethod
    def _extract_company_and_location(
        link,
    ) -> tuple[str | None, str | None, str | None]:
        """
        Looks for a line formatted as "Company · City (WorkMode)"
        within the smallest enclosing table of the title link.
        """
        parent_table = link.find_parent("table")

        if parent_table is None:
            return None, None, None

        text_lines = [
            line.strip()
            for line in parent_table.get_text("\n").split("\n")
            if line.strip()
        ]

        for line in text_lines:
            if "\u00b7" not in line:
                continue

            return LinkedInEmailConnector._parse_location_line(
                line
            )

        return None, None, None

    @staticmethod
    def _parse_location_line(
        line: str,
    ) -> tuple[str | None, str | None, str | None]:
        parts = line.split("\u00b7")

        if len(parts) < 2:
            return None, None, None

        company = parts[0].strip() or None

        location_part = "\u00b7".join(parts[1:]).strip()

        work_mode = None

        work_mode_match = re.search(
            r"\(([^)]+)\)",
            location_part,
        )

        if work_mode_match:
            work_mode = work_mode_match.group(1).strip()
            location_part = location_part[
                : work_mode_match.start()
            ].strip()

        city = location_part or None

        return company, city, work_mode

    @staticmethod
    def _get_html_body(message: Message) -> str | None:
        if message.is_multipart():
            for part in message.walk():
                if part.get_content_type() == "text/html":
                    return LinkedInEmailConnector._decode_part(
                        part
                    )

            return None

        if message.get_content_type() == "text/html":
            return LinkedInEmailConnector._decode_part(message)

        return None

    @staticmethod
    def _decode_part(part) -> str | None:
        payload = part.get_payload(decode=True)

        if payload is None:
            return None

        charset = part.get_content_charset() or "utf-8"

        try:
            return payload.decode(charset, errors="replace")
        except (LookupError, UnicodeDecodeError):
            return payload.decode("utf-8", errors="replace")

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
