from datetime import date
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.auth.models import User
from app.core.database import SessionLocal
from app.experience.models import WorkExperience
from app.languages.models import Language
from app.languages.models import ProfileLanguage
from app.main import app
from app.profile.models import Profile
from app.profile.profile_skill_models import ProfileSkill
from app.settings.service import SettingsService
from app.skills.models import Skill


client = TestClient(app)


def unique_value(
    prefix: str,
) -> str:
    return f"{prefix}_{uuid4()}"


def update_ai_settings(
    *,
    enabled: bool,
    consent_accepted: bool,
) -> None:
    db = SessionLocal()

    try:
        settings_service = SettingsService(db)

        settings_service.update_ai_settings(
            {
                "ai_features_enabled": enabled,
                "ai_consent_accepted": consent_accepted,
            }
        )
    finally:
        db.close()


@pytest.fixture(
    autouse=True,
)
def reset_ai_settings():
    update_ai_settings(
        enabled=False,
        consent_accepted=False,
    )

    yield

    update_ai_settings(
        enabled=False,
        consent_accepted=False,
    )


TEST_USER_EMAIL = "test-primary-user@career-os.local"


def get_test_user_id(db) -> int:
    test_user = (
        db.query(User)
        .filter(User.email == TEST_USER_EMAIL)
        .first()
    )

    return test_user.id

def create_profile(
    *,
    complete: bool,
) -> int:
    db = SessionLocal()

    try:
        profile = Profile(
            user_id=get_test_user_id(db),
            profile_name=unique_value(
                "AI Router Profile"
            ),
            full_name="AI Router Test User",
            current_title=(
                "Technical Partnerships Manager"
            ),
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
                "Partnership and integration specialist."
                if complete
                else None
            ),
            career_motivations=(
                "Build strategic technology partnerships."
                if complete
                else None
            ),
            preferred_environment=(
                "International SaaS environment."
                if complete
                else None
            ),
            non_negotiables=(
                "Remote flexibility."
                if complete
                else None
            ),
            additional_context=(
                "Interested in platform strategy."
                if complete
                else None
            ),
            is_active=True,
        )

        db.add(profile)
        db.flush()

        profile_id = profile.id

        if complete:
            skill = Skill(
                name=unique_value(
                    "API Integration"
                ),
                category="Technical",
            )

            language = Language(
                name=unique_value(
                    "English"
                ),
            )

            db.add(skill)
            db.add(language)
            db.flush()

            db.add(
                ProfileSkill(
                    profile_id=profile_id,
                    skill_id=skill.id,
                    years_of_experience=5,
                    self_assessment_level="Advanced",
                )
            )

            db.add(
                ProfileLanguage(
                    profile_id=profile_id,
                    language_id=language.id,
                    proficiency_level="Fluent",
                )
            )

            db.add(
                WorkExperience(
                    profile_id=profile_id,
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

        return profile_id
    finally:
        db.close()


def test_get_ai_context_preview_for_complete_profile():
    profile_id = create_profile(
        complete=True
    )

    response = client.get(
        f"/profiles/{profile_id}/ai-context-preview"
    )

    assert response.status_code == 200

    body = response.json()

    assert body["profile_id"] == profile_id
    assert body["is_ai_ready"] is True
    assert body["missing_required_information"] == []
    assert body["ai_features_enabled"] is False
    assert body["ai_consent_accepted"] is False
    assert body["ai_call_allowed"] is False


def test_complete_profile_returns_expected_categories():
    profile_id = create_profile(
        complete=True
    )

    response = client.get(
        f"/profiles/{profile_id}/ai-context-preview"
    )

    assert response.status_code == 200

    body = response.json()

    assert set(
        body["available_categories"]
    ) == {
        "PROFILE_INFORMATION",
        "CAREER_GOALS",
        "HARD_SKILLS",
        "LANGUAGES",
        "WORK_EXPERIENCES",
        "ADDITIONAL_PROFILE_CONTEXT",
    }

    assert set(
        body["missing_optional_categories"]
    ) == {
        "SOFT_SKILLS",
        "CERTIFICATIONS",
    }


def test_get_ai_context_preview_for_incomplete_profile():
    profile_id = create_profile(
        complete=False
    )

    response = client.get(
        f"/profiles/{profile_id}/ai-context-preview"
    )

    assert response.status_code == 200

    body = response.json()

    assert body["profile_id"] == profile_id
    assert body["is_ai_ready"] is False
    assert body["ai_call_allowed"] is False

    missing_information = set(
        body["missing_required_information"]
    )

    assert (
        "At least one hard skill is required"
        in missing_information
    )
    assert (
        "At least one work experience is required"
        in missing_information
    )
    assert (
        "At least one language is required"
        in missing_information
    )
    assert (
        "Professional summary is missing"
        in missing_information
    )
    assert (
        "Career motivations are missing"
        in missing_information
    )
    assert (
        "Preferred environment is missing"
        in missing_information
    )
    assert (
        "Non-negotiables are missing"
        in missing_information
    )
    assert (
        "Additional context is missing"
        in missing_information
    )


def test_get_ai_context_preview_returns_404_for_unknown_profile():
    response = client.get(
        "/profiles/999999999/ai-context-preview"
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Profile not found.",
    }


def test_ready_profile_allows_ai_call_after_consent():
    profile_id = create_profile(
        complete=True
    )

    settings_response = client.put(
        "/settings/ai",
        json={
            "ai_features_enabled": True,
            "ai_consent_accepted": True,
        },
    )

    assert settings_response.status_code == 200

    response = client.get(
        f"/profiles/{profile_id}/ai-context-preview"
    )

    assert response.status_code == 200

    body = response.json()

    assert body["is_ai_ready"] is True
    assert body["ai_features_enabled"] is True
    assert body["ai_consent_accepted"] is True
    assert body["ai_call_allowed"] is True


def test_incomplete_profile_blocks_ai_call_after_consent():
    profile_id = create_profile(
        complete=False
    )

    settings_response = client.put(
        "/settings/ai",
        json={
            "ai_features_enabled": True,
            "ai_consent_accepted": True,
        },
    )

    assert settings_response.status_code == 200

    response = client.get(
        f"/profiles/{profile_id}/ai-context-preview"
    )

    assert response.status_code == 200

    body = response.json()

    assert body["is_ai_ready"] is False
    assert body["ai_features_enabled"] is True
    assert body["ai_consent_accepted"] is True
    assert body["ai_call_allowed"] is False


def test_preview_returns_fixed_excluded_categories():
    profile_id = create_profile(
        complete=True
    )

    response = client.get(
        f"/profiles/{profile_id}/ai-context-preview"
    )

    assert response.status_code == 200

    body = response.json()

    assert body["excluded_categories"] == [
        "RAW_CV",
        "UNVALIDATED_ENRICHMENT",
        "APPLICATION_HISTORY",
        "TECHNICAL_SECRETS",
    ]


def test_preview_response_contains_only_contract_fields():
    profile_id = create_profile(
        complete=True
    )

    response = client.get(
        f"/profiles/{profile_id}/ai-context-preview"
    )

    assert response.status_code == 200

    body = response.json()

    assert set(body.keys()) == {
        "profile_id",
        "is_ai_ready",
        "missing_required_information",
        "available_categories",
        "missing_optional_categories",
        "excluded_categories",
        "ai_features_enabled",
        "ai_consent_accepted",
        "ai_call_allowed",
    }
