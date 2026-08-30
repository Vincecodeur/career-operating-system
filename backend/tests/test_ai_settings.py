from fastapi.testclient import TestClient

from app.core.database import SessionLocal
from app.main import app
from app.settings.models import ApplicationSetting


client = TestClient(app)


AI_SETTING_KEYS = [
    "ai_features_enabled",
    "ai_consent_accepted",
]


def delete_ai_settings() -> None:
    db = SessionLocal()

    try:
        (
            db.query(ApplicationSetting)
            .filter(
                ApplicationSetting.setting_key.in_(
                    AI_SETTING_KEYS
                )
            )
            .delete(
                synchronize_session=False
            )
        )

        db.commit()
    finally:
        db.close()


def set_disabled_ai_settings() -> None:
    response = client.put(
        "/settings/ai",
        json={
            "ai_features_enabled": False,
            "ai_consent_accepted": False,
        },
    )

    assert response.status_code == 200


def setup_function():
    delete_ai_settings()


def teardown_function():
    delete_ai_settings()


def test_get_ai_settings_returns_disabled_defaults():
    response = client.get(
        "/settings/ai"
    )

    assert response.status_code == 200

    assert response.json() == {
        "ai_features_enabled": False,
        "ai_consent_accepted": False,
    }


def test_enable_ai_features_with_consent():
    response = client.put(
        "/settings/ai",
        json={
            "ai_features_enabled": True,
            "ai_consent_accepted": True,
        },
    )

    assert response.status_code == 200

    assert response.json() == {
        "ai_features_enabled": True,
        "ai_consent_accepted": True,
    }


def test_enabled_ai_settings_are_persisted():
    update_response = client.put(
        "/settings/ai",
        json={
            "ai_features_enabled": True,
            "ai_consent_accepted": True,
        },
    )

    assert update_response.status_code == 200

    get_response = client.get(
        "/settings/ai"
    )

    assert get_response.status_code == 200

    assert get_response.json() == {
        "ai_features_enabled": True,
        "ai_consent_accepted": True,
    }


def test_disable_ai_features_revokes_consent():
    client.put(
        "/settings/ai",
        json={
            "ai_features_enabled": True,
            "ai_consent_accepted": True,
        },
    )

    response = client.put(
        "/settings/ai",
        json={
            "ai_features_enabled": False,
            "ai_consent_accepted": False,
        },
    )

    assert response.status_code == 200

    assert response.json() == {
        "ai_features_enabled": False,
        "ai_consent_accepted": False,
    }


def test_enable_ai_features_without_consent_is_rejected():
    set_disabled_ai_settings()

    response = client.put(
        "/settings/ai",
        json={
            "ai_features_enabled": True,
            "ai_consent_accepted": False,
        },
    )

    assert response.status_code == 422


def test_consent_cannot_remain_enabled_when_ai_is_disabled():
    set_disabled_ai_settings()

    response = client.put(
        "/settings/ai",
        json={
            "ai_features_enabled": False,
            "ai_consent_accepted": True,
        },
    )

    assert response.status_code == 422


def test_ai_settings_reject_missing_fields():
    response = client.put(
        "/settings/ai",
        json={
            "ai_features_enabled": True,
        },
    )

    assert response.status_code == 422


def test_ai_settings_response_contains_expected_fields_only():
    response = client.get(
        "/settings/ai"
    )

    assert response.status_code == 200

    assert set(
        response.json().keys()
    ) == {
        "ai_features_enabled",
        "ai_consent_accepted",
    }