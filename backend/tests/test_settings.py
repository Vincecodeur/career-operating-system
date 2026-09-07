from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def reset_ai_settings(authenticated_headers):
    client.put(
        "/settings/ai",
        json={
            "ai_features_enabled": False,
            "ai_consent_accepted": False,
        },
        headers=authenticated_headers,
    )


def test_get_job_discovery_settings(authenticated_headers):
    response = client.get(
        "/settings/job-discovery",
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert "discovery_enabled" in data
    assert "discovery_interval_minutes" in data
    assert "discovery_connectors" in data


def test_update_job_discovery_settings(authenticated_headers):
    response = client.put(
        "/settings/job-discovery",
        json={
            "discovery_enabled": True,
            "discovery_interval_minutes": 720,
            "discovery_connectors": ["france_travail"],
        },
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["discovery_enabled"] is True
    assert data["discovery_interval_minutes"] == 720
    assert data["discovery_connectors"] == ["france_travail"]


def test_get_search_criteria_settings(authenticated_headers):
    response = client.get(
        "/settings/search-criteria",
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert "target_job_titles" in data
    assert "preferred_countries" in data
    assert "work_modes" in data
    assert "included_keywords" in data
    assert "excluded_keywords" in data


def test_update_search_criteria_settings(authenticated_headers):
    response = client.put(
        "/settings/search-criteria",
        json={
            "target_job_titles": ["Product Manager"],
            "preferred_countries": ["FR"],
            "work_modes": ["Remote"],
            "included_keywords": ["python"],
            "excluded_keywords": ["java"],
        },
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["target_job_titles"] == ["Product Manager"]
    assert data["preferred_countries"] == ["FR"]
    assert data["work_modes"] == ["Remote"]
    assert data["included_keywords"] == ["python"]
    assert data["excluded_keywords"] == ["java"]


def test_get_discovery_preferences_settings(authenticated_headers):
    response = client.get(
        "/settings/discovery-preferences",
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert "discovery_age_window" in data
    assert "discovery_minimum_matching_score" in data
    assert "discovery_show_archived" in data
    assert "discovery_default_sort" in data


def test_update_discovery_preferences_settings(authenticated_headers):
    response = client.put(
        "/settings/discovery-preferences",
        json={
            "discovery_age_window": "7_DAYS",
            "discovery_minimum_matching_score": 50,
            "discovery_show_archived": True,
            "discovery_default_sort": "NEWEST_FIRST",
        },
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["discovery_age_window"] == "7_DAYS"
    assert data["discovery_minimum_matching_score"] == 50
    assert data["discovery_show_archived"] is True
    assert data["discovery_default_sort"] == "NEWEST_FIRST"


def test_get_ai_settings_requires_authentication():
    response = client.get(
        "/settings/ai"
    )

    assert response.status_code == 401


def test_get_ai_settings_returns_disabled_defaults(authenticated_headers):
    reset_ai_settings(authenticated_headers)

    response = client.get(
        "/settings/ai",
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    assert response.json() == {
        "ai_features_enabled": False,
        "ai_consent_accepted": False,
    }


def test_enable_ai_features_with_consent(authenticated_headers):
    reset_ai_settings(authenticated_headers)

    response = client.put(
        "/settings/ai",
        json={
            "ai_features_enabled": True,
            "ai_consent_accepted": True,
        },
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    assert response.json() == {
        "ai_features_enabled": True,
        "ai_consent_accepted": True,
    }

    reset_ai_settings(authenticated_headers)


def test_enabled_ai_settings_are_persisted(authenticated_headers):
    reset_ai_settings(authenticated_headers)

    update_response = client.put(
        "/settings/ai",
        json={
            "ai_features_enabled": True,
            "ai_consent_accepted": True,
        },
        headers=authenticated_headers,
    )

    assert update_response.status_code == 200

    get_response = client.get(
        "/settings/ai",
        headers=authenticated_headers,
    )

    assert get_response.status_code == 200

    assert get_response.json() == {
        "ai_features_enabled": True,
        "ai_consent_accepted": True,
    }

    reset_ai_settings(authenticated_headers)


def test_disable_ai_features_revokes_consent(authenticated_headers):
    client.put(
        "/settings/ai",
        json={
            "ai_features_enabled": True,
            "ai_consent_accepted": True,
        },
        headers=authenticated_headers,
    )

    response = client.put(
        "/settings/ai",
        json={
            "ai_features_enabled": False,
            "ai_consent_accepted": False,
        },
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    assert response.json() == {
        "ai_features_enabled": False,
        "ai_consent_accepted": False,
    }


def test_enable_ai_features_without_consent_is_rejected(authenticated_headers):
    reset_ai_settings(authenticated_headers)

    response = client.put(
        "/settings/ai",
        json={
            "ai_features_enabled": True,
            "ai_consent_accepted": False,
        },
        headers=authenticated_headers,
    )

    assert response.status_code == 422


def test_consent_cannot_remain_enabled_when_ai_is_disabled(authenticated_headers):
    reset_ai_settings(authenticated_headers)

    response = client.put(
        "/settings/ai",
        json={
            "ai_features_enabled": False,
            "ai_consent_accepted": True,
        },
        headers=authenticated_headers,
    )

    assert response.status_code == 422


def test_ai_settings_reject_missing_fields(authenticated_headers):
    response = client.put(
        "/settings/ai",
        json={
            "ai_features_enabled": True,
        },
        headers=authenticated_headers,
    )

    assert response.status_code == 422


def test_ai_settings_response_contains_expected_fields_only(authenticated_headers):
    response = client.get(
        "/settings/ai",
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    assert set(
        response.json().keys()
    ) == {
        "ai_features_enabled",
        "ai_consent_accepted",
    }


def test_ai_settings_are_isolated_between_users(
    authenticated_headers,
):
    from app.auth.models import User
    from app.auth.service import hash_password
    from app.core.database import SessionLocal
    from uuid import uuid4

    enable_response = client.put(
        "/settings/ai",
        json={
            "ai_features_enabled": True,
            "ai_consent_accepted": True,
        },
        headers=authenticated_headers,
    )

    assert enable_response.status_code == 200

    email = f"isolation-ai-settings-{uuid4()}@career-os.local"
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

    other_headers = {
        "Authorization": f"Bearer {access_token}",
    }

    other_ai_settings_response = client.get(
        "/settings/ai",
        headers=other_headers,
    )

    assert other_ai_settings_response.status_code == 200

    other_ai_settings = other_ai_settings_response.json()

    assert other_ai_settings["ai_features_enabled"] is False
    assert other_ai_settings["ai_consent_accepted"] is False

    reset_ai_settings(authenticated_headers)


def test_job_discovery_settings_are_isolated_between_users(
    authenticated_headers,
):
    from app.auth.models import User
    from app.auth.service import hash_password
    from app.core.database import SessionLocal
    from uuid import uuid4

    update_response = client.put(
        "/settings/job-discovery",
        json={
            "discovery_enabled": True,
            "discovery_interval_minutes": 60,
            "discovery_connectors": ["france_travail"],
        },
        headers=authenticated_headers,
    )

    assert update_response.status_code == 200

    email = f"isolation-job-discovery-{uuid4()}@career-os.local"
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

    other_headers = {
        "Authorization": f"Bearer {access_token}",
    }

    other_settings_response = client.get(
        "/settings/job-discovery",
        headers=other_headers,
    )

    assert other_settings_response.status_code == 200

    other_settings = other_settings_response.json()

    assert other_settings["discovery_enabled"] is False
    assert other_settings["discovery_interval_minutes"] == 1440
    assert other_settings["discovery_connectors"] == []

def test_get_linkedin_email_settings_returns_not_configured_by_default(
    authenticated_headers,
):
    response = client.get(
        "/settings/linkedin-email",
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert "imap_host" in data
    assert "imap_port" in data
    assert "email_address" in data
    assert "folder" in data
    assert "is_configured" in data

    # app_password must never be exposed, in any form, encrypted or not
    assert "app_password" not in data
    assert "app_password_encrypted" not in data


def test_update_linkedin_email_settings(authenticated_headers):
    response = client.put(
        "/settings/linkedin-email",
        json={
            "imap_host": "imap.gmail.com",
            "imap_port": 993,
            "email_address": "jobs-alerts@example.com",
            "app_password": "fake-app-password-not-real",
            "folder": "INBOX",
        },
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["imap_host"] == "imap.gmail.com"
    assert data["imap_port"] == 993
    assert data["email_address"] == "jobs-alerts@example.com"
    assert data["folder"] == "INBOX"
    assert data["is_configured"] is True

    # the password itself must never come back, in any form
    assert "app_password" not in data
    assert "app_password_encrypted" not in data


def test_linkedin_email_settings_never_expose_password_after_update(
    authenticated_headers,
):
    update_response = client.put(
        "/settings/linkedin-email",
        json={
            "imap_host": "imap.gmail.com",
            "imap_port": 993,
            "email_address": "jobs-alerts@example.com",
            "app_password": "fake-app-password-not-real",
            "folder": "INBOX",
        },
        headers=authenticated_headers,
    )

    assert update_response.status_code == 200

    get_response = client.get(
        "/settings/linkedin-email",
        headers=authenticated_headers,
    )

    assert get_response.status_code == 200

    data = get_response.json()

    assert data["is_configured"] is True
    assert "app_password" not in data
    assert "app_password_encrypted" not in data

    response_text = get_response.text
    assert "fake-app-password-not-real" not in response_text


def test_linkedin_email_settings_are_isolated_between_users(
    authenticated_headers,
):
    from app.auth.models import User
    from app.auth.service import hash_password
    from app.core.database import SessionLocal
    from uuid import uuid4

    update_response = client.put(
        "/settings/linkedin-email",
        json={
            "imap_host": "imap.gmail.com",
            "imap_port": 993,
            "email_address": "primary-user@example.com",
            "app_password": "fake-app-password-not-real",
            "folder": "INBOX",
        },
        headers=authenticated_headers,
    )

    assert update_response.status_code == 200

    email = f"isolation-linkedin-email-{uuid4()}@career-os.local"
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

    second_access_token = login_response.json()["access_token"]

    second_headers = {
        "Authorization": f"Bearer {second_access_token}",
    }

    second_get_response = client.get(
        "/settings/linkedin-email",
        headers=second_headers,
    )

    assert second_get_response.status_code == 200

    second_data = second_get_response.json()

    assert second_data["is_configured"] is False
    assert second_data["email_address"] is None

def test_update_linkedin_email_settings_keeps_password_when_empty(
    authenticated_headers,
):
    first_update = client.put(
        "/settings/linkedin-email",
        json={
            "imap_host": "imap.gmail.com",
            "imap_port": 993,
            "email_address": "jobs-alerts@example.com",
            "app_password": "original-password",
            "folder": "INBOX",
        },
        headers=authenticated_headers,
    )

    assert first_update.status_code == 200
    assert first_update.json()["is_configured"] is True

    second_update = client.put(
        "/settings/linkedin-email",
        json={
            "imap_host": "imap.outlook.com",
            "imap_port": 993,
            "email_address": "jobs-alerts@example.com",
            "app_password": "",
            "folder": "INBOX",
        },
        headers=authenticated_headers,
    )

    assert second_update.status_code == 200

    data = second_update.json()

    assert data["imap_host"] == "imap.outlook.com"
    assert data["is_configured"] is True