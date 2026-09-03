from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def create_profile(authenticated_headers):
    unique_profile_name = f"Profile_{uuid4()}"

    response = client.post(
        "/profiles",
        json={
            "profile_name": unique_profile_name,
            "full_name": "Test User",
            "current_title": "Backend Developer",
            "location": "Paris",
            "years_of_experience": 5,
            "target_role_short_term": "Senior Backend Developer",
            "target_role_long_term": "Technical Lead",
            "remote_preference": "Hybrid",
            "preferred_countries": "France",
        },
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    return response.json()


def create_certification(name_prefix: str):
    unique_certification_name = f"{name_prefix}_{uuid4()}"

    response = client.post(
        "/certifications",
        json={
            "name": unique_certification_name,
            "issuing_organization": "Test Organization",
        },
    )

    assert response.status_code == 200

    return response.json()


def create_profile_certification(
    profile_id: int,
    certification_id: int,
    authenticated_headers,
    obtained_date: str | None = "2024-01-01",
    expiration_date: str | None = "2026-01-01",
    credential_id: str | None = "TEST-CREDENTIAL",
):
    response = client.post(
        "/profile-certifications",
        json={
            "profile_id": profile_id,
            "certification_id": certification_id,
            "obtained_date": obtained_date,
            "expiration_date": expiration_date,
            "credential_id": credential_id,
        },
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    return response.json()


def test_create_profile_certification(authenticated_headers):
    profile = create_profile(authenticated_headers)
    certification = create_certification("Azure")

    response = client.post(
        "/profile-certifications",
        json={
            "profile_id": profile["id"],
            "certification_id": certification["id"],
            "obtained_date": "2024-01-01",
            "expiration_date": "2026-01-01",
            "credential_id": "AZ-TEST-001",
        },
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["profile_id"] == profile["id"]
    assert data["certification_id"] == certification["id"]
    assert data["obtained_date"] == "2024-01-01"
    assert data["expiration_date"] == "2026-01-01"
    assert data["credential_id"] == "AZ-TEST-001"


def test_duplicate_profile_certification(authenticated_headers):
    profile = create_profile(authenticated_headers)
    certification = create_certification("AWS")

    create_profile_certification(
        profile["id"],
        certification["id"],
        authenticated_headers,
    )

    response = client.post(
        "/profile-certifications",
        json={
            "profile_id": profile["id"],
            "certification_id": certification["id"],
            "obtained_date": "2024-01-01",
            "expiration_date": "2026-01-01",
            "credential_id": "AWS-TEST-001",
        },
        headers=authenticated_headers,
    )

    assert response.status_code == 409


def test_list_profile_certifications(authenticated_headers):
    response = client.get(
        "/profile-certifications",
        headers=authenticated_headers,
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_list_certifications_for_profile(authenticated_headers):
    profile = create_profile(authenticated_headers)
    certification = create_certification("GoogleCloud")

    create_profile_certification(
        profile["id"],
        certification["id"],
        authenticated_headers,
    )

    response = client.get(
        f"/profiles/{profile['id']}/certifications",
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert any(
        profile_certification["certification_id"] == certification["id"]
        for profile_certification in data
    )


def test_update_profile_certification(authenticated_headers):
    profile = create_profile(authenticated_headers)
    certification = create_certification("Kubernetes")

    create_profile_certification(
        profile["id"],
        certification["id"],
        authenticated_headers,
        "2023-01-01",
        "2025-01-01",
        "OLD-CREDENTIAL",
    )

    response = client.put(
        f"/profile-certifications/{profile['id']}/{certification['id']}",
        json={
            "obtained_date": "2024-02-01",
            "expiration_date": "2027-02-01",
            "credential_id": "NEW-CREDENTIAL",
        },
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["profile_id"] == profile["id"]
    assert data["certification_id"] == certification["id"]
    assert data["obtained_date"] == "2024-02-01"
    assert data["expiration_date"] == "2027-02-01"
    assert data["credential_id"] == "NEW-CREDENTIAL"


def test_update_profile_certification_not_found(authenticated_headers):
    response = client.put(
        "/profile-certifications/99999/99999",
        json={
            "obtained_date": "2024-02-01",
            "expiration_date": "2027-02-01",
            "credential_id": "MISSING-CREDENTIAL",
        },
        headers=authenticated_headers,
    )

    assert response.status_code == 404


def test_delete_profile_certification(authenticated_headers):
    profile = create_profile(authenticated_headers)
    certification = create_certification("Security")

    create_profile_certification(
        profile["id"],
        certification["id"],
        authenticated_headers,
    )

    response = client.delete(
        f"/profile-certifications/{profile['id']}/{certification['id']}",
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    assert (
        response.json()["message"]
        == "Profile certification deleted successfully."
    )

    profile_certifications_response = client.get(
        f"/profiles/{profile['id']}/certifications",
        headers=authenticated_headers,
    )

    assert profile_certifications_response.status_code == 200

    profile_certifications = profile_certifications_response.json()

    assert all(
        profile_certification["certification_id"] != certification["id"]
        for profile_certification in profile_certifications
    )


def test_delete_profile_certification_not_found(authenticated_headers):
    response = client.delete(
        "/profile-certifications/99999/99999",
        headers=authenticated_headers,
    )

    assert response.status_code == 404
