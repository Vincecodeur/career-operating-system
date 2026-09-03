from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from jose import jwt
from sqlalchemy.orm import Session

import traceback

from app.auth.models import User
from app.auth.email_service import (
    send_password_reset_email,
)
from app.auth.schemas import (
    ForgotPasswordRequest,
)
from app.auth.schemas import (
    MessageResponse,
)
from app.auth.schemas import (
    ResetPasswordRequest,
)

from app.auth.token_service import (
    create_password_reset_token,
)
from app.auth.token_service import (
    get_valid_password_reset_token,
)
from app.auth.token_service import (
    mark_password_reset_token_as_used,
)
from app.auth.password_reset_models import (
    PasswordResetToken,
)

from app.auth.email_change_models import (
    EmailChangeRequest,
)
from app.auth.email_service import (
    send_email_change_confirmation_email,
)
from app.auth.schemas import (
    ChangeEmailRequest,
)
from app.auth.schemas import (
    ConfirmEmailChangeRequest,
)

from app.auth.schemas import (
    RegisterRequest,
)

from app.auth.password_policy import (
    get_password_policy_violations,
)

from app.core.settings import settings

from app.auth.token_service import (
    create_email_change_request,
)
from app.auth.token_service import (
    get_valid_email_change_request,
)
from app.auth.token_service import (
    mark_email_change_request_as_used,
)


from app.auth.schemas import LoginRequest
from app.auth.schemas import LoginResponse
from app.auth.schemas import UserResponse
from app.core.database import get_db
from app.auth.service import ALGORITHM
from app.auth.service import SECRET_KEY
from app.auth.service import authenticate_user
from app.auth.service import create_access_token
from app.auth.service import get_user_by_email
from app.auth.service import hash_password


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)



PASSWORD_RECOVERY_MESSAGE = (
    "If an account exists for this email, "
    "password recovery instructions have "
    "been sent."
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    payload: RegisterRequest,
    db: Session = Depends(get_db),
):
    if not settings.PUBLIC_REGISTRATION_ENABLED:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Public registration is disabled.",
        )

    if payload.password != payload.confirm_password:
        raise HTTPException(
            status_code=(
                status.HTTP_400_BAD_REQUEST
            ),
            detail=(
                "Password confirmation does "
                "not match."
            ),
        )

    password_violations = (
        get_password_policy_violations(
            payload.password
        )
    )

    if payload.password != payload.confirm_password:
        raise HTTPException(
            status_code=(
                status.HTTP_400_BAD_REQUEST
            ),
            detail=(
                "Password confirmation does "
                "not match."
            ),
    )

    password_violations = (
        get_password_policy_violations(
            payload.password
        )
    )

    if password_violations:
        raise HTTPException(
            status_code=(
                status.HTTP_400_BAD_REQUEST
            ),
            detail=(
                "Password must contain "
                + ", ".join(password_violations)
                + "."
            ),
        )

    

    existing_user = get_user_by_email(
        db=db,
        email=payload.email,
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists.",
        )

    user = User(
        email=payload.email,
        hashed_password=hash_password(payload.password),
        is_active=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.post(
    "/login",
    response_model=LoginResponse,
)
def login(
    payload: LoginRequest,
    db: Session = Depends(get_db),
):
    user = authenticate_user(
        db=db,
        email=payload.email,
        password=payload.password,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            headers={
                "WWW-Authenticate": "Bearer",
            },
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive.",
        )

    access_token = create_access_token(
        subject=user.email,
    )

    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user=user,
    )

@router.post(
    "/forgot-password",
    response_model=MessageResponse,
)
def forgot_password(
    payload: ForgotPasswordRequest,
    db: Session = Depends(get_db),
):
    user = get_user_by_email(
        db=db,
        email=payload.email,
    )

    if user is None or not user.is_active:
        return MessageResponse(
            message=PASSWORD_RECOVERY_MESSAGE,
        )

    token_record, raw_token = (
        create_password_reset_token(
            db=db,
            user=user,
        )
    )

    try:
        send_password_reset_email(
            recipient_email=user.email,
            reset_token=raw_token,
        )
 
    except Exception:
        traceback.print_exc()

        db.query(
            PasswordResetToken
        ).filter(
            PasswordResetToken.id
            == token_record.id
        ).delete(
            synchronize_session=False
        )

        db.commit()

    return MessageResponse(
        message=PASSWORD_RECOVERY_MESSAGE,
    )


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={
            "WWW-Authenticate": "Bearer",
        },
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        email = payload.get("sub")

        if email is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = get_user_by_email(
        db=db,
        email=email,
    )

    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive.",
        )

    return user


@router.post(
    "/reset-password",
    response_model=MessageResponse,
)
def reset_password(
    payload: ResetPasswordRequest,
    db: Session = Depends(get_db),
):
    if (
        payload.new_password
        != payload.confirm_password
    ):
        raise HTTPException(
            status_code=(
                status.HTTP_400_BAD_REQUEST
            ),
            detail=(
                "Password confirmation does "
                "not match."
            ),
        )

    password_violations = (
        get_password_policy_violations(
            payload.new_password
        )
    )

    if password_violations:
        raise HTTPException(
            status_code=(
                status.HTTP_400_BAD_REQUEST
            ),
            detail=(
                "Password must contain "
                + ", ".join(password_violations)
                + "."
            ),
        )

    token_record = (
        get_valid_password_reset_token(
            db=db,
            raw_token=payload.token,
        )
    )

    if token_record is None:
        raise HTTPException(
            status_code=(
                status.HTTP_400_BAD_REQUEST
            ),
            detail=(
                "Password reset token is "
                "invalid or expired."
            ),
        )

    user = (
        db.query(User)
        .filter(
            User.id
            == token_record.user_id
        )
        .first()
    )

    if user is None or not user.is_active:
        raise HTTPException(
            status_code=(
                status.HTTP_400_BAD_REQUEST
            ),
            detail=(
                "Password reset token is "
                "invalid or expired."
            ),
        )

    user.hashed_password = hash_password(
        payload.new_password
    )

    mark_password_reset_token_as_used(
        db=db,
        token_record=token_record,
    )

    db.add(user)
    db.commit()

    return MessageResponse(
        message=(
            "Password has been reset "
            "successfully."
        ),
    )

@router.post(
    "/change-email",
    response_model=MessageResponse,
)
def change_email(
    payload: ChangeEmailRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    existing_user = get_user_by_email(
        db=db,
        email=payload.new_email,
    )

    if existing_user is not None:
        raise HTTPException(
            status_code=(
                status.HTTP_400_BAD_REQUEST
            ),
            detail=(
                "This email address is already "
                "in use."
            ),
        )

    request_record, raw_token = (
        create_email_change_request(
            db=db,
            user=current_user,
            new_email=payload.new_email,
        )
    )

    try:
        send_email_change_confirmation_email(
            recipient_email=current_user.email,
            new_email=payload.new_email,
            confirmation_token=raw_token,
        )
    except Exception:
        traceback.print_exc()

        db.query(
            EmailChangeRequest
        ).filter(
            EmailChangeRequest.id
            == request_record.id
        ).delete(
            synchronize_session=False
        )

        db.commit()

        raise HTTPException(
            status_code=(
                status.HTTP_500_INTERNAL_SERVER_ERROR
            ),
            detail=(
                "Unable to send email change "
                "confirmation."
            ),
        )

    return MessageResponse(
        message=(
            "A confirmation link has been sent "
            "to your current email address."
        ),
    )


@router.post(
    "/change-email/confirm",
    response_model=MessageResponse,
)
def confirm_email_change(
    payload: ConfirmEmailChangeRequest,
    db: Session = Depends(get_db),
):
    request_record = (
        get_valid_email_change_request(
            db=db,
            raw_token=payload.token,
        )
    )

    if request_record is None:
        raise HTTPException(
            status_code=(
                status.HTTP_400_BAD_REQUEST
            ),
            detail=(
                "Email change link is invalid "
                "or expired."
            ),
        )

    existing_user = get_user_by_email(
        db=db,
        email=request_record.new_email,
    )

    if existing_user is not None:
        raise HTTPException(
            status_code=(
                status.HTTP_400_BAD_REQUEST
            ),
            detail=(
                "This email address is already "
                "in use."
            ),
        )

    user = (
        db.query(User)
        .filter(
            User.id
            == request_record.user_id
        )
        .first()
    )

    if user is None or not user.is_active:
        raise HTTPException(
            status_code=(
                status.HTTP_400_BAD_REQUEST
            ),
            detail=(
                "Email change link is invalid "
                "or expired."
            ),
        )

    user.email = request_record.new_email

    mark_email_change_request_as_used(
        db=db,
        request_record=request_record,
    )

    db.add(user)
    db.commit()

    return MessageResponse(
        message=(
            "Your email address has been "
            "updated successfully."
        ),
    )

@router.get(
    "/me",
    response_model=UserResponse,
)
def read_current_user(
    current_user: User = Depends(get_current_user),
):
    return current_user