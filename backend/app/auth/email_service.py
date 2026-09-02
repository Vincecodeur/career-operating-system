import smtplib
from email.message import EmailMessage
from email.utils import formataddr

from app.core.settings import settings


def validate_smtp_configuration() -> None:
    required_values = {
        "SMTP_HOST": settings.SMTP_HOST,
        "SMTP_USERNAME": (
            settings.SMTP_USERNAME
        ),
        "SMTP_PASSWORD": (
            settings.SMTP_PASSWORD
        ),
        "SMTP_FROM_EMAIL": (
            settings.SMTP_FROM_EMAIL
        ),
    }

    missing_values = [
        name
        for name, value
        in required_values.items()
        if not value
    ]

    if missing_values:
        raise RuntimeError(
            "Missing SMTP configuration: "
            + ", ".join(missing_values)
        )


def build_password_reset_url(
    token: str,
) -> str:
    base_url = (
        settings.FRONTEND_BASE_URL.rstrip(
            "/"
        )
    )

    return (
        f"{base_url}/reset-password"
        f"?token={token}"
    )


def send_password_reset_email(
    recipient_email: str,
    reset_token: str,
) -> None:
    validate_smtp_configuration()

    reset_url = build_password_reset_url(
        reset_token
    )

    message = EmailMessage()

    message["Subject"] = (
        "Reset your Career Operating System password"
    )

    message["From"] = formataddr(
        (
            settings.SMTP_FROM_NAME,
            settings.SMTP_FROM_EMAIL,
        )
    )

    message["To"] = recipient_email

    message.set_content(
        "\n".join(
            [
                "A password reset was requested "
                "for your Career Operating System "
                "account.",
                "",
                "Use the following link to reset "
                "your password:",
                reset_url,
                "",
                "This link expires after "
                f"{settings.PASSWORD_RESET_TOKEN_EXPIRE_MINUTES} "
                "minutes.",
                "",
                "If you did not request this "
                "password reset, you can ignore "
                "this email.",
            ]
        )
    )

    with smtplib.SMTP(
        host=settings.SMTP_HOST,
        port=settings.SMTP_PORT,
        timeout=10,
    ) as smtp_server:
        smtp_server.ehlo()

        if settings.SMTP_USE_TLS:
            smtp_server.starttls()
            smtp_server.ehlo()

        smtp_server.login(
            settings.SMTP_USERNAME,
            settings.SMTP_PASSWORD,
        )

        smtp_server.send_message(
            message
        )
        
def build_email_change_confirmation_url(
    token: str,
) -> str:
    base_url = (
        settings.FRONTEND_BASE_URL.rstrip(
            "/"
        )
    )

    return (
        f"{base_url}/confirm-email-change"
        f"?token={token}"
    )


def send_email_change_confirmation_email(
    recipient_email: str,
    new_email: str,
    confirmation_token: str,
) -> None:
    validate_smtp_configuration()

    confirmation_url = (
        build_email_change_confirmation_url(
            confirmation_token
        )
    )

    message = EmailMessage()

    message["Subject"] = (
        "Confirm your Career Operating System "
        "email change"
    )

    message["From"] = formataddr(
        (
            settings.SMTP_FROM_NAME,
            settings.SMTP_FROM_EMAIL,
        )
    )

    message["To"] = recipient_email

    message.set_content(
        "\n".join(
            [
                "A request was made to change the "
                "email address associated with your "
                "Career Operating System account to:",
                "",
                new_email,
                "",
                "Use the following link to confirm "
                "this change:",
                confirmation_url,
                "",
                "This link expires after "
                f"{settings.EMAIL_CHANGE_TOKEN_EXPIRE_MINUTES} "
                "minutes.",
                "",
                "If you did not request this change, "
                "you can ignore this email and your "
                "current email address will remain "
                "unchanged.",
            ]
        )
    )

    with smtplib.SMTP(
        host=settings.SMTP_HOST,
        port=settings.SMTP_PORT,
        timeout=10,
    ) as smtp_server:
        smtp_server.ehlo()

        if settings.SMTP_USE_TLS:
            smtp_server.starttls()
            smtp_server.ehlo()

        smtp_server.login(
            settings.SMTP_USERNAME,
            settings.SMTP_PASSWORD,
        )

        smtp_server.send_message(
            message
        )