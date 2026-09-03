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


def create_test_work_experience(authenticated_headers):
    profile = create_test_profile(authenticated_headers)

    response = client.post(
        "/work-experiences",
        json={
            "profile_id": profile["id"],
            "company_name": "Test Company",
            "job_title": "Backend Developer",
            "start_date": "2020-01-01",
            "end_date": "2022-12-31",
            "is_current_position": False,
            "description": "Built backend APIs and integration services.",
        },
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    return {
        "profile": profile,
        "work_experience": response.json(),
    }


def test_create_work_experience(authenticated_headers):
    profile = create_test_profile(authenticated_headers)

    response = client.post(
        "/work-experiences",
        json={
            "profile_id": profile["id"],
            "company_name": "Create Test Company",
            "job_title": "Software Engineer",
            "start_date": "2021-01-01",
            "end_date": "2023-01-01",
            "is_current_position": False,
            "description": "Created and maintained backend services.",
        },
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["profile_id"] == profile["id"]
    assert data["company_name"] == "Create Test Company"
    assert data["job_title"] == "Software Engineer"
    assert data["start_date"] == "2021-01-01"
    assert data["end_date"] == "2023-01-01"
    assert data["is_current_position"] is False
    assert data["description"] == "Created and maintained backend services."
    assert "id" in data


def test_list_work_experiences():
    response = client.get(
        "/work-experiences"
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list,
    )


def test_get_work_experience(authenticated_headers):
    data = create_test_work_experience(authenticated_headers)

    work_experience_id = data["work_experience"]["id"]

    response = client.get(
        f"/work-experiences/{work_experience_id}",
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    work_experience = response.json()

    assert work_experience["id"] == work_experience_id
    assert work_experience["company_name"] == "Test Company"
    assert work_experience["job_title"] == "Backend Developer"


def test_list_work_experiences_for_profile(authenticated_headers):
    data = create_test_work_experience(authenticated_headers)

    profile_id = data["profile"]["id"]
    work_experience_id = data["work_experience"]["id"]

    response = client.get(
        f"/profiles/{profile_id}/work-experiences",
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    work_experiences = response.json()

    assert any(
        work_experience["id"] == work_experience_id
        for work_experience in work_experiences
    )


def test_update_work_experience(authenticated_headers):
    data = create_test_work_experience(authenticated_headers)

    work_experience_id = data["work_experience"]["id"]

    response = client.put(
        f"/work-experiences/{work_experience_id}",
        json={
            "company_name": "Updated Company",
            "job_title": "Senior Backend Developer",
            "start_date": "2020-02-01",
            "end_date": None,
            "is_current_position": True,
            "description": "Updated backend ownership and platform responsibilities.",
        },
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    updated_work_experience = response.json()

    assert updated_work_experience["id"] == work_experience_id
    assert updated_work_experience["company_name"] == "Updated Company"
    assert updated_work_experience["job_title"] == "Senior Backend Developer"
    assert updated_work_experience["start_date"] == "2020-02-01"
    assert updated_work_experience["end_date"] is None
    assert updated_work_experience["is_current_position"] is True
    assert (
        updated_work_experience["description"]
        == "Updated backend ownership and platform responsibilities."
    )


def test_update_work_experience_not_found(authenticated_headers):
    response = client.put(
        "/work-experiences/999999",
        json={
            "company_name": "Missing Company",
            "job_title": "Missing Role",
            "start_date": "2020-01-01",
            "end_date": None,
            "is_current_position": False,
            "description": "This update should fail.",
        },
        headers=authenticated_headers,
    )

    assert response.status_code == 404


def test_delete_work_experience(authenticated_headers):
    data = create_test_work_experience(authenticated_headers)

    work_experience_id = data["work_experience"]["id"]

    response = client.delete(
        f"/work-experiences/{work_experience_id}",
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    delete_response = response.json()

    assert delete_response["message"] == "Work experience deleted."

    get_response = client.get(
        f"/work-experiences/{work_experience_id}",
        headers=authenticated_headers,
    )

    assert get_response.status_code == 404


def test_delete_work_experience_not_found(authenticated_headers):
    response = client.delete(
        "/work-experiences/999999",
        headers=authenticated_headers,
    )

    assert response.status_code == 404
