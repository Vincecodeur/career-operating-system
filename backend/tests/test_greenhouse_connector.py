import httpx

from app.jobs.connectors.connector_interface import ConnectorInterface
from app.jobs.connectors.greenhouse_connector import GreenhouseConnector
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
                "https://example.test/boards/demo/jobs",
            ),
            response=httpx.Response(
                500,
            ),
        )


def test_greenhouse_connector_implements_interface():
    connector = GreenhouseConnector(
        board_token="demo",
        api_url="https://example.test/boards",
    )

    assert isinstance(
        connector,
        ConnectorInterface,
    )


def test_fetch_job_offers_returns_raw_offers(monkeypatch):
    def fake_get(
        url,
        params,
        timeout,
    ):
        assert (
            url
            == "https://example.test/boards/demo/jobs"
        )

        return FakeResponse(
            {
                "jobs": [
                    {
                        "id": 8571054002,
                        "title": "Partner Integration Manager",
                        "company_name": "Example Company",
                        "location": {
                            "name": "Paris",
                        },
                        "absolute_url": "https://example.test/jobs/8571054002",
                        "first_published": "2026-08-09T10:00:00Z",
                        "language": "en",
                        "content": "Partnership role with API integrations.",
                        "metadata": [
                            {
                                "name": "Job Family",
                                "value": "Business Development",
                            }
                        ],
                    }
                ]
            }
        )

    monkeypatch.setattr(
        "httpx.get",
        fake_get,
    )

    connector = GreenhouseConnector(
        board_token="demo",
        api_url="https://example.test/boards",
    )

    offers = connector.fetch_job_offers()

    assert len(offers) == 1

    assert isinstance(
        offers[0],
        RawOffer,
    )


def test_greenhouse_offer_maps_to_raw_offer(monkeypatch):
    def fake_get(
        url,
        params,
        timeout,
    ):
        return FakeResponse(
            {
                "jobs": [
                    {
                        "id": 8571054002,
                        "title": "Partner Integration Manager",
                        "company_name": "Example Company",
                        "location": {
                            "name": "Paris",
                        },
                        "absolute_url": "https://example.test/jobs/8571054002",
                        "first_published": "2026-08-09T10:00:00Z",
                        "language": "en",
                        "content": "Partnership role with API integrations.",
                        "metadata": [
                            {
                                "name": "Job Family",
                                "value": "Business Development",
                            }
                        ],
                    }
                ]
            }
        )

    monkeypatch.setattr(
        "httpx.get",
        fake_get,
    )

    connector = GreenhouseConnector(
        board_token="demo",
        api_url="https://example.test/boards",
    )

    offer = connector.fetch_job_offers()[0]

    assert offer.source_name == "Greenhouse"
    assert offer.source_job_id == "8571054002"
    assert offer.source_url == "https://example.test/jobs/8571054002"
    assert offer.title == "Partner Integration Manager"
    assert offer.company == "Example Company"
    assert offer.raw_description == "Partnership role with API integrations."
    assert offer.city == "Paris"
    assert offer.region is None
    assert offer.country is None
    assert offer.contract_type_raw == "Business Development"
    assert offer.language_raw == "en"


def test_fetch_job_offers_returns_empty_list_on_no_content(monkeypatch):
    def fake_get(
        url,
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

    connector = GreenhouseConnector(
        board_token="demo",
        api_url="https://example.test/boards",
    )

    offers = connector.fetch_job_offers()

    assert offers == []


def test_fetch_job_offers_returns_empty_list_without_board_token():
    connector = GreenhouseConnector(
        board_token="",
        api_url="https://example.test/boards",
    )

    offers = connector.fetch_job_offers()

    assert offers == []


def test_fetch_job_offers_returns_empty_list_without_api_url():
    connector = GreenhouseConnector(
        board_token="demo",
        api_url="",
    )

    offers = connector.fetch_job_offers()

    assert offers == []


def test_fetch_job_offers_returns_empty_list_on_http_error(monkeypatch):
    def fake_get(
        url,
        params,
        timeout,
    ):
        return FailingResponse()

    monkeypatch.setattr(
        "httpx.get",
        fake_get,
    )

    connector = GreenhouseConnector(
        board_token="demo",
        api_url="https://example.test/boards",
    )

    offers = connector.fetch_job_offers()

    assert offers == []


def test_fetch_job_offers_returns_empty_list_on_unexpected_payload(monkeypatch):
    def fake_get(
        url,
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

    connector = GreenhouseConnector(
        board_token="demo",
        api_url="https://example.test/boards",
    )

    offers = connector.fetch_job_offers()

    assert offers == []


def test_fetch_job_offers_ignores_non_dict_jobs(monkeypatch):
    def fake_get(
        url,
        params,
        timeout,
    ):
        return FakeResponse(
            {
                "jobs": [
                    "invalid",
                    {
                        "id": 1,
                        "title": "Valid Job",
                    },
                ]
            }
        )

    monkeypatch.setattr(
        "httpx.get",
        fake_get,
    )

    connector = GreenhouseConnector(
        board_token="demo",
        api_url="https://example.test/boards",
    )

    offers = connector.fetch_job_offers()

    assert len(offers) == 1