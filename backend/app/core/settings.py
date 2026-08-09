from pathlib import Path

from dotenv import load_dotenv

import os


BASE_DIR = Path(__file__).resolve().parent.parent.parent

load_dotenv(BASE_DIR / ".env")


def _get_bool_env(
    name: str,
    default: str = "false",
) -> bool:
    return os.getenv(
        name,
        default,
    ).lower() == "true"


def _get_int_env(
    name: str,
    default: str,
) -> int:
    return int(
        os.getenv(
            name,
            default,
        )
    )


def _get_list_env(
    name: str,
    default: str,
) -> list[str]:
    raw_value = os.getenv(
        name,
        default,
    )

    return [
        item.strip()
        for item in raw_value.split(",")
        if item.strip()
    ]


class Settings:
    FRANCE_TRAVAIL_CLIENT_ID: str = os.getenv(
        "FRANCE_TRAVAIL_CLIENT_ID",
        "",
    )

    FRANCE_TRAVAIL_CLIENT_SECRET: str = os.getenv(
        "FRANCE_TRAVAIL_CLIENT_SECRET",
        "",
    )

    FRANCE_TRAVAIL_TOKEN_URL: str = os.getenv(
        "FRANCE_TRAVAIL_TOKEN_URL",
        "https://entreprise.francetravail.fr/connexion/oauth2/access_token?realm=/partenaire",
    )

    FRANCE_TRAVAIL_API_URL: str = os.getenv(
        "FRANCE_TRAVAIL_API_URL",
        "https://api.francetravail.io/partenaire/offresdemploi",
    )

    DISCOVERY_ENABLED: bool = _get_bool_env(
        "DISCOVERY_ENABLED",
        "false",
    )

    DISCOVERY_INTERVAL_MINUTES: int = _get_int_env(
        "DISCOVERY_INTERVAL_MINUTES",
        "1440",
    )

    DISCOVERY_CONNECTORS: list[str] = _get_list_env(
        "DISCOVERY_CONNECTORS",
        "france_travail",
    )
    
    LINKEDIN_CLIENT_ID: str = os.getenv(
        "LINKEDIN_CLIENT_ID",
        "",
    )

    LINKEDIN_CLIENT_SECRET: str = os.getenv(
        "LINKEDIN_CLIENT_SECRET",
        "",
    )

    LINKEDIN_ACCESS_TOKEN: str = os.getenv(
        "LINKEDIN_ACCESS_TOKEN",
        "",
    )

    LINKEDIN_API_URL: str = os.getenv(
        "LINKEDIN_API_URL",
        "",
    )

    LINKEDIN_TIMEOUT: int = _get_int_env(
        "LINKEDIN_TIMEOUT",
        "10",
    )


settings = Settings()