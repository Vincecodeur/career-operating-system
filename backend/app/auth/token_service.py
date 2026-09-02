import hashlib
import secrets
from datetime import datetime
from datetime import timedelta
from datetime import timezone

from sqlalchemy.orm import Session

from app.auth.models import User
from app.auth.password_reset_models import (
    PasswordResetToken,
)
from app.auth.email_change_models import (
    EmailChangeRequest,
)

from app.core.settings import settings


def generate_password_reset_token() -> str:
    return secrets.token_urlsafe(32)


def hash_password_reset_token(
    token: str,
) -> str:
    return hashlib.sha256(
        token.encode("utf-8")
    ).hexdigest()


def invalidate_existing_password_reset_tokens(
    db: Session,
    user_id: int,
) -> None:
    now = datetime.now(timezone.utc)

    existing_tokens = (
        db.query(PasswordResetToken)
        .filter(
            PasswordResetToken.user_id
            == user_id,
            PasswordResetToken.used_at.is_(
                None
            ),
        )
        .all()
    )

    for existing_token in existing_tokens:
        existing_token.used_at = now


def create_password_reset_token(
    db: Session,
    user: User,
) -> tuple[PasswordResetToken, str]:
    invalidate_existing_password_reset_tokens(
        db=db,
        user_id=user.id,
    )

    raw_token = (
        generate_password_reset_token()
    )

    token_record = PasswordResetToken(
        user_id=user.id,
        token_hash=hash_password_reset_token(
            raw_token
        ),
        expires_at=(
            datetime.now(timezone.utc)
            + timedelta(
                minutes=(
                    settings
                    .PASSWORD_RESET_TOKEN_EXPIRE_MINUTES
                )
            )
        ),
    )

    db.add(token_record)
    db.commit()
    db.refresh(token_record)

    return (
        token_record,
        raw_token,
    )


def get_valid_password_reset_token(
    db: Session,
    raw_token: str,
) -> PasswordResetToken | None:
    token_hash = hash_password_reset_token(
        raw_token
    )

    token_record = (
        db.query(PasswordResetToken)
        .filter(
            PasswordResetToken.token_hash
            == token_hash
        )
        .first()
    )

    if token_record is None:
        return None

    if token_record.used_at is not None:
        return None

    now = datetime.now(timezone.utc)

    expires_at = token_record.expires_at

    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(
            tzinfo=timezone.utc
        )

    if expires_at <= now:
        return None

    return token_record


def mark_password_reset_token_as_used(
    db: Session,
    token_record: PasswordResetToken,
) -> None:
    token_record.used_at = datetime.now(
        timezone.utc
    )

    db.add(token_record)
    
def create_email_change_request(
    db: Session,
    user: User,
    new_email: str,
) -> tuple[EmailChangeRequest, str]:
    now = datetime.now(timezone.utc)

    existing_requests = (
        db.query(EmailChangeRequest)
        .filter(
            EmailChangeRequest.user_id
            == user.id,
            EmailChangeRequest.used_at.is_(
                None
            ),
        )
        .all()
    )

    for existing_request in existing_requests:
        existing_request.used_at = now

    raw_token = (
        generate_password_reset_token()
    )

    request_record = EmailChangeRequest(
        user_id=user.id,
        new_email=new_email,
        token_hash=hash_password_reset_token(
            raw_token
        ),
        expires_at=(
            datetime.now(timezone.utc)
            + timedelta(
                minutes=(
                    settings
                    .EMAIL_CHANGE_TOKEN_EXPIRE_MINUTES
                )
            )
        ),
    )

    db.add(request_record)
    db.commit()
    db.refresh(request_record)

    return (
        request_record,
        raw_token,
    )


def get_valid_email_change_request(
    db: Session,
    raw_token: str,
) -> EmailChangeRequest | None:
    token_hash = hash_password_reset_token(
        raw_token
    )

    request_record = (
        db.query(EmailChangeRequest)
        .filter(
            EmailChangeRequest.token_hash
            == token_hash
        )
        .first()
    )

    if request_record is None:
        return None

    if request_record.used_at is not None:
        return None

    now = datetime.now(timezone.utc)

    expires_at = request_record.expires_at

    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(
            tzinfo=timezone.utc
        )

    if expires_at <= now:
        return None

    return request_record


def mark_email_change_request_as_used(
    db: Session,
    request_record: EmailChangeRequest,
) -> None:
    request_record.used_at = datetime.now(
        timezone.utc
    )

    db.add(request_record)