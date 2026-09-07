from sqlalchemy.orm import Session

from app.core.encryption import decrypt_secret
from app.settings.service import SettingsService


def resolve_linkedin_email_credentials(
    db: Session,
    user_id: int,
) -> dict | None:
    """
    Resolves the credentials LinkedInEmailConnector needs from
    UserSettings, decrypting the stored app password.

    Returns None if the connector is not configured for this user
    (no password stored) or if decryption fails (missing/invalid
    LINKEDIN_EMAIL_ENCRYPTION_KEY, or a value that cannot be
    decrypted with the current key) - in both cases the connector
    must be skipped rather than instantiated with incomplete or
    unusable credentials.
    """
    settings_service = SettingsService(db)

    linkedin_settings = settings_service.get_linkedin_email_settings(
        user_id
    )

    if not linkedin_settings["is_configured"]:
        return None

    decrypted_password = decrypt_secret(
        linkedin_settings["app_password_encrypted"]
    )

    if decrypted_password is None:
        return None

    return {
        "imap_host": linkedin_settings["imap_host"],
        "imap_port": linkedin_settings["imap_port"],
        "email_address": linkedin_settings["email_address"],
        "app_password": decrypted_password,
        "folder": linkedin_settings["folder"],
    }


CREDENTIAL_RESOLVERS = {
    "linkedin_email": resolve_linkedin_email_credentials,
}
