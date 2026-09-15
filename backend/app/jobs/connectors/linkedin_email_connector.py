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

MAX_PLAUSIBLE_TITLE_LENGTH = 200


class LinkedInEmailConnector(ConnectorInterface):
    """
    Connecteur LinkedIn pour le pipeline Job Discovery, basé sur la
    lecture des emails de notification LinkedIn reçus dans une boîte
    mail IMAP dédiée, plutôt que sur un appel API ou du scraping du
    site LinkedIn.

    Détection par contenu (TEXT), pas par expéditeur (FROM) :
    un email transféré manuellement (par opposition à une vraie
    redirection IMAP, qui préserve l'en-tête From d'origine) remplace
    l'expéditeur d'origine par celui du compte qui transfère. Le
    marqueur LinkedIn original reste cependant cité dans le corps du
    message. Chercher via TEXT (en-têtes + corps) couvre donc les
    deux cas : emails livrés par une vraie redirection (marqueur dans
    From) et emails transférés manuellement (marqueur cité dans le
    corps) - confirmé sur un cas réel le 2026-09-15.

    Limite connue et non résolue à ce stade : seul le template email
    "offres similaires" (expéditeur jobs-noreply@linkedin.com) a été
    analysé et testé. Le template "alerte de recherche enregistrée"
    (expéditeur jobalerts-noreply@linkedin.com) a une structure HTML
    probablement différente, non encore reverse-engineered. Si des
    emails de ce second type ne produisent aucune offre extraite,
    ce n'est pas une erreur silencieuse dissimulée : c'est cette
    limite connue qui s'exprime.
    """

    SOURCE_NAME = "LinkedIn"

    DEFAULT_SENDER_FILTER = "jobs-noreply@linkedin.com"

    DEFAULT_CONTENT_MARKERS = [
        "jobs-noreply@linkedin.com",
        "jobalerts-noreply@linkedin.com",
    ]

    def __init__(
        self,
        imap_host: str | None = None,
        imap_port: int | None = None,
        email_address: str | None = None,
        app_password: str | None = None,
        folder: str = "INBOX",
        sender_filter: str | None = None,
        content_markers: list[str] | None = None,
        only_unread: bool = True,
        timeout: int = 10,
    ):
        self.imap_host = imap_host
        self.imap_port = imap_port or 993
        self.email_address = email_address
        self.app_password = app_password
        self.folder = folder
        self.sender_filter = sender_filter
        self.only_unread = only_unread
        self.timeout = timeout

        if content_markers is not None:
            self.content_markers = content_markers
        elif sender_filter is not None:
            self.content_markers = [sender_filter]
        else:
            self.content_markers = list(
                self.DEFAULT_CONTENT_MARKERS
            )

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

            message_ids = self._search_marker_emails(
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

    def _search_marker_emails(
        self,
        connection: imaplib.IMAP4_SSL,
    ) -> list[bytes]:
        if not self.content_markers:
            return []

        criteria = self._build_text_or_criteria(
            self.content_markers
        )

        search_args = (
            ["UNSEEN", *criteria]
            if self.only_unread
            else criteria
        )

        status, data = connection.search(
            None,
            *search_args,
        )

        if status != "OK" or not data or not data[0]:
            return []

        return data[0].split()

    @staticmethod
    def _build_text_or_criteria(
        markers: list[str],
    ) -> list[str]:
        """
        Builds IMAP SEARCH criteria matching any email whose headers
        or body contain at least one of the given markers, using
        nested OR TEXT clauses (e.g. for 2 markers: OR TEXT "a" TEXT
        "b"; for 3: OR TEXT "a" OR TEXT "b" TEXT "c").
        """
        if len(markers) == 1:
            return ["TEXT", f'"{markers[0]}"']

        criteria: list[str] = []

        for marker in markers[:-1]:
            criteria.append("OR")
            criteria.append("TEXT")
            criteria.append(f'"{marker}"')

        criteria.append("TEXT")
        criteria.append(f'"{markers[-1]}"')

        return criteria

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

            title = self._normalize_whitespace(
                link.get_text(strip=True)
            )

            if not title:
                # invisible wrapper links around the job card share
                # the same href but carry no text at all
                continue

            if title.lower().endswith("logo"):
                # the company logo link also wraps the job URL and
                # carries visible text (e.g. "Acme Corp logo"), but
                # is not the job title
                continue

            if not self._looks_like_a_real_title(title):
                # Confirmed real case (2026-09-15): LinkedIn's
                # "saved search alert" email template (sender
                # jobalerts-noreply@linkedin.com) wraps the entire
                # card - title, company, city, status, button text
                # all concatenated - inside a single <a> link, unlike
                # the "similar jobs" grid template this parser was
                # built for (each field isolated in its own cell).
                # Rather than persist a corrupted, unusably long
                # "title" (which even overflowed a database column
                # limit in production), skip it. This degrades
                # gracefully to 0 offers extracted for that email,
                # consistent with the documented, still-unresolved
                # limitation on this second template - not a new
                # silent failure mode.
                logger.info(
                    "LinkedInEmailConnector: skipping a job link "
                    "whose text does not look like a plausible job "
                    "title (likely a different, not yet supported "
                    "email template)."
                )
                continue

            company, city, work_mode = (
                self._extract_company_and_location(link)
            )

            if company is None and city is None:
                continue

            if job_id in offers_by_job_id:
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
    def _looks_like_a_real_title(title: str) -> bool:
        """
        Plausibility check protecting against templates this parser
        was not built for (see the "saved search alert" case,
        2026-09-15): a real job title is reasonably short and never
        contains the "·" separator used elsewhere to join
        company/city, since that character only appears when a link
        wraps an entire card rather than just its title.

        Generic on purpose: this guards against any future unknown
        template producing similarly concatenated text, not just the
        one specific case already observed.
        """
        if len(title) > MAX_PLAUSIBLE_TITLE_LENGTH:
            return False

        if "\u00b7" in title:
            return False

        return True
    
    @staticmethod
    def _normalize_whitespace(text: str) -> str:
        """
        Collapses any run of whitespace (including literal \\r\\n
        line breaks that can appear inside a single text node when
        the source HTML wraps a title across two physical lines) into
        a single space. get_text(strip=True) only trims the ends of
        the concatenated text, never internal whitespace - confirmed
        real case (2026-09-15): titles like "Responsable\\r\\n SI de
        Gestion" extracted from an actual LinkedIn email.
        """
        return re.sub(r"\s+", " ", text).strip()

    @staticmethod
    def _extract_company_and_location(
        link,
    ) -> tuple[str | None, str | None, str | None]:
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

        company = (
            LinkedInEmailConnector._normalize_whitespace(parts[0])
            or None
        )

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

        city = (
            LinkedInEmailConnector._normalize_whitespace(
                location_part
            )
            or None
        )

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
