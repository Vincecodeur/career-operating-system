from email.message import EmailMessage

from app.jobs.connectors.linkedin_email_connector import (
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


def test_extracts_two_offers_from_real_structure_email():
    connector = build_connector()

    raw_email_bytes = build_full_test_email()

    import email as email_module

    parsed_message = email_module.message_from_bytes(
        raw_email_bytes
    )

    offers = connector._extract_offers_from_email(
        parsed_message
    )

    assert len(offers) == 2

    for offer in offers:
        assert isinstance(offer, RawOffer)


def test_first_offer_fields_are_correctly_extracted():
    connector = build_connector()

    raw_email_bytes = build_full_test_email()

    import email as email_module

    parsed_message = email_module.message_from_bytes(
        raw_email_bytes
    )

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

    import email as email_module

    parsed_message = email_module.message_from_bytes(
        raw_email_bytes
    )

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

    import email as email_module

    parsed_message = email_module.message_from_bytes(
        raw_email_bytes
    )

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


def email_message_from_bytes(raw_bytes: bytes):
    import email as email_module

    return email_module.message_from_bytes(raw_bytes)


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
