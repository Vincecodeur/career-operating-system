from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def create_test_profile():
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
    )

    assert response.status_code == 200

    return response.json()


def create_test_skill():
    skill_name = f"Skill_{uuid4()}"

    response = client.post(
        "/skills",
        json={
            "name": skill_name,
            "category": "Technical",
        },
    )

    assert response.status_code == 200

    return response.json()


def create_test_profile_skill():
    profile = create_test_profile()
    skill = create_test_skill()

    response = client.post(
        "/profile-skills",
        json={
            "profile_id": profile["id"],
            "skill_id": skill["id"],
            "years_of_experience": 2,
            "self_assessment_level": "Intermediate",
        },
    )

    assert response.status_code == 200

    return {
        "profile": profile,
        "skill": skill,
        "profile_skill": response.json(),
    }


def test_create_profile_skill():
    profile = create_test_profile()
    skill = create_test_skill()

    response = client.post(
        "/profile-skills",
        json={
            "profile_id": profile["id"],
            "skill_id": skill["id"],
            "years_of_experience": 3,
            "self_assessment_level": "Advanced",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["profile_id"] == profile["id"]
    assert data["skill_id"] == skill["id"]
    assert data["years_of_experience"] == 3
    assert data["self_assessment_level"] == "Advanced"


def test_list_profile_skills():
    response = client.get(
        "/profile-skills"
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list,
    )


def test_list_skills_for_profile():
    data = create_test_profile_skill()

    profile_id = data["profile"]["id"]
    skill_id = data["skill"]["id"]

    response = client.get(
        f"/profiles/{profile_id}/skills"
    )

    assert response.status_code == 200

    profile_skills = response.json()

    assert any(
        profile_skill["skill_id"] == skill_id
        for profile_skill in profile_skills
    )


def test_update_profile_skill():
    data = create_test_profile_skill()

    profile_id = data["profile"]["id"]
    skill_id = data["skill"]["id"]

    response = client.put(
        f"/profile-skills/{profile_id}/{skill_id}",
        json={
            "years_of_experience": 7,
            "self_assessment_level": "Expert",
        },
    )

    assert response.status_code == 200

    updated_profile_skill = response.json()

    assert updated_profile_skill["profile_id"] == profile_id
    assert updated_profile_skill["skill_id"] == skill_id
    assert updated_profile_skill["years_of_experience"] == 7
    assert updated_profile_skill["self_assessment_level"] == "Expert"


def test_update_profile_skill_not_found():
    response = client.put(
        "/profile-skills/999999/999999",
        json={
            "years_of_experience": 1,
            "self_assessment_level": "Beginner",
        },
    )

    assert response.status_code == 404


def test_delete_profile_skill():
    data = create_test_profile_skill()

    profile_id = data["profile"]["id"]
    skill_id = data["skill"]["id"]

    response = client.delete(
        f"/profile-skills/{profile_id}/{skill_id}"
    )

    assert response.status_code == 200

    deleted_profile_skill = response.json()

    assert deleted_profile_skill["profile_id"] == profile_id
    assert deleted_profile_skill["skill_id"] == skill_id

    profile_skills_response = client.get(
        f"/profiles/{profile_id}/skills"
    )

    assert profile_skills_response.status_code == 200

    profile_skills = profile_skills_response.json()

    assert all(
        profile_skill["skill_id"] != skill_id
        for profile_skill in profile_skills
    )

    skill_response = client.get(
        f"/skills/{skill_id}"
    )

    assert skill_response.status_code == 200


def test_delete_profile_skill_not_found():
    response = client.delete(
        "/profile-skills/999999/999999"
    )

    assert response.status_code == 404