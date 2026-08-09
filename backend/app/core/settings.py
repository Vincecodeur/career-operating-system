from pathlib import Path

from dotenv import load_dotenv

import os


BASE_DIR = Path(__file__).resolve().parent.parent.parent

load_dotenv(BASE_DIR / ".env")


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


settings = Settings()