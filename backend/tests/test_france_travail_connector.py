from app.jobs.connectors.connector_interface import ConnectorInterface
from app.jobs.connectors.france_travail_connector import FranceTravailConnector
from app.jobs.raw_offer_schema import RawOffer


class FakeResponse:
    def __init__(
        self,
        json_payload=None,
        status_code=200,
    ):
        self.json_payload = json_payload or {}
        self.status_code = status_code

    def json(self):
        return self.json_payload

    def raise_for_status(self):
        return None


def test_france_travail_connector_implements_interface():
    connector = FranceTravailConnector(
        client_id="test-client-id",
        client_secret="test-client-secret",
    )

    assert isinstance(
        connector,
        ConnectorInterface,
    )


def test_fetch_access_token(monkeypatch):
    def fake_post(
        url,
        data,
        timeout,
    ):
        assert data["grant_type"] == "client_credentials"
        assert data["client_id"] == "test-client-id"
        assert data["client_secret"] == "test-client-secret"
        assert data["scope"] == "o2dsoffre api_offresdemploiv2"

        return FakeResponse(
            {
                "access_token": "fake-token",
            }
        )

    monkeypatch.setattr(
        "httpx.post",
        fake_post,
    )

    connector = FranceTravailConnector(
        client_id="test-client-id",
        client_secret="test-client-secret",
    )

    token = connector.fetch_access_token()

    assert token == "fake-token"


def test_fetch_job_offers_returns_raw_offers(monkeypatch):
    def fake_post(
        url,
        data,
        timeout,
    ):
        return FakeResponse(
            {
                "access_token": "fake-token",
            }
        )

    def fake_get(
        url,
        headers,
        params,
        timeout,
    ):
        assert headers["Authorization"] == "Bearer fake-token"
        assert params["range"] == "0-49"

        return FakeResponse(
            {
                "resultats": [
                    {
                        "id": "123ABC",
                        "intitule": "Integration Architect",
                        "description": "Integration role with APIs.",
                        "dateCreation": "2026-08-08T10:00:00Z",
                        "lieuTravail": {
                            "libelle": "75 - PARIS",
                        },
                        "entreprise": {
                            "nom": "Example Company",
                        },
                        "typeContrat": "CDI",
                        "salaire": {
                            "libelle": "Annuel de 70000 Euros",
                        },
                        "origineOffre": {
                            "urlOrigine": "https://example.com/jobs/123ABC",
                        },
                    }
                ]
            }
        )

    monkeypatch.setattr(
        "httpx.post",
        fake_post,
    )
    monkeypatch.setattr(
        "httpx.get",
        fake_get,
    )

    connector = FranceTravailConnector(
        client_id="test-client-id",
        client_secret="test-client-secret",
    )

    offers = connector.fetch_job_offers()

    assert len(offers) == 1
    assert isinstance(
        offers[0],
        RawOffer,
    )


def test_fetch_job_offers_maps_france_travail_offer_to_raw_offer(monkeypatch):
    def fake_post(
        url,
        data,
        timeout,
    ):
        return FakeResponse(
            {
                "access_token": "fake-token",
            }
        )

    def fake_get(
        url,
        headers,
        params,
        timeout,
    ):
        return FakeResponse(
            {
                "resultats": [
                    {
                        "id": "123ABC",
                        "intitule": "Integration Architect",
                        "description": "Integration role with APIs.",
                        "dateCreation": "2026-08-08T10:00:00Z",
                        "lieuTravail": {
                            "libelle": "75 - PARIS",
                        },
                        "entreprise": {
                            "nom": "Example Company",
                        },
                        "typeContrat": "CDI",
                        "salaire": {
                            "libelle": "Annuel de 70000 Euros",
                        },
                        "origineOffre": {
                            "urlOrigine": "https://example.com/jobs/123ABC",
                        },
                    }
                ]
            }
        )

    monkeypatch.setattr(
        "httpx.post",
        fake_post,
    )
    monkeypatch.setattr(
        "httpx.get",
        fake_get,
    )

    connector = FranceTravailConnector(
        client_id="test-client-id",
        client_secret="test-client-secret",
    )

    offer = connector.fetch_job_offers()[0]

    assert offer.source_name == "France Travail"
    assert offer.source_job_id == "123ABC"
    assert offer.source_url == "https://example.com/jobs/123ABC"
    assert offer.title == "Integration Architect"
    assert offer.company == "Example Company"
    assert offer.raw_description == "Integration role with APIs."
    assert offer.city == "75 - PARIS"
    assert offer.country == "France"
    assert offer.contract_type_raw == "CDI"
    assert offer.salary_raw == "Annuel de 70000 Euros"
    assert offer.published_at_raw == "2026-08-08T10:00:00Z"
    assert offer.language_raw == "FR"


def test_fetch_job_offers_returns_empty_list_on_no_content(monkeypatch):
    def fake_post(
        url,
        data,
        timeout,
    ):
        return FakeResponse(
            {
                "access_token": "fake-token",
            }
        )

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
        "httpx.post",
        fake_post,
    )
    monkeypatch.setattr(
        "httpx.get",
        fake_get,
    )

    connector = FranceTravailConnector(
        client_id="test-client-id",
        client_secret="test-client-secret",
    )

    offers = connector.fetch_job_offers()

    assert offers == []