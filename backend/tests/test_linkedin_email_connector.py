import imaplib
from email.message import EmailMessage

from app.jobs.connectors.connector_interface import ConnectorInterface
from app.jobs.connectors.linkedin_email_connector import (
    LinkedInEmailConnector,
)
from app.jobs.raw_offer_schema import RawOffer


def build_valid_connector() -> LinkedInEmailConnector:
    return LinkedInEmailConnector(
        imap_host="imap.example.test",
        imap_port=993,
        email_address="jobs-alerts@example.test",
        app_password="fake-app-password",
        folder="INBOX",
    )


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
    connector = build_valid_connector()

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

    connector = build_valid_connector()

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

    connector = build_valid_connector()

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

    connector = build_valid_connector()

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

    connector = build_valid_connector()

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

    connector = build_valid_connector()

    offers = connector.fetch_job_offers()

    assert offers == []


def test_fetch_job_offers_returns_raw_offer_type_when_extraction_implemented(
    monkeypatch,
):
    """
    Extraction currently always returns an empty list (not yet
    implemented, see linkedin_email_connector.py). This test locks in
    the expected return type contract: whenever extraction produces
    results in the future, they must be RawOffer instances, exactly
    like every other connector in the registry.
    """
    fake_connection = FakeIMAPConnection(
        message_ids=[b"1"],
    )

    monkeypatch.setattr(
        imaplib,
        "IMAP4_SSL",
        lambda host, port, timeout: fake_connection,
    )

    connector = build_valid_connector()

    offers = connector.fetch_job_offers()

    assert isinstance(offers, list)

    for offer in offers:
        assert isinstance(offer, RawOffer)
