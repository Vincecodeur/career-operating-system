from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken

from app.core.settings import settings


def _get_fernet() -> Fernet | None:
    """
    Returns a Fernet instance built from LINKEDIN_EMAIL_ENCRYPTION_KEY.

    Returns None if the key is absent or malformed, so callers can
    degrade gracefully (treat the secret as "not configured") instead
    of crashing the application at import time or at request time.
    """
    if not settings.LINKEDIN_EMAIL_ENCRYPTION_KEY:
        return None

    try:
        return Fernet(
            settings.LINKEDIN_EMAIL_ENCRYPTION_KEY.encode()
        )
    except (ValueError, TypeError):
        return None


def encrypt_secret(value: str) -> str | None:
    """
    Encrypts a plaintext secret for storage at rest.

    Returns None if no valid encryption key is configured, rather
    than raising - callers are expected to treat None as "cannot
    persist this secret right now" and surface that explicitly.
    """
    fernet = _get_fernet()

    if fernet is None:
        return None

    return fernet.encrypt(
        value.encode()
    ).decode()


def decrypt_secret(encrypted_value: str) -> str | None:
    """
    Decrypts a secret previously produced by encrypt_secret().

    Returns None if no valid encryption key is configured, or if the
    stored value cannot be decrypted with the current key (wrong key,
    corrupted value). Never raises to the caller.
    """
    fernet = _get_fernet()

    if fernet is None:
        return None

    try:
        return fernet.decrypt(
            encrypted_value.encode()
        ).decode()
    except InvalidToken:
        return None
