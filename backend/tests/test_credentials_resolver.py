from uuid import uuid4

from app.auth.models import User
from app.core.database import SessionLocal
from app.core.encryption import encrypt_secret
from app.jobs.connectors.credentials_resolver import (
    CREDENTIAL_RESOLVERS,
    resolve_linkedin_email_credentials,
)
from app.settings.service import SettingsService


def get_primary_test_user_id(db) -> int:
    user = db.query(User).filter(
        User.email == "test-primary-user@career-os.local"
    ).first()

    return user.id


def test_credential_resolvers_contains_linkedin_email():
    assert "linkedin_email" in CREDENTIAL_RESOLVERS
    assert (
        CREDENTIAL_RESOLVERS["linkedin_email"]
        is resolve_linkedin_email_credentials
    )


def test_resolve_linkedin_email_credentials_returns_none_when_not_configured():
    db = SessionLocal()

    try:
        user_id = get_primary_test_user_id(db)

        from app.settings.models import UserSettings

        settings_service = SettingsService(db)
        settings_service._get_or_create_user_settings(user_id)

        user_settings = db.query(UserSettings).filter(
            UserSettings.user_id == user_id
        ).first()

        user_settings.linkedin_email_app_password_encrypted = None
        db.commit()

        credentials = resolve_linkedin_email_credentials(
            db, user_id
        )

        assert credentials is None
    finally:
        db.rollback()
        db.close()


def test_resolve_linkedin_email_credentials_returns_decrypted_values():
    db = SessionLocal()

    try:
        user_id = get_primary_test_user_id(db)

        settings_service = SettingsService(db)
        settings_service.update_linkedin_email_settings(
            user_id,
            {
                "imap_host": "imap.example.test",
                "imap_port": 993,
                "email_address": "jobs-alerts@example.test",
                "app_password": "fake-app-password-not-real",
                "folder": "INBOX",
            },
        )

        credentials = resolve_linkedin_email_credentials(
            db, user_id
        )

        assert credentials is not None
        assert credentials["imap_host"] == "imap.example.test"
        assert credentials["imap_port"] == 993
        assert (
            credentials["email_address"]
            == "jobs-alerts@example.test"
        )
        assert (
            credentials["app_password"]
            == "fake-app-password-not-real"
        )
        assert credentials["folder"] == "INBOX"
    finally:
        db.rollback()

        from app.settings.models import UserSettings

        user_settings = db.query(UserSettings).filter(
            UserSettings.user_id == user_id
        ).first()
        if user_settings is not None:
            user_settings.linkedin_email_app_password_encrypted = None
            db.commit()

        db.close()


def test_resolve_linkedin_email_credentials_returns_none_on_undecryptable_value():
    db = SessionLocal()

    try:
        user_id = get_primary_test_user_id(db)

        from app.settings.models import UserSettings

        user_settings = db.query(UserSettings).filter(
            UserSettings.user_id == user_id
        ).first()

        if user_settings is None:
            settings_service = SettingsService(db)
            settings_service._get_or_create_user_settings(user_id)
            user_settings = db.query(UserSettings).filter(
                UserSettings.user_id == user_id
            ).first()

        user_settings.linkedin_email_imap_host = "imap.example.test"
        user_settings.linkedin_email_imap_port = 993
        user_settings.linkedin_email_address = (
            "jobs-alerts@example.test"
        )
        user_settings.linkedin_email_app_password_encrypted = (
            "not-a-valid-fernet-token"
        )
        db.commit()

        credentials = resolve_linkedin_email_credentials(
            db, user_id
        )

        assert credentials is None
    finally:
        db.rollback()

        from app.settings.models import UserSettings

        user_settings = db.query(UserSettings).filter(
            UserSettings.user_id == user_id
        ).first()
        if user_settings is not None:
            user_settings.linkedin_email_app_password_encrypted = None
            db.commit()

        db.close()
