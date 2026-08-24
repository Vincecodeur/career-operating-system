import os
import sys
from pathlib import Path

from dotenv import load_dotenv


BACKEND_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BACKEND_DIR / ".env"

sys.path.insert(
    0,
    str(BACKEND_DIR),
)

load_dotenv(ENV_FILE)

TEST_DATABASE_URL = os.getenv(
    "DATABASE_URL_TEST",
    "",
)

if not TEST_DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL_TEST is required to run the test suite."
    )

if not TEST_DATABASE_URL.endswith(
    "/career_os_test"
):
    raise RuntimeError(
        "Test execution refused: DATABASE_URL_TEST must target "
        "the career_os_test database."
    )

os.environ["DATABASE_URL"] = TEST_DATABASE_URL


from app.core.database import Base
from app.core.database import SessionLocal
from app.core.database import engine
from app.jobs.models import JobOffer
from app.main import app
from app.profile.models import Profile
from app.reference_data.seed_loader import (
    seed_reference_data,
)


def reset_test_database() -> None:
    Base.metadata.drop_all(
        bind=engine,
    )

    Base.metadata.create_all(
        bind=engine,
    )


def seed_required_test_data() -> None:
    db = SessionLocal()

    try:
        seed_reference_data(db)

        db.add_all(
            [
                Profile(
                    profile_name="Test Primary Profile",
                    full_name="Primary Test User",
                    current_title="Technical Partnerships Manager",
                    location="France",
                    years_of_experience=10,
                    target_role_short_term="Solution Architect",
                    target_role_long_term="Enterprise Architect",
                    remote_preference="Hybrid",
                    preferred_countries="France,UK",
                    is_active=True,
                ),
                Profile(
                    profile_name="Test Secondary Profile",
                    full_name="Secondary Test User",
                    current_title="Solution Architect",
                    location="France",
                    years_of_experience=8,
                    target_role_short_term="Enterprise Architect",
                    target_role_long_term="CTO",
                    remote_preference="Remote",
                    preferred_countries="France,UK",
                    is_active=True,
                ),
            ]
        )

        db.add(
            JobOffer(
                title="Test Job Offer",
                company_name="Test Company",
                location="France",
                country="France",
                source="TEST",
                description="Test job offer used by the automated test suite.",
                language="English",
                work_mode="Hybrid",
                contract_type="Permanent",
                seniority="Senior",
                quality_level="COMPLETE",
                status="ACTIVE",
            )
        )

        db.commit()
    finally:
        db.close()


reset_test_database()
seed_required_test_data()