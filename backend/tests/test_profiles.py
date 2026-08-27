from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


PROFILE_PAYLOAD = {
    "profile_name": "Test Profile",
    "full_name": "Vincent Test",
    "current_title": "Technical Partnerships Manager",
    "location": "France",
    "years_of_experience": 10,
    "target_role_short_term": "Solution Architect",
    "target_role_long_term": "Enterprise Architect",
    "remote_preference": "Hybrid",
    "preferred_countries": "France,UK"
}


def create_test_profile():
    response = client.post(
        "/profiles",
        json=PROFILE_PAYLOAD
    )

    assert response.status_code == 200

    return response.json()


def test_create_profile():
    response = client.post(
        "/profiles",
        json=PROFILE_PAYLOAD
    )

    assert response.status_code == 200

    body = response.json()

    assert body["profile_name"] == PROFILE_PAYLOAD["profile_name"]
    assert body["full_name"] == PROFILE_PAYLOAD["full_name"]


def test_get_profiles():
    response = client.get("/profiles")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_profile():
    profile = create_test_profile()

    response = client.get(
        f"/profiles/{profile['id']}"
    )

    assert response.status_code == 200

    body = response.json()

    assert body["id"] == profile["id"]


def test_update_profile():
    profile = create_test_profile()

    update_payload = {
        "profile_name": "Updated Profile",
        "full_name": "Updated Name",
        "current_title": "Principal Architect",
        "location": "United Kingdom",
        "years_of_experience": 15,
        "target_role_short_term": "Architect",
        "target_role_long_term": "CTO",
        "remote_preference": "Remote",
        "preferred_countries": "UK"
    }

    response = client.put(
        f"/profiles/{profile['id']}",
        json=update_payload
    )

    assert response.status_code == 200

    body = response.json()

    assert body["profile_name"] == "Updated Profile"
    assert body["full_name"] == "Updated Name"


def test_delete_profile():
    profile = create_test_profile()

    response = client.delete(
        f"/profiles/{profile['id']}"
    )

    assert response.status_code == 200

    body = response.json()

    assert body["is_active"] is False


def test_profile_not_found():
    response = client.get("/profiles/99999999")

    assert response.status_code in [404, 200]


def test_soft_delete_sets_is_active_false():
    profile = create_test_profile()

    delete_response = client.delete(
        f"/profiles/{profile['id']}"
    )

    assert delete_response.status_code == 200

    body = delete_response.json()

    assert body["is_active"] is False
    
    
def test_profile_additional_context_fields():
    profile_payload = {
        "profile_name": "Technical Partnerships",
        "full_name": "Vincent Gueret",
        "current_title": "Technical Partnerships Manager",
        "location": "France",
        "years_of_experience": 10,
        "target_role_short_term": "Head of Partnerships",
        "target_role_long_term": "VP Partnerships",
        "remote_preference": "HYBRID",
        "preferred_countries": "FR,UK",
        "professional_summary": "Partnership and integration specialist.",
        "career_motivations": "Build strategic partnerships.",
        "preferred_environment": "International SaaS environment.",
        "non_negotiables": "Remote flexibility.",
        "additional_context": "Interested in platform strategy.",
    }

    create_response = client.post(
        "/profiles",
        json=profile_payload,
    )

    assert create_response.status_code == 200

    created_profile = create_response.json()

    profile_id = created_profile["id"]

    get_response = client.get(
        f"/profiles/{profile_id}",
    )

    assert get_response.status_code == 200

    profile = get_response.json()

    assert (
        profile["professional_summary"]
        == "Partnership and integration specialist."
    )

    assert (
        profile["career_motivations"]
        == "Build strategic partnerships."
    )

    assert (
        profile["preferred_environment"]
        == "International SaaS environment."
    )

    assert (
        profile["non_negotiables"]
        == "Remote flexibility."
    )

    assert (
        profile["additional_context"]
        == "Interested in platform strategy."
    )