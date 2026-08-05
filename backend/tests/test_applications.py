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