from fastapi.testclient import TestClient
from app.jobs.job_offer_metadata_extraction_service import (
    JobOfferMetadataExtractionService,
)
from app.main import app

client = TestClient(app)


def test_get_job_offers():
    response = client.get("/job-offers")

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list
    )
    
def test_complete_job_offer_description_returns_404_for_unknown_offer(
    authenticated_headers,
):
    response = client.patch(
        "/job-offers/999999/complete-description",
        json={"description": "Some real description."},
        headers=authenticated_headers,
    )

    assert response.status_code == 404


def test_complete_job_offer_description_requires_authentication():
    create_response = client.post(
        "/job-offers",
        json={
            "title": "Test Offer For Completion",
            "company_name": "Test Company",
            "location": "Paris",
            "source": "LinkedIn",
            "source_url": "https://example.com/test",
            "description": "placeholder",
        },
    )

    job_offer_id = create_response.json()["id"]

    response = client.patch(
        f"/job-offers/{job_offer_id}/complete-description",
        json={"description": "Some real description."},
    )

    assert response.status_code == 401


def test_complete_job_offer_description_updates_offer(authenticated_headers):
    create_response = client.post(
        "/job-offers",
        json={
            "title": "Test Offer For Completion 2",
            "company_name": "Test Company",
            "location": "Paris",
            "source": "LinkedIn",
            "source_url": "https://example.com/test-2",
            "description": "placeholder",
        },
    )

    job_offer_id = create_response.json()["id"]

    assert create_response.json()["quality_level"] == "PARTIAL"

    response = client.patch(
        f"/job-offers/{job_offer_id}/complete-description",
        json={
            "description": "A propos de l'offre d'emploi: real content."
        },
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["quality_level"] == "COMPLETE"
    assert (
        data["description"]
        == "A propos de l'offre d'emploi: real content."
    )
    
def test_complete_job_offer_description_reports_extraction_success(
    authenticated_headers,
    monkeypatch,
):
    monkeypatch.setattr(
        JobOfferMetadataExtractionService,
        "extract_and_persist",
        staticmethod(
            lambda db, job_offer_id: True
        ),
    )

    create_response = client.post(
        "/job-offers",
        json={
            "title": "Test Offer Metadata Extraction Success",
            "company_name": "Test Company",
            "location": "Paris",
            "source": "LinkedIn",
            "source_url": (
                "https://example.com/metadata-success"
            ),
            "description": "placeholder",
        },
    )

    job_offer_id = create_response.json()["id"]

    response = client.patch(
        f"/job-offers/{job_offer_id}/complete-description",
        json={"description": "A real complete description."},
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["quality_level"] == "COMPLETE"
    assert data["metadata_extraction_status"] == "success"


def test_complete_job_offer_description_does_not_fail_when_extraction_fails(
    authenticated_headers,
    monkeypatch,
):
    def raise_simulated_error(db, job_offer_id):
        raise RuntimeError("Simulated Gemini failure for testing.")

    monkeypatch.setattr(
        JobOfferMetadataExtractionService,
        "extract_and_persist",
        staticmethod(raise_simulated_error),
    )

    create_response = client.post(
        "/job-offers",
        json={
            "title": "Test Offer Metadata Extraction Failure",
            "company_name": "Test Company",
            "location": "Paris",
            "source": "LinkedIn",
            "source_url": (
                "https://example.com/metadata-failure"
            ),
            "description": "placeholder",
        },
    )

    job_offer_id = create_response.json()["id"]

    response = client.patch(
        f"/job-offers/{job_offer_id}/complete-description",
        json={"description": "A real complete description."},
        headers=authenticated_headers,
    )

    # Point crucial validé ici : l'échec de l'extraction (simulé par
    # une exception quelconque, ex. surcharge Gemini 503) ne doit
    # jamais empêcher la sauvegarde de la description elle-même,
    # déjà commitée avant l'appel à extract_and_persist().
    assert response.status_code == 200

    data = response.json()

    assert data["quality_level"] == "COMPLETE"
    assert data["description"] == "A real complete description."
    assert data["metadata_extraction_status"] == "failed"