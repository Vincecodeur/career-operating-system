from cryptography.fernet import Fernet

from app.core import encryption


def test_encrypt_then_decrypt_returns_original_value(monkeypatch):
    valid_key = Fernet.generate_key().decode()

    monkeypatch.setattr(
        encryption.settings,
        "LINKEDIN_EMAIL_ENCRYPTION_KEY",
        valid_key,
    )

    original_value = "my-app-password-123"

    encrypted = encryption.encrypt_secret(original_value)

    assert encrypted is not None
    assert encrypted != original_value

    decrypted = encryption.decrypt_secret(encrypted)

    assert decrypted == original_value


def test_encrypt_secret_returns_none_without_key(monkeypatch):
    monkeypatch.setattr(
        encryption.settings,
        "LINKEDIN_EMAIL_ENCRYPTION_KEY",
        "",
    )

    result = encryption.encrypt_secret("some-secret")

    assert result is None


def test_decrypt_secret_returns_none_without_key(monkeypatch):
    monkeypatch.setattr(
        encryption.settings,
        "LINKEDIN_EMAIL_ENCRYPTION_KEY",
        "",
    )

    result = encryption.decrypt_secret("irrelevant-value")

    assert result is None


def test_decrypt_secret_returns_none_with_wrong_key(monkeypatch):
    original_key = Fernet.generate_key().decode()
    different_key = Fernet.generate_key().decode()

    monkeypatch.setattr(
        encryption.settings,
        "LINKEDIN_EMAIL_ENCRYPTION_KEY",
        original_key,
    )

    encrypted = encryption.encrypt_secret("some-secret")
    assert encrypted is not None

    monkeypatch.setattr(
        encryption.settings,
        "LINKEDIN_EMAIL_ENCRYPTION_KEY",
        different_key,
    )

    result = encryption.decrypt_secret(encrypted)

    assert result is None


def test_decrypt_secret_returns_none_with_malformed_value(monkeypatch):
    valid_key = Fernet.generate_key().decode()

    monkeypatch.setattr(
        encryption.settings,
        "LINKEDIN_EMAIL_ENCRYPTION_KEY",
        valid_key,
    )

    result = encryption.decrypt_secret("not-a-valid-fernet-token")

    assert result is None


def test_encrypt_secret_returns_none_with_malformed_key(monkeypatch):
    monkeypatch.setattr(
        encryption.settings,
        "LINKEDIN_EMAIL_ENCRYPTION_KEY",
        "not-a-valid-fernet-key",
    )

    result = encryption.encrypt_secret("some-secret")

    assert result is None
