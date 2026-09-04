from datetime import date
from uuid import uuid4

import pytest

from app.ai.context_service import AIContextService
from app.auth.models import User
from app.certifications.models import Certification
from app.certifications.models import ProfileCertification
from app.core.database import SessionLocal
from app.experience.models import WorkExperience
from app.languages.models import Language
from app.languages.models import ProfileLanguage
from app.profile.models import Profile
from app.profile.profile_skill_models import ProfileSkill
from app.profile.profile_soft_skill_models import ProfileSoftSkill
from app.settings.service import SettingsService
from app.skills.models import Skill


TEST_USER_EMAIL = "test-primary-user@career-os.local"


def get_test_user_id(db) -> int:
    test_user = (
        db.query(User)
        .filter(User.email == TEST_USER_EMAIL)
        .first()
    )

    return test_user.id


def unique_value(
    prefix: str,
) -> str:
    return f"{prefix}_{uuid4()}"


@pytest.fixture
def db():
    session = SessionLocal()

    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture(
    autouse=True,
)
def reset_ai_settings(
    db,
):
    settings_service = SettingsService(
        db
    )

    settings_service.update_ai_settings(
        {
            "ai_features_enabled": False,
            "ai_consent_accepted": False,
        }
    )

    yield

    settings_service.update_ai_settings(
        {
            "ai_features_enabled": False,
            "ai_consent_accepted": False,
        }
    )


def create_profile(
    db,
    *,
    current_title: str | None = (
        "Technical Partnerships Manager"
    ),
    professional_summary: str | None = (
        "Partnership and integration specialist."
    ),
    career_motivations: str | None = (
        "Build strategic technology partnerships."
    ),
    preferred_environment: str | None = (
        "International SaaS environment."
    ),
    non_negotiables: str | None = (
        "Remote flexibility."
    ),
    additional_context: str | None = (
        "Interested in platform strategy."
    ),
) -> Profile:
    profile = Profile(
        user_id=get_test_user_id(db),
        profile_name=unique_value(
            "AI Context Profile"
        ),
        full_name="AI Context Test User",
        current_title=current_title or "",
        location="France",
        years_of_experience=10,
        target_role_short_term=(
            "Head of Partnerships"
        ),
        target_role_long_term=(
            "VP Partnerships"
        ),
        remote_preference="HYBRID",
        preferred_countries="FR,UK",
        professional_summary=(
            professional_summary
        ),
        career_motivations=(
            career_motivations
        ),
        preferred_environment=(
            preferred_environment
        ),
        non_negotiables=(
            non_negotiables
        ),
        additional_context=(
            additional_context
        ),
        is_active=True,
    )

    db.add(profile)
    db.commit()
    db.refresh(profile)

    return profile


def add_hard_skill(
    db,
    profile: Profile,
) -> None:
    skill = Skill(
        name=unique_value(
            "API Integration"
        ),
        category="Technical",
    )

    db.add(skill)
    db.flush()

    db.add(
        ProfileSkill(
            profile_id=profile.id,
            skill_id=skill.id,
            years_of_experience=5,
            self_assessment_level="Advanced",
        )
    )

    db.commit()


def add_soft_skill(
    db,
    profile: Profile,
) -> None:
    db.add(
        ProfileSoftSkill(
            profile_id=profile.id,
            name=unique_value(
                "Stakeholder Management"
            ),
        )
    )

    db.commit()


def add_language(
    db,
    profile: Profile,
) -> None:
    language = Language(
        name=unique_value(
            "English"
        ),
    )

    db.add(language)
    db.flush()

    db.add(
        ProfileLanguage(
            profile_id=profile.id,
            language_id=language.id,
            proficiency_level="Fluent",
        )
    )

    db.commit()


def add_certification(
    db,
    profile: Profile,
) -> None:
    certification = Certification(
        name=unique_value(
            "Cloud Certification"
        ),
        issuing_organization=(
            "Test Organization"
        ),
    )

    db.add(certification)
    db.flush()

    db.add(
        ProfileCertification(
            profile_id=profile.id,
            certification_id=(
                certification.id
            ),
            obtained_date=date(
                2025,
                1,
                1,
            ),
            expiration_date=None,
            credential_id=None,
        )
    )

    db.commit()