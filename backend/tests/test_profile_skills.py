from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def create_test_profile(authenticated_headers):
    profile_name = f"Profile_{uuid4()}"

    response = client.post(
        "/profiles",
        json={
            "profile_name": profile_name,
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


def create_test_skill(name_prefix: str = "Skill"):
    unique_skill_name = f"{name_prefix}_{uuid4()}"

    response = client.post(
        "/skills",
        json={
            "name": unique_skill_name,
            "category": "Technical",
        },
    )

    assert response.status_code == 200

    return response.json()


def create_test_profile_skill(authenticated_headers):
    profile = create_test_profile(authenticated_headers)
    skill = create_test_skill()

    response = client.post(
        "/profile-skills",
        json={
            "profile_id": profile["id"],
            "skill_id": skill["id"],
            "years_of_experience": 3,
            "self_assessment_level": "Intermediate",
        },
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    return {
        "profile": profile,
        "skill": skill,
        "profile_skill": response.json(),
    }


def test_create_profile_skill(authenticated_headers):
    profile = create_test_profile(authenticated_headers)
    skill = create_test_skill()

    response = client.post(
        "/profile-skills",
        json={
            "profile_id": profile["id"],
            "skill_id": skill["id"],
            "years_of_experience": 5,
            "self_assessment_level": "Advanced",
        },
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["profile_id"] == profile["id"]
    assert data["skill_id"] == skill["id"]
    assert data["years_of_experience"] == 5
    assert data["self_assessment_level"] == "Advanced"


def test_list_profile_skills(authenticated_headers):
    create_test_profile_skill(authenticated_headers)

    response = client.get(
        "/profile-skills",
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list,
    )


def test_list_skills_for_profile(authenticated_headers):
    data = create_test_profile_skill(authenticated_headers)

    profile_id = data["profile"]["id"]
    skill_id = data["skill"]["id"]

    response = client.get(
        f"/profiles/{profile_id}/skills",
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    profile_skills = response.json()

    assert any(
        profile_skill["skill_id"] == skill_id
        for profile_skill in profile_skills
    )


def test_update_profile_skill(authenticated_headers):
    data = create_test_profile_skill(authenticated_headers)

    profile_id = data["profile"]["id"]
    skill_id = data["skill"]["id"]

    response = client.put(
        f"/profile-skills/{profile_id}/{skill_id}",
        json={
            "years_of_experience": 8,
            "self_assessment_level": "Expert",
        },
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    updated = response.json()

    assert updated["profile_id"] == profile_id
    assert updated["skill_id"] == skill_id
    assert updated["years_of_experience"] == 8
    assert updated["self_assessment_level"] == "Expert"


def test_update_profile_skill_not_found(authenticated_headers):
    response = client.put(
        "/profile-skills/999999/999999",
        json={
            "years_of_experience": 1,
            "self_assessment_level": "Beginner",
        },
        headers=authenticated_headers,
    )

    assert response.status_code == 404


def test_delete_profile_skill(authenticated_headers):
    data = create_test_profile_skill(authenticated_headers)

    profile_id = data["profile"]["id"]
    skill_id = data["skill"]["id"]

    response = client.delete(
        f"/profile-skills/{profile_id}/{skill_id}",
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    list_response = client.get(
        f"/profiles/{profile_id}/skills",
        headers=authenticated_headers,
    )

    assert list_response.status_code == 200

    remaining_skill_ids = {
        profile_skill["skill_id"]
        for profile_skill in list_response.json()
    }

    assert skill_id not in remaining_skill_ids


def test_delete_profile_skill_not_found(authenticated_headers):
    response = client.delete(
        "/profile-skills/999999/999999",
        headers=authenticated_headers,
    )

    assert response.status_code == 404
