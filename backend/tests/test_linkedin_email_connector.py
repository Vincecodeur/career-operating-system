import imaplib
from email.message import EmailMessage

from app.jobs.connectors.connector_interface import ConnectorInterface
from app.jobs.connectors.linkedin_email_connector import (
    MAX_PLAUSIBLE_TITLE_LENGTH,
    LinkedInEmailConnector,
)
from app.jobs.raw_offer_schema import RawOffer


def build_connector() -> LinkedInEmailConnector:
    return LinkedInEmailConnector(
        imap_host="imap.example.test",
        imap_port=993,
        email_address="jobs-alerts@example.test",
        app_password="fake-app-password",
        folder="INBOX",
    )


# ---------------------------------------------------------------
# Mechanics tests: IMAP connection, login, folder selection, marking
# emails as read. All use a fake imaplib.IMAP4_SSL replacement, no
# real network connection. These tests were accidentally dropped
# from this file at some point between 7.1.30.4 and 7.1.30.5 (the
# HTML extraction tests overwrote this file's content instead of
# being added to it) - restored here, 2026-09-15, alongside a
# collect-only verification to confirm no further silent loss.
# ---------------------------------------------------------------


def build_raw_email_message(sender: str = "jobs-noreply@linkedin.com") -> bytes:
    message = EmailMessage()
    message["From"] = sender
    message["Subject"] = "New jobs for you"
    message.set_content("Fake LinkedIn job alert email body.")

    return message.as_bytes()


class FakeIMAPConnection:
    """
    Minimal fake replacing imaplib.IMAP4_SSL for tests, avoiding any
    real network connection.
    """

    def __init__(
        self,
        message_ids: list[bytes] | None = None,
        raw_email: bytes | None = None,
        select_status: str = "OK",
        search_status: str = "OK",
        fetch_status: str = "OK",
        login_should_fail: bool = False,
    ):
        self.message_ids = message_ids or []
        self.raw_email = raw_email or build_raw_email_message()
        self.select_status = select_status
        self.search_status = search_status
        self.fetch_status = fetch_status
        self.login_should_fail = login_should_fail

        self.logged_in = False
        self.selected_folder = None
        self.stored_flags: list[tuple] = []
        self.closed = False
        self.logged_out = False

    def login(self, email_address, app_password):
        if self.login_should_fail:
            raise imaplib.IMAP4.error("Login failed")

        self.logged_in = True

    def select(self, folder):
        self.selected_folder = folder
        return (self.select_status, [b""])

    def search(self, charset, *criteria):
        if self.search_status != "OK":
            return (self.search_status, [b""])

        joined_ids = b" ".join(self.message_ids)
        return (self.search_status, [joined_ids])

    def fetch(self, message_id, parts):
        if self.fetch_status != "OK":
            return (self.fetch_status, [None])

        return (
            self.fetch_status,
            [(message_id, self.raw_email)],
        )

    def store(self, message_id, flag_action, flags):
        self.stored_flags.append(
            (message_id, flag_action, flags)
        )

    def close(self):
        self.closed = True

    def logout(self):
        self.logged_out = True


def test_linkedin_email_connector_implements_interface():
    connector = build_connector()

    assert isinstance(
        connector,
        ConnectorInterface,
    )


def test_fetch_job_offers_returns_empty_list_without_imap_host():
    connector = LinkedInEmailConnector(
        imap_host="",
        email_address="jobs-alerts@example.test",
        app_password="fake-app-password",
    )

    offers = connector.fetch_job_offers()

    assert offers == []


def test_fetch_job_offers_returns_empty_list_without_email_address():
    connector = LinkedInEmailConnector(
        imap_host="imap.example.test",
        email_address="",
        app_password="fake-app-password",
    )

    offers = connector.fetch_job_offers()

    assert offers == []


def test_fetch_job_offers_returns_empty_list_without_app_password():
    connector = LinkedInEmailConnector(
        imap_host="imap.example.test",
        email_address="jobs-alerts@example.test",
        app_password="",
    )

    offers = connector.fetch_job_offers()

    assert offers == []


def test_fetch_job_offers_returns_empty_list_on_login_failure(monkeypatch):
    fake_connection = FakeIMAPConnection(
        login_should_fail=True,
    )

    monkeypatch.setattr(
        imaplib,
        "IMAP4_SSL",
        lambda host, port, timeout: fake_connection,
    )

    connector = build_connector()

    offers = connector.fetch_job_offers()

    assert offers == []
    assert fake_connection.logged_out is True


def test_fetch_job_offers_returns_empty_list_on_connection_error(monkeypatch):
    def raise_connection_error(host, port, timeout):
        raise OSError("Connection refused")

    monkeypatch.setattr(
        imaplib,
        "IMAP4_SSL",
        raise_connection_error,
    )

    connector = build_connector()

    offers = connector.fetch_job_offers()

    assert offers == []


def test_fetch_job_offers_returns_empty_list_when_no_unread_emails(
    monkeypatch,
):
    fake_connection = FakeIMAPConnection(
        message_ids=[],
    )

    monkeypatch.setattr(
        imaplib,
        "IMAP4_SSL",
        lambda host, port, timeout: fake_connection,
    )

    connector = build_connector()

    offers = connector.fetch_job_offers()

    assert offers == []


def test_fetch_job_offers_marks_processed_emails_as_read(monkeypatch):
    fake_connection = FakeIMAPConnection(
        message_ids=[b"1", b"2"],
    )

    monkeypatch.setattr(
        imaplib,
        "IMAP4_SSL",
        lambda host, port, timeout: fake_connection,
    )

    connector = build_connector()

    connector.fetch_job_offers()

    assert len(fake_connection.stored_flags) == 2

    for message_id, flag_action, flags in fake_connection.stored_flags:
        assert flag_action == "+FLAGS"
        assert flags == "\\Seen"


def test_fetch_job_offers_returns_empty_list_on_select_failure(monkeypatch):
    fake_connection = FakeIMAPConnection(
        select_status="NO",
    )

    monkeypatch.setattr(
        imaplib,
        "IMAP4_SSL",
        lambda host, port, timeout: fake_connection,
    )

    connector = build_connector()

    offers = connector.fetch_job_offers()

    assert offers == []


def test_fetch_job_offers_returns_raw_offer_type_when_extraction_implemented(
    monkeypatch,
):
    fake_connection = FakeIMAPConnection(
        message_ids=[b"1"],
    )

    monkeypatch.setattr(
        imaplib,
        "IMAP4_SSL",
        lambda host, port, timeout: fake_connection,
    )

    connector = build_connector()

    offers = connector.fetch_job_offers()

    assert isinstance(offers, list)

    for offer in offers:
        assert isinstance(offer, RawOffer)


# ---------------------------------------------------------------
# HTML extraction tests, based on a real sample email received
# 2026-08-29 (anonymized).
# ---------------------------------------------------------------


def build_real_structure_email_html(job_cards_html: str) -> str:
    """
    Reconstructs the real, structurally faithful skeleton of a
    LinkedIn "similar jobs" notification email (nested tables, one
    logo link + one invisible wrapper link + one titled link per job
    card, company/city line joined by a middle dot), based on a real
    sample email received 2026-08-29. Tracking parameters, sender
    email and recipient name are anonymized/fictional.
    """
    return f"""
    <html>
    <body>
    <table>
    <tr>
    <td>
    <a href="https://www.linkedin.com/comm/jobs/view/9999999999?refId=FAKE&trk=eml-fake">
    Offres d'emploi similaires à Test Job chez fake.company
    </a>
    </td>
    </tr>
    </table>
    <table>
    <tr>
    <td>
    {job_cards_html}
    </td>
    </tr>
    </table>
    <table>
    <tr>
    <td>Cet e-mail est destiné à Test User (Fake Title)</td>
    </tr>
    </table>
    </body>
    </html>
    """


def build_job_card_html(
    job_id: str,
    title: str,
    company: str,
    location: str,
) -> str:
    url = (
        f"https://www.linkedin.com/comm/jobs/view/{job_id}/"
        f"?trackingId=FAKE%3D%3D&refId=FAKE%3D%3D"
    )

    return f"""
    <table>
    <tr>
    <td>
        <a href="{url}">{company} logo</a>
    </td>
    <td>
        <a href="{url}"></a>
        <table>
        <tr>
        <td>
            <a href="{url}"> {title} </a>
        </td>
        </tr>
        <tr>
        <td>
            {company} \u00b7 {location}
        </td>
        </tr>
        </table>
    </td>
    </tr>
    </table>
    """


def build_full_test_email() -> bytes:
    card_1 = build_job_card_html(
        job_id="4460820198",
        title="Senior Digital / E-Retail Manager",
        company="The Talent of Tomorrow",
        location="Ville de Paris (Hybride)",
    )

    card_2 = build_job_card_html(
        job_id="4417327246",
        title="Delivery Manager",
        company="Lazer Technologies",
        location="France (\u00c0 distance)",
    )

    html_body = build_real_structure_email_html(card_1 + card_2)

    message = EmailMessage()
    message["From"] = "jobs-noreply@linkedin.com"
    message["Subject"] = (
        "Nouvelles offres d'emploi similaires \u00e0 Test Job "
        "chez fake.company"
    )
    message.set_content(
        "Fallback plain text body.",
    )
    message.add_alternative(
        html_body,
        subtype="html",
    )

    return message.as_bytes()


def email_message_from_bytes(raw_bytes: bytes):
    import email as email_module

    return email_module.message_from_bytes(raw_bytes)


def test_extracts_two_offers_from_real_structure_email():
    connector = build_connector()

    raw_email_bytes = build_full_test_email()

    parsed_message = email_message_from_bytes(raw_email_bytes)

    offers = connector._extract_offers_from_email(
        parsed_message
    )

    assert len(offers) == 2

    for offer in offers:
        assert isinstance(offer, RawOffer)


def test_first_offer_fields_are_correctly_extracted():
    connector = build_connector()

    raw_email_bytes = build_full_test_email()

    parsed_message = email_message_from_bytes(raw_email_bytes)

    offers = connector._extract_offers_from_email(
        parsed_message
    )

    first_offer = offers[0]

    assert first_offer.source_name == "LinkedIn"
    assert first_offer.source_job_id == "4460820198"
    assert (
        "linkedin.com/comm/jobs/view/4460820198"
        in first_offer.source_url
    )
    assert first_offer.title == "Senior Digital / E-Retail Manager"
    assert first_offer.company == "The Talent of Tomorrow"
    assert first_offer.city == "Ville de Paris"
    assert first_offer.work_mode_raw == "Hybride"
    assert "Senior Digital / E-Retail Manager" in (
        first_offer.raw_description
    )
    assert "The Talent of Tomorrow" in first_offer.raw_description


def test_second_offer_handles_remote_work_mode_with_accent():
    connector = build_connector()

    raw_email_bytes = build_full_test_email()

    parsed_message = email_message_from_bytes(raw_email_bytes)

    offers = connector._extract_offers_from_email(
        parsed_message
    )

    second_offer = offers[1]

    assert second_offer.source_job_id == "4417327246"
    assert second_offer.title == "Delivery Manager"
    assert second_offer.company == "Lazer Technologies"
    assert second_offer.city == "France"
    assert second_offer.work_mode_raw == "\u00c0 distance"


def test_deduplicates_multiple_links_to_same_job_id():
    """
    Each real job card contains 3 links to the same job id (logo,
    invisible wrapper, titled link) - only the titled one carries
    text and must produce exactly one RawOffer, not three.
    """
    connector = build_connector()

    raw_email_bytes = build_full_test_email()

    parsed_message = email_message_from_bytes(raw_email_bytes)

    offers = connector._extract_offers_from_email(
        parsed_message
    )

    job_ids = [offer.source_job_id for offer in offers]

    assert len(job_ids) == len(set(job_ids))


def test_returns_empty_list_for_email_without_html_body():
    connector = build_connector()

    message = EmailMessage()
    message["From"] = "jobs-noreply@linkedin.com"
    message.set_content("Plain text only, no HTML alternative.")

    offers = connector._extract_offers_from_email(message)

    assert offers == []


def test_returns_empty_list_for_html_without_job_links():
    connector = build_connector()

    message = EmailMessage()
    message["From"] = "jobs-noreply@linkedin.com"
    message.set_content("Fallback text.")
    message.add_alternative(
        "<html><body><p>No job links here.</p></body></html>",
        subtype="html",
    )

    offers = connector._extract_offers_from_email(
        email_message_from_bytes(message.as_bytes())
    )

    assert offers == []


def test_returns_empty_list_on_malformed_html():
    connector = build_connector()

    message = EmailMessage()
    message["From"] = "jobs-noreply@linkedin.com"
    message.set_content("Fallback text.")
    message.add_alternative(
        "<html><body><table><tr><td>unclosed",
        subtype="html",
    )

    offers = connector._extract_offers_from_email(
        email_message_from_bytes(message.as_bytes())
    )

    assert isinstance(offers, list)


# ---------------------------------------------------------------
# Marker-based detection tests (2026-09-15): the connector now
# searches by TEXT marker (headers + body) instead of FROM only,
# to also catch manually forwarded emails whose From header no
# longer matches the original LinkedIn sender.
# ---------------------------------------------------------------


def test_default_content_markers_include_both_known_senders():
    connector = build_connector()

    assert connector.content_markers == [
        "jobs-noreply@linkedin.com",
        "jobalerts-noreply@linkedin.com",
    ]


def test_sender_filter_override_still_supported_as_single_marker():
    connector = LinkedInEmailConnector(
        imap_host="imap.example.test",
        email_address="jobs-alerts@example.test",
        app_password="fake-app-password",
        sender_filter="custom-sender@example.com",
    )

    assert connector.content_markers == [
        "custom-sender@example.com",
    ]


def test_content_markers_override_takes_priority_over_sender_filter():
    connector = LinkedInEmailConnector(
        imap_host="imap.example.test",
        email_address="jobs-alerts@example.test",
        app_password="fake-app-password",
        sender_filter="ignored@example.com",
        content_markers=["marker-a@example.com", "marker-b@example.com"],
    )

    assert connector.content_markers == [
        "marker-a@example.com",
        "marker-b@example.com",
    ]


def test_build_text_or_criteria_with_single_marker():
    criteria = LinkedInEmailConnector._build_text_or_criteria(
        ["only-marker@example.com"]
    )

    assert criteria == ["TEXT", '"only-marker@example.com"']


def test_build_text_or_criteria_with_two_markers():
    criteria = LinkedInEmailConnector._build_text_or_criteria(
        ["marker-a@example.com", "marker-b@example.com"]
    )

    assert criteria == [
        "OR",
        "TEXT",
        '"marker-a@example.com"',
        "TEXT",
        '"marker-b@example.com"',
    ]


def test_build_text_or_criteria_with_three_markers():
    criteria = LinkedInEmailConnector._build_text_or_criteria(
        ["a@example.com", "b@example.com", "c@example.com"]
    )

    assert criteria == [
        "OR",
        "TEXT",
        '"a@example.com"',
        "OR",
        "TEXT",
        '"b@example.com"',
        "TEXT",
        '"c@example.com"',
    ]


def test_fetch_job_offers_finds_manually_forwarded_email(monkeypatch):
    """
    Regression test for the real case encountered 2026-09-15: an
    email manually forwarded from Outlook to Gmail has its original
    From header replaced by the forwarding account's own address
    (e.g. "vincent gueret <vincecodeur@gmail.com>"), not
    "jobs-noreply@linkedin.com". The connector must still find it,
    since the marker is quoted in the forwarded body and TEXT search
    covers headers and body alike.
    """
    forwarded_email = EmailMessage()
    forwarded_email["From"] = "vincent gueret <vincecodeur@gmail.com>"
    forwarded_email["Subject"] = "TR : Deel recrute au poste de X"
    forwarded_email.set_content(
        "Fallback text mentioning jobs-noreply@linkedin.com "
        "as quoted header."
    )

    fake_connection = FakeIMAPConnection(
        message_ids=[b"1"],
        raw_email=forwarded_email.as_bytes(),
    )

    monkeypatch.setattr(
        imaplib,
        "IMAP4_SSL",
        lambda host, port, timeout: fake_connection,
    )

    connector = build_connector()

    offers = connector.fetch_job_offers()

    assert isinstance(offers, list)
    assert len(fake_connection.stored_flags) == 1


def test_only_unread_false_omits_unseen_from_search_criteria():
    connector = LinkedInEmailConnector(
        imap_host="imap.example.test",
        email_address="jobs-alerts@example.test",
        app_password="fake-app-password",
        only_unread=False,
    )

    captured_args = {}

    class RecordingConnection:
        def search(self, charset, *criteria):
            captured_args["criteria"] = criteria
            return ("OK", [b""])

    connector._search_marker_emails(RecordingConnection())

    assert "UNSEEN" not in captured_args["criteria"]


def test_only_unread_true_includes_unseen_in_search_criteria():
    connector = LinkedInEmailConnector(
        imap_host="imap.example.test",
        email_address="jobs-alerts@example.test",
        app_password="fake-app-password",
        only_unread=True,
    )

    captured_args = {}

    class RecordingConnection:
        def search(self, charset, *criteria):
            captured_args["criteria"] = criteria
            return ("OK", [b""])

    connector._search_marker_emails(RecordingConnection())

    assert "UNSEEN" in captured_args["criteria"]


def test_looks_like_a_real_title_accepts_normal_title():
    assert LinkedInEmailConnector._looks_like_a_real_title(
        "Senior Digital / E-Retail Manager"
    ) is True


def test_looks_like_a_real_title_rejects_title_over_max_length():
    long_title = "A" * (MAX_PLAUSIBLE_TITLE_LENGTH + 1)

    assert LinkedInEmailConnector._looks_like_a_real_title(
        long_title
    ) is False


def test_looks_like_a_real_title_accepts_title_at_max_length():
    title_at_limit = "A" * MAX_PLAUSIBLE_TITLE_LENGTH

    assert LinkedInEmailConnector._looks_like_a_real_title(
        title_at_limit
    ) is True


def test_looks_like_a_real_title_rejects_title_containing_separator():
    assert LinkedInEmailConnector._looks_like_a_real_title(
        "Sr Agent Architect (France)Parloa \u00b7 Paris, "
        "\u00celе-de-France, France"
    ) is False


def test_parse_job_cards_skips_saved_search_alert_style_concatenated_card():
    """
    Regression test for the real case encountered 2026-09-15: the
    "saved search alert" email template (jobalerts-noreply@linkedin.com)
    wraps title + company + city + status inside a single <a> link,
    unlike the "similar jobs" grid template. The card must be skipped
    entirely (0 offers), not produce a corrupted RawOffer, since the
    concatenated text exceeded a database column limit in production.
    """
    connector = build_connector()

    concatenated_card_html = """
    <html>
    <body>
    <table>
    <tr>
    <td>
    <a href="https://www.linkedin.com/comm/jobs/view/4443983281?alertAction=markasviewed&savedSearchId=1234">
    Sr Agent Architect (France)Parloa \u00b7 Paris, \u00cele-de-France,
    France Recrutement actif Candidature simplifi\u00e9e
    </a>
    </td>
    </tr>
    </table>
    </body>
    </html>
    """

    message = EmailMessage()
    message["From"] = "jobalerts-noreply@linkedin.com"
    message.set_content("Fallback text.")
    message.add_alternative(
        concatenated_card_html,
        subtype="html",
    )

    offers = connector._extract_offers_from_email(
        email_message_from_bytes(message.as_bytes())
    )

    assert offers == []


def test_normalizes_internal_line_breaks_in_title():
    """
    Regression test for a real case encountered 2026-09-15: LinkedIn
    wraps some titles across two physical lines in the source HTML,
    producing a literal "\\r\\n" inside the extracted text since
    get_text(strip=True) only trims the ends, not internal
    whitespace.
    """
    connector = build_connector()

    card_html = build_job_card_html(
        job_id="1111111111",
        title="Responsable\r\n SI de Gestion (S.I.G) - H/F",
        company="SEVETYS",
        location="Ville de Paris (Hybride)",
    )

    html_body = build_real_structure_email_html(card_html)

    message = EmailMessage()
    message["From"] = "jobs-noreply@linkedin.com"
    message.set_content("Fallback text.")
    message.add_alternative(html_body, subtype="html")

    offers = connector._extract_offers_from_email(
        email_message_from_bytes(message.as_bytes())
    )

    assert len(offers) == 1
    assert offers[0].title == "Responsable SI de Gestion (S.I.G) - H/F"