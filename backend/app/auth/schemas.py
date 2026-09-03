from pydantic import BaseModel
from pydantic import Field


class LoginRequest(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    is_active: bool

    model_config = {
        "from_attributes": True
    }


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse


class TokenPayload(BaseModel):
    sub: str


class ForgotPasswordRequest(BaseModel):
    email: str


class MessageResponse(BaseModel):
    message: str


class ResetPasswordRequest(BaseModel):
    token: str = Field(
        min_length=1,
    )

    new_password: str = Field(
        min_length=8,
    )

    confirm_password: str = Field(
        min_length=8,
    )
    


class ChangeEmailRequest(BaseModel):
    new_email: str = Field(
        min_length=3,
    )


class ConfirmEmailChangeRequest(BaseModel):
    token: str = Field(
        min_length=1,
    )
    


class RegisterRequest(BaseModel):
    email: str = Field(
        min_length=3,
    )

    password: str = Field(
        min_length=8,
    )

    confirm_password: str = Field(
        min_length=8,
    )