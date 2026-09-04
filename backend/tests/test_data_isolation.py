from uuid import uuid4

from fastapi.testclient import TestClient

from app.auth.models import User
from app.auth.service import hash_password
from app.core.database import SessionLocal
from app.main import app


client = TestClient(app)


def create_second_user_headers():
    email = f"isolation-test-{uuid4()}@career-os.local"
    password = "IsolationTestPassword123!"

    db = SessionLocal()

    try:
        second_user = User(
            email=email,
            hashed_password=hash_password(password),
            is_active=True,
        )

        db.add(second_user)
        db.commit()
    finally:
        db.close()

    login_response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    assert login_response.status_code == 200

    access_token = login_response.json()["access_token"]

    return {
        "Authorization": f"Bearer {access_token}",
    }


def create_full_dataset(authenticated_headers):
    profile_response = client.post(
        "/profiles",
        json={
            "profile_name": f"Isolation Profile_{uuid4()}",
            "full_name": "Isolation Test User",
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

    assert profile_response.status_code == 200

    profile = profile_response.json()

    cv_response = client.post(
        f"/profiles/{profile['id']}/cvs",
        files={
            "cv_file": (
                "isolation-test-cv.pdf",
                b"Isolation test CV content",
                "application/pdf",
            ),
        },
        data={
            "language": "fr",
            "version_label": "Isolation Test Version",
            "is_default": "true",
        },
        headers=authenticated_headers,
    )

    assert cv_response.status_code == 200

    cv = cv_response.json()

    skill_response = client.post(
        "/skills",
        json={
            "name": f"Isolation Skill_{uuid4()}",
            "category": "Technical",
        },
    )

    assert skill_response.status_code == 200

    skill = skill_response.json()

    profile_skill_response = client.post(
        "/profile-skills",
        json={
            "profile_id": profile["id"],
            "skill_id": skill["id"],
            "years_of_experience": 3,
            "self_assessment_level": "Intermediate",
        },
        headers=authenticated_headers,
    )

    assert profile_skill_response.status_code == 200

    soft_skill_response = client.post(
        "/profile-soft-skills",
        json={
            "profile_id": profile["id"],
            "name": f"Isolation Soft Skill_{uuid4()}",
        },
        headers=authenticated_headers,
    )

    assert soft_skill_response.status_code == 200

    soft_skill = soft_skill_response.json()

    language_response = client.post(
        "/languages",
        json={
            "name": f"Isolation Language_{uuid4()}",
        },
    )

    assert language_response.status_code == 200

    language = language_response.json()

    profile_language_response = client.post(
        "/profile-languages",
        json={
            "profile_id": profile["id"],
            "language_id": language["id"],
            "proficiency_level": "Fluent",
        },
        headers=authenticated_headers,
    )

    assert profile_language_response.status_code == 200

    certification_response = client.post(
        "/certifications",
        json={
            "name": f"Isolation Certification_{uuid4()}",
            "issuing_organization": "Test Organization",
        },
    )

    assert certification_response.status_code == 200

    certification = certification_response.json()

    profile_certification_response = client.post(
        "/profile-certifications",
        json={
            "profile_id": profile["id"],
            "certification_id": certification["id"],
            "obtained_date": "2024-01-01",
            "expiration_date": "2026-01-01",
            "credential_id": "ISOLATION-TEST-001",
        },
        headers=authenticated_headers,
    )

    assert profile_certification_response.status_code == 200

    work_experience_response = client.post(
        "/work-experiences",
        json={
            "profile_id": profile["id"],
            "company_name": "Isolation Test Company",
            "job_title": "Backend Developer",
            "start_date": "2020-01-01",
            "end_date": "2022-12-31",
            "is_current_position": False,
            "description": "Isolation test work experience.",
        },
        headers=authenticated_headers,
    )

    assert work_experience_response.status_code == 200

    work_experience = work_experience_response.json()

    application_response = client.post(
        "/applications",
        json={
            "profile_id": profile["id"],
            "job_offer_id": 1,
            "status": "Applied",
        },
        headers=authenticated_headers,
    )

    assert application_response.status_code == 200

    application = application_response.json()

    return {
        "profile": profile,
        "cv": cv,
        "skill": skill,
        "soft_skill": soft_skill,
        "language": language,
        "certification": certification,
        "work_experience": work_experience,
        "application": application,
    }


def test_profile_is_isolated_between_users(authenticated_headers):
    other_headers = create_second_user_headers()

    dataset = create_full_dataset(authenticated_headers)

    profile_id = dataset["profile"]["id"]

    list_response = client.get(
        "/profiles",
        headers=other_headers,
    )

    assert list_response.status_code == 200

    other_user_profile_ids = [
        item["id"] for item in list_response.json()
    ]

    assert profile_id not in other_user_profile_ids

    get_response = client.get(
        f"/profiles/{profile_id}",
        headers=other_headers,
    )

    assert get_response.status_code == 404


def test_cv_is_isolated_between_users(authenticated_headers):
    other_headers = create_second_user_headers()

    dataset = create_full_dataset(authenticated_headers)

    profile_id = dataset["profile"]["id"]
    cv_id = dataset["cv"]["id"]

    list_response = client.get(
        f"/profiles/{profile_id}/cvs",
        headers=other_headers,
    )

    assert list_response.status_code == 404

    get_response = client.get(
        f"/cvs/{cv_id}",
        headers=other_headers,
    )

    assert get_response.status_code == 404

    download_response = client.get(
        f"/cvs/{cv_id}/download",
        headers=other_headers,
    )

    assert download_response.status_code == 404


def test_profile_skills_are_isolated_between_users(authenticated_headers):
    other_headers = create_second_user_headers()

    dataset = create_full_dataset(authenticated_headers)

    profile_id = dataset["profile"]["id"]
    skill_id = dataset["skill"]["id"]

    list_response = client.get(
        f"/profiles/{profile_id}/skills",
        headers=other_headers,
    )

    assert list_response.status_code == 404

    update_response = client.put(
        f"/profile-skills/{profile_id}/{skill_id}",
        json={
            "years_of_experience": 10,
            "self_assessment_level": "Expert",
        },
        headers=other_headers,
    )

    assert update_response.status_code == 404

    delete_response = client.delete(
        f"/profile-skills/{profile_id}/{skill_id}",
        headers=other_headers,
    )

    assert delete_response.status_code == 404


def test_profile_soft_skills_are_isolated_between_users(authenticated_headers):
    other_headers = create_second_user_headers()

    dataset = create_full_dataset(authenticated_headers)

    profile_id = dataset["profile"]["id"]
    soft_skill_id = dataset["soft_skill"]["id"]

    list_response = client.get(
        f"/profiles/{profile_id}/soft-skills",
        headers=other_headers,
    )

    assert list_response.status_code == 404

    delete_response = client.delete(
        f"/profile-soft-skills/{soft_skill_id}",
        headers=other_headers,
    )

    assert delete_response.status_code == 404


def test_profile_languages_are_isolated_between_users(authenticated_headers):
    other_headers = create_second_user_headers()

    dataset = create_full_dataset(authenticated_headers)

    profile_id = dataset["profile"]["id"]
    language_id = dataset["language"]["id"]

    list_response = client.get(
        f"/profiles/{profile_id}/languages",
        headers=other_headers,
    )

    assert list_response.status_code == 404

    update_response = client.put(
        f"/profile-languages/{profile_id}/{language_id}",
        json={
            "proficiency_level": "Native",
        },
        headers=other_headers,
    )

    assert update_response.status_code == 404

    delete_response = client.delete(
        f"/profile-languages/{profile_id}/{language_id}",
        headers=other_headers,
    )

    assert delete_response.status_code == 404


def test_profile_certifications_are_isolated_between_users(authenticated_headers):
    other_headers = create_second_user_headers()

    dataset = create_full_dataset(authenticated_headers)

    profile_id = dataset["profile"]["id"]
    certification_id = dataset["certification"]["id"]

    list_response = client.get(
        f"/profiles/{profile_id}/certifications",
        headers=other_headers,
    )

    assert list_response.status_code == 404

    update_response = client.put(
        f"/profile-certifications/{profile_id}/{certification_id}",
        json={
            "obtained_date": "2025-01-01",
            "expiration_date": "2027-01-01",
            "credential_id": "HACKED-CREDENTIAL",
        },
        headers=other_headers,
    )

    assert update_response.status_code == 404

    delete_response = client.delete(
        f"/profile-certifications/{profile_id}/{certification_id}",
        headers=other_headers,
    )

    assert delete_response.status_code == 404


def test_work_experience_is_isolated_between_users(authenticated_headers):
    other_headers = create_second_user_headers()

    dataset = create_full_dataset(authenticated_headers)

    profile_id = dataset["profile"]["id"]
    work_experience_id = dataset["work_experience"]["id"]

    list_response = client.get(
        f"/profiles/{profile_id}/work-experiences",
        headers=other_headers,
    )

    assert list_response.status_code == 404

    get_response = client.get(
        f"/work-experiences/{work_experience_id}",
        headers=other_headers,
    )

    assert get_response.status_code == 404

    update_response = client.put(
        f"/work-experiences/{work_experience_id}",
        json={
            "company_name": "Hacked Company",
            "job_title": "Hacked Role",
            "start_date": "2020-01-01",
            "end_date": None,
            "is_current_position": True,
            "description": "This update should not succeed.",
        },
        headers=other_headers,
    )

    assert update_response.status_code == 404

    delete_response = client.delete(
        f"/work-experiences/{work_experience_id}",
        headers=other_headers,
    )

    assert delete_response.status_code == 404


def test_application_is_isolated_between_users(authenticated_headers):
    other_headers = create_second_user_headers()

    dataset = create_full_dataset(authenticated_headers)

    application_id = dataset["application"]["id"]

    list_response = client.get(
        "/applications",
        headers=other_headers,
    )

    assert list_response.status_code == 200

    other_user_application_ids = [
        item["id"] for item in list_response.json()
    ]

    assert application_id not in other_user_application_ids

    get_response = client.get(
        f"/applications/{application_id}",
        headers=other_headers,
    )

    assert get_response.status_code == 404

    timeline_response = client.get(
        f"/applications/{application_id}/timeline",
        headers=other_headers,
    )

    assert timeline_response.status_code == 404

    status_response = client.post(
        f"/applications/{application_id}/status",
        json={
            "status": "Phone Screen",
        },
        headers=other_headers,
    )

    assert status_response.status_code == 404


def test_profile_enrichment_is_isolated_between_users(authenticated_headers):
    other_headers = create_second_user_headers()

    dataset = create_full_dataset(authenticated_headers)

    profile_id = dataset["profile"]["id"]
    cv_id = dataset["cv"]["id"]

    list_response = client.get(
        f"/profiles/{profile_id}/enrichment",
        headers=other_headers,
    )

    assert list_response.status_code == 404

    generate_response = client.post(
        f"/cvs/{cv_id}/enrichment/generate",
        headers=other_headers,
    )

    assert generate_response.status_code == 404

    accept_all_response = client.post(
        "/enrichment/accept-all",
        json={
            "profile_id": profile_id,
            "cv_id": cv_id,
        },
        headers=other_headers,
    )

    assert accept_all_response.status_code == 404
