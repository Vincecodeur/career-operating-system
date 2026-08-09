import httpx

from app.jobs.connectors.connector_interface import ConnectorInterface
from app.jobs.connectors.linkedin_connector import LinkedInConnector
from app.jobs.raw_offer_schema import RawOffer


class FakeResponse:
    def __init__(
        self,
        json_payload=None,
        status_code=200,
    ):
        self.json_payload = json_payload
        self.status_code = status_code

    def json(self):
        return self.json_payload

    def raise_for_status(self):
        return None


class FailingResponse:
    status_code = 500

    def raise_for_status(self):
        raise httpx.HTTPStatusError(
            "Fake server error",
            request=httpx.Request(
                "GET",
                "https://example.test/jobs",
            ),
            response=httpx.Response(
                500,
            ),
        )


def test_linkedin_connector_implements_interface():
    connector = LinkedInConnector(
        api_url="https://example.test/jobs",
        access_token="fake-token",
    )

    assert isinstance(
        connector,
        ConnectorInterface,
    )


def test_fetch_job_offers_returns_raw_offers(monkeypatch):
    def fake_get(
        url,
        headers,
        params,
        timeout,
    ):
        assert url == "https://example.test/jobs"
        assert headers["Authorization"] == "Bearer fake-token"

        return FakeResponse(
            {
                "jobs": [
                    {
                        "id": "LINKEDIN-001",
                        "title": "Technical Partnerships Manager",
                        "description": "Partnership role with APIs.",
                        "company": {
                            "name": "Example Company",
                        },
                        "location": {
                            "city": "Paris",
                            "region": "Ile-de-France",
                            "country": "France",
                        },
                        "url": "https://example.test/jobs/1",
                        "employment_type": "CDI",
                        "work_mode": "Hybrid",
                        "salary": "70000 - 90000 EUR",
                        "published_at": "2026-08-09",
                        "language": "EN",
                    }
                ]
            }
        )

    monkeypatch.setattr(
        "httpx.get",
        fake_get,
    )

    connector = LinkedInConnector(
        api_url="https://example.test/jobs",
        access_token="fake-token",
    )

    offers = connector.fetch_job_offers()

    assert len(offers) == 1
    assert isinstance(
        offers[0],
        RawOffer,
    )


def test_linkedin_offer_maps_to_raw_offer(monkeypatch):
    def fake_get(
        url,
        headers,
        params,
        timeout,
    ):
        return FakeResponse(
            {
                "jobs": [
                    {
                        "id": "LINKEDIN-001",
                        "title": "Technical Partnerships Manager",
                        "description": "Partnership role with APIs.",
                        "company": {
                            "name": "Example Company",
                        },
                        "location": {
                            "city": "Paris",
                            "region": "Ile-de-France",
                            "country": "France",
                        },
                        "url": "https://example.test/jobs/1",
                        "employment_type": "CDI",
                        "work_mode": "Hybrid",
                        "salary": "70000 - 90000 EUR",
                        "published_at": "2026-08-09",
                        "language": "EN",
                    }
                ]
            }
        )

    monkeypatch.setattr(
        "httpx.get",
        fake_get,
    )

    connector = LinkedInConnector(
        api_url="https://example.test/jobs",
        access_token="fake-token",
    )

    offer = connector.fetch_job_offers()[0]

    assert offer.source_name == "LinkedIn"
    assert offer.source_job_id == "LINKEDIN-001"
    assert offer.source_url == "https://example.test/jobs/1"
    assert offer.title == "Technical Partnerships Manager"
    assert offer.company == "Example Company"
    assert offer.raw_description == "Partnership role with APIs."
    assert offer.city == "Paris"
    assert offer.region == "Ile-de-France"
    assert offer.country == "France"
    assert offer.contract_type_raw == "CDI"
    assert offer.work_mode_raw == "Hybrid"
    assert offer.salary_raw == "70000 - 90000 EUR"
    assert offer.published_at_raw == "2026-08-09"
    assert offer.language_raw == "EN"


def test_fetch_job_offers_returns_empty_list_on_no_content(monkeypatch):
    def fake_get(
        url,
        headers,
        params,
        timeout,
    ):
        return FakeResponse(
            status_code=204,
        )

    monkeypatch.setattr(
        "httpx.get",
        fake_get,
    )

    connector = LinkedInConnector(
        api_url="https://example.test/jobs",
        access_token="fake-token",
    )

    offers = connector.fetch_job_offers()

    assert offers == []


def test_fetch_job_offers_returns_empty_list_without_api_url():
    connector = LinkedInConnector(
        api_url="",
        access_token="fake-token",
    )

    offers = connector.fetch_job_offers()

    assert offers == []


def test_fetch_job_offers_returns_empty_list_on_http_error(monkeypatch):
    def fake_get(
        url,
        headers,
        params,
        timeout,
    ):
        return FailingResponse()

    monkeypatch.setattr(
        "httpx.get",
        fake_get,
    )

    connector = LinkedInConnector(
        api_url="https://example.test/jobs",
        access_token="fake-token",
    )

    offers = connector.fetch_job_offers()

    assert offers == []


def test_fetch_job_offers_returns_empty_list_on_unexpected_payload(monkeypatch):
    def fake_get(
        url,
        headers,
        params,
        timeout,
    ):
        return FakeResponse(
            {
                "unexpected": []
            }
        )

    monkeypatch.setattr(
        "httpx.get",
        fake_get,
    )

    connector = LinkedInConnector(
        api_url="https://example.test/jobs",
        access_token="fake-token",
    )

    offers = connector.fetch_job_offers()

    assert offers == []