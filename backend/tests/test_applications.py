from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_list_applications():
    response = client.get(
        "/applications"
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list
    )


def test_get_application_not_found():
    response = client.get(
        "/applications/999999"
    )

    assert response.status_code == 404


def test_create_application():
    response = client.post(
        "/applications",
        json={
            "profile_id": 1,
            "job_offer_id": 1,
            "status": "Applied"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["profile_id"] == 1
    assert data["job_offer_id"] == 1
    assert data["status"] == "Applied"


def test_get_application():
    create_response = client.post(
        "/applications",
        json={
            "profile_id": 1,
            "job_offer_id": 1,
            "status": "Interview"
        }
    )

    application_id = create_response.json()["id"]

    response = client.get(
        f"/applications/{application_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == application_id
    assert data["status"] == "Interview"
    

def test_update_application():
    create_response = client.post(
        "/applications",
        json={
            "profile_id": 1,
            "job_offer_id": 1,
            "status": "Applied"
        }
    )

    application_id = create_response.json()["id"]

    response = client.put(
        f"/applications/{application_id}",
        json={
            "status": "Interview",
            "notes": "Entretien RH réalisé",
            "source_type": "REFERRAL"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "Interview"
    assert data["notes"] == "Entretien RH réalisé"
    assert data["source_type"] == "REFERRAL"


def test_transition_application_status():
    create_response = client.post(
        "/applications",
        json={
            "profile_id": 1,
            "job_offer_id": 1,
            "status": "Applied"
        }
    )

    application_id = create_response.json()["id"]

    response = client.post(
        f"/applications/{application_id}/status",
        json={
            "status": "Phone Screen"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "Phone Screen"


def test_invalid_status_transition():
    create_response = client.post(
        "/applications",
        json={
            "profile_id": 1,
            "job_offer_id": 1,
            "status": "Interview"
        }
    )

    application_id = create_response.json()["id"]

    response = client.post(
        f"/applications/{application_id}/status",
        json={
            "status": "Applied"
        }
    )

    assert response.status_code == 400

    assert response.json()["detail"] == (
        "Invalid status transition."
    )


def test_transition_application_not_found():
    response = client.post(
        "/applications/999999/status",
        json={
            "status": "Phone Screen"
        }
    )

    assert response.status_code == 404


def test_get_application_timeline():
    create_response = client.post(
        "/applications",
        json={
            "profile_id": 1,
            "job_offer_id": 1,
            "status": "Interview"
        }
    )

    application_id = create_response.json()["id"]

    transition_response = client.post(
        f"/applications/{application_id}/status",
        json={
            "status": "Offer"
        }
    )

    assert transition_response.status_code == 200

    response = client.get(
        f"/applications/{application_id}/timeline"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) >= 1

    assert data[0]["event_type"] == "STATUS_CHANGED"
    assert data[0]["old_value"] == "Interview"
    assert data[0]["new_value"] == "Offer"


def test_timeline_application_not_found():
    response = client.get(
        "/applications/999999/timeline"
    )

    assert response.status_code == 404