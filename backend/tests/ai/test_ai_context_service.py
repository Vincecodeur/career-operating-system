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


def add_work_experience(
    db,
    profile: Profile,
) -> None:
    db.add(
        WorkExperience(
            profile_id=profile.id,
            company_name="Test Company",
            job_title=(
                "Technical Partnerships Manager"
            ),
            start_date=date(
                2020,
                1,
                1,
            ),
            end_date=None,
            is_current_position=True,
            description=(
                "Managed technical partnerships "
                "and platform integrations."
            ),
        )
    )

    db.commit()


def create_complete_profile(
    db,
    *,
    include_soft_skill: bool = True,
    include_certification: bool = True,
) -> Profile:
    profile = create_profile(
        db
    )

    add_hard_skill(
        db,
        profile,
    )

    add_language(
        db,
        profile,
    )

    add_work_experience(
        db,
        profile,
    )

    if include_soft_skill:
        add_soft_skill(
            db,
            profile,
        )

    if include_certification:
        add_certification(
            db,
            profile,
        )

    return profile


def test_complete_profile_is_ai_ready(
    db,
):
    profile = create_complete_profile(
        db
    )

    service = AIContextService(
        db
    )

    preview = service.get_ai_context_preview(
        profile.id
    )

    assert preview is not None
    assert preview.profile_id == profile.id
    assert preview.is_ai_ready is True
    assert (
        preview.missing_required_information
        == []
    )
    assert (
        preview.ai_features_enabled
        is False
    )
    assert (
        preview.ai_consent_accepted
        is False
    )
    assert (
        preview.ai_call_allowed
        is False
    )


def test_missing_current_title_is_not_ready(
    db,
):
    profile = create_profile(
        db,
        current_title="",
    )

    add_hard_skill(
        db,
        profile,
    )

    add_language(
        db,
        profile,
    )

    add_work_experience(
        db,
        profile,
    )

    service = AIContextService(
        db
    )

    preview = service.get_ai_context_preview(
        profile.id
    )

    assert preview is not None
    assert preview.is_ai_ready is False

    assert (
        "Current title is missing"
        in preview.missing_required_information
    )


def test_missing_hard_skill_is_not_ready(
    db,
):
    profile = create_profile(
        db
    )

    add_language(
        db,
        profile,
    )

    add_work_experience(
        db,
        profile,
    )

    service = AIContextService(
    db
    )

    preview = service.get_ai_context_preview(
        profile.id
    )

    assert preview is not None
    assert preview.is_ai_ready is False

    assert (
        "At least one hard skill is required"
        in preview.missing_required_information
    )


@pytest.mark.parametrize(
    (
        "field_name",
        "expected_message",
    ),
    [
        (
            "professional_summary",
            "Professional summary is missing",
        ),
        (
            "career_motivations",
            "Career motivations are missing",
        ),
        (
            "preferred_environment",
            "Preferred environment is missing",
        ),
        (
            "non_negotiables",
            "Non-negotiables are missing",
        ),
        (
            "additional_context",
            "Additional context is missing",
        ),
    ],
)
def test_missing_additional_context_field_is_not_ready(
    db,
    field_name,
    expected_message,
):
    profile = create_profile(
        db,
        **{
            field_name: None,
        },
    )

    add_hard_skill(
        db,
        profile,
    )

    add_language(
        db,
        profile,
    )

    add_work_experience(
        db,
        profile,
    )

    service = AIContextService(
        db
    )

    preview = service.get_ai_context_preview(
        profile.id
    )

    assert preview is not None
    assert preview.is_ai_ready is False

    assert (
        expected_message
        in preview.missing_required_information
    )


def test_missing_optional_categories_do_not_block_readiness(
    db,
):
    profile = create_complete_profile(
        db,
        include_soft_skill=False,
        include_certification=False,
    )

    service = AIContextService(
        db
    )

    preview = service.get_ai_context_preview(
        profile.id
    )

    assert preview is not None
    assert preview.is_ai_ready is True

    assert set(
        preview.missing_optional_categories
    ) == {
        "SOFT_SKILLS",
        "CERTIFICATIONS",
    }


def test_available_categories_reflect_profile_data(
    db,
):
    profile = create_complete_profile(
        db
    )

    service = AIContextService(
        db
    )

    preview = service.get_ai_context_preview(
        profile.id
    )

    assert preview is not None

    assert set(
        preview.available_categories
    ) == {
        "PROFILE_INFORMATION",
        "CAREER_GOALS",
        "HARD_SKILLS",
        "SOFT_SKILLS",
        "LANGUAGES",
        "CERTIFICATIONS",
        "WORK_EXPERIENCES",
        "ADDITIONAL_PROFILE_CONTEXT",
    }

    assert (
        preview.missing_optional_categories
        == []
    )


def test_excluded_categories_are_always_returned(
    db,
):
    profile = create_profile(
        db
    )

    service = AIContextService(
        db
    )

    preview = service.get_ai_context_preview(
        profile.id
    )

    assert preview is not None

    assert preview.excluded_categories == [
        "RAW_CV",
        "UNVALIDATED_ENRICHMENT",
        "APPLICATION_HISTORY",
        "TECHNICAL_SECRETS",
    ]


def test_ai_call_is_allowed_when_all_conditions_are_true(
    db,
):
    profile = create_complete_profile(
        db
    )

    settings_service = SettingsService(
        db
    )

    settings_service.update_ai_settings(
        {
            "ai_features_enabled": True,
            "ai_consent_accepted": True,
        }
    )

    service = AIContextService(
        db
    )

    preview = service.get_ai_context_preview(
        profile.id
    )

    assert preview is not None
    assert preview.is_ai_ready is True
    assert preview.ai_features_enabled is True
    assert preview.ai_consent_accepted is True
    assert preview.ai_call_allowed is True


def test_ai_call_is_blocked_when_profile_is_not_ready(
    db,
):
    profile = create_profile(
        db
    )

    settings_service = SettingsService(
        db
    )

    settings_service.update_ai_settings(
        {
            "ai_features_enabled": True,
            "ai_consent_accepted": True,
        }
    )

    service = AIContextService(
        db
    )

    preview = service.get_ai_context_preview(
        profile.id
    )

    assert preview is not None
    assert preview.is_ai_ready is False
    assert preview.ai_features_enabled is True
    assert preview.ai_consent_accepted is True
    assert preview.ai_call_allowed is False
