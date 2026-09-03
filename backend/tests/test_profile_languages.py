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


def create_language(name_prefix: str = "Language"):
    unique_language_name = f"{name_prefix}_{uuid4()}"

    response = client.post(
        "/languages",
        json={
            "name": unique_language_name,
        },
    )

    assert response.status_code == 200

    return response.json()


def create_profile_language(
    profile_id: int,
    language_id: int,
    proficiency_level: str = "Fluent",
):
    response = client.post(
        "/profile-languages",
        json={
            "profile_id": profile_id,
            "language_id": language_id,
            "proficiency_level": proficiency_level,
        },
    )

    assert response.status_code == 200

    return response.json()


def test_create_profile_language(authenticated_headers):
    profile = create_profile(authenticated_headers)
    language = create_language()

    response = client.post(
        "/profile-languages",
        json={
            "profile_id": profile["id"],
            "language_id": language["id"],
            "proficiency_level": "Native",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["profile_id"] == profile["id"]
    assert data["language_id"] == language["id"]
    assert data["proficiency_level"] == "Native"


def test_duplicate_profile_language(authenticated_headers):
    profile = create_profile(authenticated_headers)
    language = create_language()

    create_profile_language(
        profile["id"],
        language["id"],
    )

    response = client.post(
        "/profile-languages",
        json={
            "profile_id": profile["id"],
            "language_id": language["id"],
            "proficiency_level": "Fluent",
        },
    )

    assert response.status_code == 409


def test_list_languages_for_profile(authenticated_headers):
    profile = create_profile(authenticated_headers)
    language = create_language()

    create_profile_language(
        profile["id"],
        language["id"],
    )

    response = client.get(
        f"/profiles/{profile['id']}/languages",
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert any(
        profile_language["language_id"] == language["id"]
        for profile_language in data
    )


def test_update_profile_language(authenticated_headers):
    profile = create_profile(authenticated_headers)
    language = create_language()

    create_profile_language(
        profile["id"],
        language["id"],
        "Beginner",
    )

    response = client.put(
        f"/profile-languages/{profile['id']}/{language['id']}",
        json={
            "proficiency_level": "Advanced",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["profile_id"] == profile["id"]
    assert data["language_id"] == language["id"]
    assert data["proficiency_level"] == "Advanced"


def test_delete_profile_language(authenticated_headers):
    profile = create_profile(authenticated_headers)
    language = create_language()

    create_profile_language(
        profile["id"],
        language["id"],
    )

    response = client.delete(
        f"/profile-languages/{profile['id']}/{language['id']}"
    )

    assert response.status_code == 200

    profile_languages_response = client.get(
        f"/profiles/{profile['id']}/languages",
        headers=authenticated_headers,
    )

    assert profile_languages_response.status_code == 200

    profile_languages = profile_languages_response.json()

    assert all(
        profile_language["language_id"] != language["id"]
        for profile_language in profile_languages
    )
