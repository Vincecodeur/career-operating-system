from datetime import datetime
from datetime import timedelta
from datetime import timezone

from fastapi.testclient import TestClient

from app.auth.models import User
from app.auth.password_reset_models import (
    PasswordResetToken,
)
from app.auth.service import hash_password
from app.auth.service import verify_password
from app.auth.token_service import (
    create_password_reset_token,
)
from app.auth.token_service import (
    hash_password_reset_token,
)
from app.core.database import SessionLocal
from app.main import app


client = TestClient(app)


def create_test_user(
    email: str,
    password: str = "Password123!",
) -> User:
    db = SessionLocal()

    try:
        existing_user = (
            db.query(User)
            .filter(
                User.email == email
            )
            .first()
        )

        if existing_user is not None:
            db.query(
                PasswordResetToken
            ).filter(
                PasswordResetToken.user_id
                == existing_user.id
            ).delete(
                synchronize_session=False
            )

            db.delete(existing_user)
            db.commit()

        user = User(
            email=email,
            hashed_password=hash_password(
                password
            ),
            is_active=True,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user
    finally:
        db.close()


def test_register_is_disabled():
    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "Password123!",
        },
    )

    assert response.status_code == 403

    data = response.json()

    assert (
        data["detail"]
        == "Public registration is disabled."
    )


def test_login_with_unknown_user():
    response = client.post(
        "/auth/login",
        json={
            "email": "unknown@example.com",
            "password": "Password123!",
        },
    )

    assert response.status_code == 401

    data = response.json()

    assert (
        data["detail"]
        == "Invalid email or password."
    )


def test_me_without_token():
    response = client.get(
        "/auth/me",
    )

    assert response.status_code == 401


def test_forgot_password_unknown_user_returns_generic_response(
    monkeypatch,
):
    email_sent = False

    def fake_send_password_reset_email(
        recipient_email: str,
        reset_token: str,
    ) -> None:
        nonlocal email_sent
        email_sent = True

    monkeypatch.setattr(
        "app.auth.router.send_password_reset_email",
        fake_send_password_reset_email,
    )

    response = client.post(
        "/auth/forgot-password",
        json={
            "email": (
                "unknown-password-reset"
                "@example.com"
            ),
        },
    )

    assert response.status_code == 200

    assert response.json() == {
        "message": (
            "If an account exists for this "
            "email, password recovery "
            "instructions have been sent."
        )
    }

    assert email_sent is False


def test_forgot_password_existing_user_creates_token_and_sends_email(
    monkeypatch,
):
    user = create_test_user(
        "password-reset-request@example.com"
    )

    sent_email: dict[str, str] = {}

    def fake_send_password_reset_email(
        recipient_email: str,
        reset_token: str,
    ) -> None:
        sent_email["recipient_email"] = (
            recipient_email
        )
        sent_email["reset_token"] = (
            reset_token
        )

    monkeypatch.setattr(
        "app.auth.router.send_password_reset_email",
        fake_send_password_reset_email,
    )

    response = client.post(
        "/auth/forgot-password",
        json={
            "email": user.email,
        },
    )

    assert response.status_code == 200

    assert (
        sent_email["recipient_email"]
        == user.email
    )

    assert sent_email["reset_token"]

    db = SessionLocal()

    try:
        token_record = (
            db.query(PasswordResetToken)
            .filter(
                PasswordResetToken.user_id
                == user.id
            )
            .first()
        )

        assert token_record is not None

        assert token_record.token_hash == (
            hash_password_reset_token(
                sent_email["reset_token"]
            )
        )

        assert (
            token_record.token_hash
            != sent_email["reset_token"]
        )

        assert token_record.used_at is None
    finally:
        db.close()


def test_reset_password_rejects_password_mismatch():
    response = client.post(
        "/auth/reset-password",
        json={
            "token": "invalid-token",
            "new_password": (
                "NewPassword123!"
            ),
            "confirm_password": (
                "DifferentPassword123!"
            ),
        },
    )

    assert response.status_code == 400

    assert response.json()["detail"] == (
        "Password confirmation does not "
        "match."
    )


def test_reset_password_rejects_invalid_token():
    response = client.post(
        "/auth/reset-password",
        json={
            "token": "invalid-token",
            "new_password": (
                "NewPassword123!"
            ),
            "confirm_password": (
                "NewPassword123!"
            ),
        },
    )

    assert response.status_code == 400

    assert response.json()["detail"] == (
        "Password reset token is invalid "
        "or expired."
    )


def test_reset_password_rejects_expired_token():
    user = create_test_user(
        "expired-reset-token@example.com"
    )

    raw_token = "expired-reset-token"

    db = SessionLocal()

    try:
        token_record = PasswordResetToken(
            user_id=user.id,
            token_hash=(
                hash_password_reset_token(
                    raw_token
                )
            ),
            expires_at=(
                datetime.now(timezone.utc)
                - timedelta(minutes=1)
            ),
        )

        db.add(token_record)
        db.commit()
    finally:
        db.close()

    response = client.post(
        "/auth/reset-password",
        json={
            "token": raw_token,
            "new_password": (
                "NewPassword123!"
            ),
            "confirm_password": (
                "NewPassword123!"
            ),
        },
    )

    assert response.status_code == 400

    assert response.json()["detail"] == (
        "Password reset token is invalid "
        "or expired."
    )


def test_reset_password_rejects_used_token():
    user = create_test_user(
        "used-reset-token@example.com"
    )

    raw_token = "used-reset-token"

    db = SessionLocal()

    try:
        token_record = PasswordResetToken(
            user_id=user.id,
            token_hash=(
                hash_password_reset_token(
                    raw_token
                )
            ),
            expires_at=(
                datetime.now(timezone.utc)
                + timedelta(minutes=60)
            ),
            used_at=datetime.now(
                timezone.utc
            ),
        )

        db.add(token_record)
        db.commit()
    finally:
        db.close()

    response = client.post(
        "/auth/reset-password",
        json={
            "token": raw_token,
            "new_password": (
                "NewPassword123!"
            ),
            "confirm_password": (
                "NewPassword123!"
            ),
        },
    )

    assert response.status_code == 400


def test_reset_password_success():
    old_password = "OldPassword123!"
    new_password = "NewPassword123!"

    user = create_test_user(
        "successful-password-reset@example.com",
        old_password,
    )

    db = SessionLocal()

    try:
        _, raw_token = (
            create_password_reset_token(
                db=db,
                user=user,
            )
        )
    finally:
        db.close()

    response = client.post(
        "/auth/reset-password",
        json={
            "token": raw_token,
            "new_password": new_password,
            "confirm_password": new_password,
        },
    )

    assert response.status_code == 200

    assert response.json() == {
        "message": (
            "Password has been reset "
            "successfully."
        )
    }

    db = SessionLocal()

    try:
        updated_user = (
            db.query(User)
            .filter(
                User.id == user.id
            )
            .first()
        )

        assert updated_user is not None

        assert verify_password(
            new_password,
            updated_user.hashed_password,
        )

        assert not verify_password(
            old_password,
            updated_user.hashed_password,
        )

        token_record = (
            db.query(PasswordResetToken)
            .filter(
                PasswordResetToken.user_id
                == user.id
            )
            .first()
        )

        assert token_record is not None
        assert token_record.used_at is not None
    finally:
        db.close()


def test_successful_token_cannot_be_reused():
    user = create_test_user(
        "reused-reset-token@example.com"
    )

    db = SessionLocal()

    try:
        _, raw_token = (
            create_password_reset_token(
                db=db,
                user=user,
            )
        )
    finally:
        db.close()

    payload = {
        "token": raw_token,
        "new_password": "NewPassword123!",
        "confirm_password": (
            "NewPassword123!"
        ),
    }

    first_response = client.post(
        "/auth/reset-password",
        json=payload,
    )

    second_response = client.post(
        "/auth/reset-password",
        json=payload,
    )

    assert first_response.status_code == 200
    assert second_response.status_code == 400


def test_login_works_with_new_password():
    old_password = "OldPassword123!"
    new_password = "NewPassword123!"
    email = "login-after-reset@example.com"

    user = create_test_user(
        email,
        old_password,
    )

    db = SessionLocal()

    try:
        _, raw_token = (
            create_password_reset_token(
                db=db,
                user=user,
            )
        )
    finally:
        db.close()

    reset_response = client.post(
        "/auth/reset-password",
        json={
            "token": raw_token,
            "new_password": new_password,
            "confirm_password": new_password,
        },
    )

    assert reset_response.status_code == 200

    old_login_response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": old_password,
        },
    )

    new_login_response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": new_password,
        },
    )

    assert old_login_response.status_code == 401
    assert new_login_response.status_code == 200
    
from app.auth.email_change_models import (
    EmailChangeRequest,
)


def get_auth_headers_for_user(
    user: User,
    password: str,
) -> dict[str, str]:
    login_response = client.post(
        "/auth/login",
        json={
            "email": user.email,
            "password": password,
        },
    )

    access_token = login_response.json()[
        "access_token"
    ]

    return {
        "Authorization": f"Bearer {access_token}",
    }


def test_change_email_requires_authentication():
    response = client.post(
        "/auth/change-email",
        json={
            "new_email": "new-address@example.com",
        },
    )

    assert response.status_code == 401


def test_change_email_rejects_existing_email(
    monkeypatch,
):
    password = "Password123!"

    existing_user = create_test_user(
        "existing-user@example.com",
        password,
    )

    requesting_user = create_test_user(
        "requesting-user@example.com",
        password,
    )

    headers = get_auth_headers_for_user(
        requesting_user,
        password,
    )

    def fake_send_email_change_confirmation_email(
        recipient_email: str,
        new_email: str,
        confirmation_token: str,
    ) -> None:
        pass

    monkeypatch.setattr(
        "app.auth.router.send_email_change_confirmation_email",
        fake_send_email_change_confirmation_email,
    )

    response = client.post(
        "/auth/change-email",
        json={
            "new_email": existing_user.email,
        },
        headers=headers,
    )

    assert response.status_code == 400


def test_change_email_creates_request_and_sends_confirmation(
    monkeypatch,
):
    password = "Password123!"

    user = create_test_user(
        "current-email@example.com",
        password,
    )

    headers = get_auth_headers_for_user(
        user,
        password,
    )

    sent_email: dict[str, str] = {}

    def fake_send_email_change_confirmation_email(
        recipient_email: str,
        new_email: str,
        confirmation_token: str,
    ) -> None:
        sent_email["recipient_email"] = (
            recipient_email
        )
        sent_email["new_email"] = new_email
        sent_email["confirmation_token"] = (
            confirmation_token
        )

    monkeypatch.setattr(
        "app.auth.router.send_email_change_confirmation_email",
        fake_send_email_change_confirmation_email,
    )

    response = client.post(
        "/auth/change-email",
        json={
            "new_email": "new-email@example.com",
        },
        headers=headers,
    )

    assert response.status_code == 200

    assert (
        sent_email["recipient_email"]
        == user.email
    )
    assert (
        sent_email["new_email"]
        == "new-email@example.com"
    )
    assert sent_email["confirmation_token"]

    db = SessionLocal()

    try:
        request_record = (
            db.query(EmailChangeRequest)
            .filter(
                EmailChangeRequest.user_id
                == user.id
            )
            .first()
        )

        assert request_record is not None
        assert (
            request_record.new_email
            == "new-email@example.com"
        )
        assert (
            request_record.token_hash
            == hash_password_reset_token(
                sent_email["confirmation_token"]
            )
        )
        assert request_record.used_at is None
    finally:
        db.close()


def test_confirm_email_change_rejects_invalid_token():
    response = client.post(
        "/auth/change-email/confirm",
        json={
            "token": "invalid-token",
        },
    )

    assert response.status_code == 400


def test_confirm_email_change_success(
    monkeypatch,
):
    password = "Password123!"

    user = create_test_user(
        "before-change@example.com",
        password,
    )

    headers = get_auth_headers_for_user(
        user,
        password,
    )

    sent_email: dict[str, str] = {}

    def fake_send_email_change_confirmation_email(
        recipient_email: str,
        new_email: str,
        confirmation_token: str,
    ) -> None:
        sent_email["confirmation_token"] = (
            confirmation_token
        )

    monkeypatch.setattr(
        "app.auth.router.send_email_change_confirmation_email",
        fake_send_email_change_confirmation_email,
    )

    client.post(
        "/auth/change-email",
        json={
            "new_email": "after-change@example.com",
        },
        headers=headers,
    )

    confirm_response = client.post(
        "/auth/change-email/confirm",
        json={
            "token": sent_email[
                "confirmation_token"
            ],
        },
    )

    assert confirm_response.status_code == 200

    db = SessionLocal()

    try:
        updated_user = (
            db.query(User)
            .filter(User.id == user.id)
            .first()
        )

        assert (
            updated_user.email
            == "after-change@example.com"
        )
    finally:
        db.close()

    old_login_response = client.post(
        "/auth/login",
        json={
            "email": "before-change@example.com",
            "password": password,
        },
    )

    new_login_response = client.post(
        "/auth/login",
        json={
            "email": "after-change@example.com",
            "password": password,
        },
    )

    assert old_login_response.status_code == 401
    assert new_login_response.status_code == 200


def test_confirm_email_change_token_cannot_be_reused(
    monkeypatch,
):
    password = "Password123!"

    user = create_test_user(
        "reuse-email-token@example.com",
        password,
    )

    headers = get_auth_headers_for_user(
        user,
        password,
    )

    sent_email: dict[str, str] = {}

    def fake_send_email_change_confirmation_email(
        recipient_email: str,
        new_email: str,
        confirmation_token: str,
    ) -> None:
        sent_email["confirmation_token"] = (
            confirmation_token
        )

    monkeypatch.setattr(
        "app.auth.router.send_email_change_confirmation_email",
        fake_send_email_change_confirmation_email,
    )

    client.post(
        "/auth/change-email",
        json={
            "new_email": "reused-target@example.com",
        },
        headers=headers,
    )

    payload = {
        "token": sent_email[
            "confirmation_token"
        ],
    }

    first_response = client.post(
        "/auth/change-email/confirm",
        json=payload,
    )

    second_response = client.post(
        "/auth/change-email/confirm",
        json=payload,
    )

    assert first_response.status_code == 200
    assert second_response.status_code == 400