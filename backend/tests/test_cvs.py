from uuid import uuid4

from fastapi.testclient import TestClient

from app.core.database import create_tables
from app.main import app


create_tables()

client = TestClient(app)


def create_test_profile(authenticated_headers):
    profile_name = f"Profile_{uuid4()}"

    response = client.post(
        "/profiles",
        json={
            "profile_name": profile_name,
            "full_name": "Test User",
            "current_title": "Product Manager",
            "location": "Paris",
            "years_of_experience": 8,
            "target_role_short_term": "Senior Product Manager",
            "target_role_long_term": "Head of Product",
            "remote_preference": "Hybrid",
            "preferred_countries": "France",
        },
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    return response.json()


def create_test_cv(
    profile_id: int,
    file_name: str = "test-cv.pdf",
    content: bytes = b"Test CV content",
    language: str = "fr",
    version_label: str = "Test Version",
    is_default: bool = False,
):
    response = client.post(
        f"/profiles/{profile_id}/cvs",
        files={
            "cv_file": (
                file_name,
                content,
                "application/pdf",
            ),
        },
        data={
            "language": language,
            "version_label": version_label,
            "is_default": str(is_default).lower(),
        },
    )

    assert response.status_code == 200

    return response.json()


def test_create_cv(authenticated_headers):
    profile = create_test_profile(authenticated_headers)

    response = client.post(
        f"/profiles/{profile['id']}/cvs",
        files={
            "cv_file": (
                "product-manager-cv.pdf",
                b"Product Manager CV content",
                "application/pdf",
            ),
        },
        data={
            "language": "fr",
            "version_label": "France 2026",
            "is_default": "true",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["profile_id"] == profile["id"]
    assert data["original_file_name"] == "product-manager-cv.pdf"
    assert data["language"] == "fr"
    assert data["version_label"] == "France 2026"
    assert data["is_default"] is True
    assert data["parsing_status"] == "PENDING"
    assert data["file_size_bytes"] > 0
    assert data["mime_type"] == "application/pdf"


def test_profile_can_have_multiple_cvs(authenticated_headers):
    profile = create_test_profile(authenticated_headers)

    first_cv = create_test_cv(
        profile_id=profile["id"],
        file_name="cv-fr.pdf",
        language="fr",
        version_label="FR Version",
    )

    second_cv = create_test_cv(
        profile_id=profile["id"],
        file_name="cv-en.pdf",
        language="en",
        version_label="EN Version",
    )

    response = client.get(
        f"/profiles/{profile['id']}/cvs"
    )

    assert response.status_code == 200

    cvs = response.json()

    cv_ids = [
        cv["id"]
        for cv in cvs
    ]

    assert first_cv["id"] in cv_ids
    assert second_cv["id"] in cv_ids


def test_list_profile_cvs(authenticated_headers):
    profile = create_test_profile(authenticated_headers)

    cv = create_test_cv(
        profile_id=profile["id"],
    )

    response = client.get(
        f"/profiles/{profile['id']}/cvs"
    )

    assert response.status_code == 200

    cvs = response.json()

    assert isinstance(cvs, list)

    assert any(
        existing_cv["id"] == cv["id"]
        for existing_cv in cvs
    )


def test_get_cv(authenticated_headers):
    profile = create_test_profile(authenticated_headers)

    cv = create_test_cv(
        profile_id=profile["id"],
    )

    response = client.get(
        f"/cvs/{cv['id']}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == cv["id"]
    assert data["profile_id"] == profile["id"]


def test_cv_not_found():
    response = client.get(
        "/cvs/99999999"
    )

    assert response.status_code == 404


def test_update_cv(authenticated_headers):
    profile = create_test_profile(authenticated_headers)

    cv = create_test_cv(
        profile_id=profile["id"],
        language="fr",
        version_label="Initial Version",
    )

    response = client.put(
        f"/cvs/{cv['id']}",
        json={
            "language": "en",
            "version_label": "Updated Version",
        },
    )

    assert response.status_code == 200

    updated_cv = response.json()

    assert updated_cv["id"] == cv["id"]
    assert updated_cv["language"] == "en"
    assert updated_cv["version_label"] == "Updated Version"


def test_set_default_cv(authenticated_headers):
    profile = create_test_profile(authenticated_headers)

    cv = create_test_cv(
        profile_id=profile["id"],
        is_default=False,
    )

    response = client.post(
        f"/cvs/{cv['id']}/set-default"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == cv["id"]
    assert data["is_default"] is True


def test_only_one_default_cv_per_profile(authenticated_headers):
    profile = create_test_profile(authenticated_headers)

    first_cv = create_test_cv(
        profile_id=profile["id"],
        file_name="first-cv.pdf",
        is_default=True,
    )

    second_cv = create_test_cv(
        profile_id=profile["id"],
        file_name="second-cv.pdf",
        is_default=False,
    )

    response = client.post(
        f"/cvs/{second_cv['id']}/set-default"
    )

    assert response.status_code == 200

    list_response = client.get(
        f"/profiles/{profile['id']}/cvs"
    )

    assert list_response.status_code == 200

    cvs = list_response.json()

    first_cv_after_update = next(
        cv
        for cv in cvs
        if cv["id"] == first_cv["id"]
    )

    second_cv_after_update = next(
        cv
        for cv in cvs
        if cv["id"] == second_cv["id"]
    )

    assert first_cv_after_update["is_default"] is False
    assert second_cv_after_update["is_default"] is True


def test_delete_cv(authenticated_headers):
    profile = create_test_profile(authenticated_headers)

    cv = create_test_cv(
        profile_id=profile["id"],
    )

    response = client.delete(
        f"/cvs/{cv['id']}"
    )

    assert response.status_code == 200

    deleted_cv = response.json()

    assert deleted_cv["id"] == cv["id"]

    get_response = client.get(
        f"/cvs/{cv['id']}"
    )

    assert get_response.status_code == 404


def test_delete_default_cv(authenticated_headers):
    profile = create_test_profile(authenticated_headers)

    cv = create_test_cv(
        profile_id=profile["id"],
        is_default=True,
    )

    response = client.delete(
        f"/cvs/{cv['id']}"
    )

    assert response.status_code == 200

    list_response = client.get(
        f"/profiles/{profile['id']}/cvs"
    )

    assert list_response.status_code == 200

    cvs = list_response.json()

    assert all(
        existing_cv["is_default"] is False
        for existing_cv in cvs
    )


def test_profile_cannot_see_other_profile_cvs(authenticated_headers):
    first_profile = create_test_profile(authenticated_headers)
    second_profile = create_test_profile(authenticated_headers)

    first_profile_cv = create_test_cv(
        profile_id=first_profile["id"],
        file_name="first-profile-cv.pdf",
    )

    second_profile_cv = create_test_cv(
        profile_id=second_profile["id"],
        file_name="second-profile-cv.pdf",
    )

    response = client.get(
        f"/profiles/{first_profile['id']}/cvs"
    )

    assert response.status_code == 200

    first_profile_cvs = response.json()

    first_profile_cv_ids = [
        cv["id"]
        for cv in first_profile_cvs
    ]

    assert first_profile_cv["id"] in first_profile_cv_ids
    assert second_profile_cv["id"] not in first_profile_cv_ids


def test_cv_created_with_pending_parsing_status(authenticated_headers):
    profile = create_test_profile(authenticated_headers)

    cv = create_test_cv(
        profile_id=profile["id"],
    )

    assert cv["parsing_status"] == "PENDING"
