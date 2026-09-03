from datetime import datetime
from datetime import timedelta
from datetime import timezone

from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.auth.models import User

SECRET_KEY = "CHANGE_ME_BEFORE_PRODUCTION"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
REMEMBER_ME_TOKEN_EXPIRE_MINUTES = 60 * 24 * 30

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    return pwd_context.verify(
        plain_password,
        hashed_password,
    )


def get_user_by_email(
    db: Session,
    email: str,
) -> User | None:
    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )


def authenticate_user(
    db: Session,
    email: str,
    password: str,
) -> User | None:
    user = get_user_by_email(
        db,
        email,
    )

    if not user:
        return None

    if not verify_password(
        password,
        user.hashed_password,
    ):
        return None

    return user


def create_access_token(
    subject: str,
    remember_me: bool = False,
) -> str:
    expire_minutes = (
        REMEMBER_ME_TOKEN_EXPIRE_MINUTES
        if remember_me
        else ACCESS_TOKEN_EXPIRE_MINUTES
    )

    expire = (
        datetime.now(timezone.utc)
        + timedelta(
            minutes=expire_minutes
        )
    )

    payload = {
        "sub": subject,
        "exp": expire,
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )