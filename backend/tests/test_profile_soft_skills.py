from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def create_profile():
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
            "remote_preference": "HYBRID",
            "preferred_countries": "FR",
        },
    )

    assert response.status_code == 200

    return response.json()


def create_soft_skill(
    profile_id: int,
    name: str,
):
    response = client.post(
        "/profile-soft-skills",
        json={
            "profile_id": profile_id,
            "name": name,
        },
    )

    assert response.status_code == 200

    return response.json()


def test_create_profile_soft_skill():
    profile = create_profile()
    soft_skill_name = f"Leadership_{uuid4()}"

    response = client.post(
        "/profile-soft-skills",
        json={
            "profile_id": profile["id"],
            "name": soft_skill_name,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["profile_id"] == profile["id"]
    assert data["name"] == soft_skill_name
    assert "id" in data
    assert "created_at" in data


def test_create_profile_soft_skill_trims_name():
    profile = create_profile()
    soft_skill_name = f"Communication_{uuid4()}"

    response = client.post(
        "/profile-soft-skills",
        json={
            "profile_id": profile["id"],
            "name": f"  {soft_skill_name}  ",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == soft_skill_name


def test_create_profile_soft_skill_requires_name():
    profile = create_profile()

    response = client.post(
        "/profile-soft-skills",
        json={
            "profile_id": profile["id"],
            "name": "   ",
        },
    )

    assert response.status_code == 400


def test_create_profile_soft_skill_profile_not_found():
    response = client.post(
        "/profile-soft-skills",
        json={
            "profile_id": 999999,
            "name": "Leadership",
        },
    )

    assert response.status_code == 404


def test_duplicate_profile_soft_skill_for_same_profile():
    profile = create_profile()
    soft_skill_name = f"Negotiation_{uuid4()}"

    create_soft_skill(
        profile["id"],
        soft_skill_name,
    )

    response = client.post(
        "/profile-soft-skills",
        json={
            "profile_id": profile["id"],
            "name": soft_skill_name,
        },
    )

    assert response.status_code == 409


def test_same_soft_skill_name_allowed_for_different_profiles():
    first_profile = create_profile()
    second_profile = create_profile()

    soft_skill_name = f"Problem Solving_{uuid4()}"

    first_response = client.post(
        "/profile-soft-skills",
        json={
            "profile_id": first_profile["id"],
            "name": soft_skill_name,
        },
    )

    assert first_response.status_code == 200

    second_response = client.post(
        "/profile-soft-skills",
        json={
            "profile_id": second_profile["id"],
            "name": soft_skill_name,
        },
    )

    assert second_response.status_code == 200


def test_list_soft_skills_for_profile():
    profile = create_profile()

    first_soft_skill = create_soft_skill(
        profile["id"],
        f"Adaptability_{uuid4()}",
    )

    second_soft_skill = create_soft_skill(
        profile["id"],
        f"Teamwork_{uuid4()}",
    )

    response = client.get(
        f"/profiles/{profile['id']}/soft-skills"
    )

    assert response.status_code == 200

    data = response.json()

    soft_skill_ids = {
        soft_skill["id"]
        for soft_skill in data
    }

    assert first_soft_skill["id"] in soft_skill_ids
    assert second_soft_skill["id"] in soft_skill_ids


def test_list_soft_skills_profile_not_found():
    response = client.get(
        "/profiles/999999/soft-skills"
    )

    assert response.status_code == 404


def test_delete_profile_soft_skill():
    profile = create_profile()

    soft_skill = create_soft_skill(
        profile["id"],
        f"Stakeholder Management_{uuid4()}",
    )

    response = client.delete(
        f"/profile-soft-skills/{soft_skill['id']}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == (
        "Soft skill deleted successfully."
    )

    list_response = client.get(
        f"/profiles/{profile['id']}/soft-skills"
    )

    assert list_response.status_code == 200

    remaining_ids = {
        item["id"]
        for item in list_response.json()
    }

    assert soft_skill["id"] not in remaining_ids


def test_delete_profile_soft_skill_not_found():
    response = client.delete(
        "/profile-soft-skills/999999"
    )

    assert response.status_code == 404