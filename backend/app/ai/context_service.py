from sqlalchemy.orm import Session

from app.ai.context_schemas import (
    AIContextPreviewResponse,
)
from app.certifications.models import (
    ProfileCertification,
)
from app.experience.models import WorkExperience
from app.languages.models import ProfileLanguage
from app.profile.models import Profile
from app.profile.profile_skill_models import (
    ProfileSkill,
)
from app.profile.profile_soft_skill_models import (
    ProfileSoftSkill,
)
from app.settings.service import SettingsService


AVAILABLE_CATEGORY_PROFILE_INFORMATION = (
    "PROFILE_INFORMATION"
)
AVAILABLE_CATEGORY_CAREER_GOALS = (
    "CAREER_GOALS"
)
AVAILABLE_CATEGORY_HARD_SKILLS = (
    "HARD_SKILLS"
)
AVAILABLE_CATEGORY_SOFT_SKILLS = (
    "SOFT_SKILLS"
)
AVAILABLE_CATEGORY_LANGUAGES = (
    "LANGUAGES"
)
AVAILABLE_CATEGORY_CERTIFICATIONS = (
    "CERTIFICATIONS"
)
AVAILABLE_CATEGORY_WORK_EXPERIENCES = (
    "WORK_EXPERIENCES"
)
AVAILABLE_CATEGORY_ADDITIONAL_CONTEXT = (
    "ADDITIONAL_PROFILE_CONTEXT"
)


EXCLUDED_CATEGORIES = [
    "RAW_CV",
    "UNVALIDATED_ENRICHMENT",
    "APPLICATION_HISTORY",
    "TECHNICAL_SECRETS",
]


class AIContextService:
    """
    Evaluates AI readiness and builds a safe context preview.

    This service never calls an AI provider, builds a prompt,
    reads raw CV content or uses pending enrichment proposals.
    """

    def __init__(
        self,
        db: Session,
    ):
        self.db = db
        self.settings_service = SettingsService(
            db
        )

    @staticmethod
    def _has_text(
        value: str | None,
    ) -> bool:
        return bool(
            value
            and value.strip()
        )

    def get_profile(
        self,
        profile_id: int,
    ) -> Profile | None:
        return (
            self.db.query(Profile)
            .filter(
                Profile.id == profile_id
            )
            .first()
        )

    def _has_hard_skills(
        self,
        profile_id: int,
    ) -> bool:
        return (
            self.db.query(ProfileSkill)
            .filter(
                ProfileSkill.profile_id
                == profile_id
            )
            .first()
            is not None
        )

    def _has_soft_skills(
        self,
        profile_id: int,
    ) -> bool:
        return (
            self.db.query(ProfileSoftSkill)
            .filter(
                ProfileSoftSkill.profile_id
                == profile_id
            )
            .first()
            is not None
        )

    def _has_languages(
        self,
        profile_id: int,
    ) -> bool:
        return (
            self.db.query(ProfileLanguage)
            .filter(
                ProfileLanguage.profile_id
                == profile_id
            )
            .first()
            is not None
        )

    def _has_certifications(
        self,
        profile_id: int,
    ) -> bool:
        return (
            self.db.query(
                ProfileCertification
            )
            .filter(
                ProfileCertification.profile_id
                == profile_id
            )
            .first()
            is not None
        )

    def _has_work_experiences(
        self,
        profile_id: int,
    ) -> bool:
        return (
            self.db.query(WorkExperience)
            .filter(
                WorkExperience.profile_id
                == profile_id
            )
            .first()
            is not None
        )

    def _get_missing_required_information(
        self,
        profile: Profile,
        has_hard_skills: bool,
        has_work_experiences: bool,
        has_languages: bool,
    ) -> list[str]:
        missing_information: list[str] = []

        if not self._has_text(
            profile.current_title
        ):
            missing_information.append(
                "Current title is missing"
            )

        if not has_hard_skills:
            missing_information.append(
                "At least one hard skill is required"
            )

        if not has_work_experiences:
            missing_information.append(
                "At least one work experience is required"
            )

        if not has_languages:
            missing_information.append(
                "At least one language is required"
            )

        if not self._has_text(
            profile.professional_summary
        ):
            missing_information.append(
                "Professional summary is missing"
            )

        if not self._has_text(
            profile.career_motivations
        ):
            missing_information.append(
                "Career motivations are missing"
            )

        if not self._has_text(
            profile.preferred_environment
        ):
            missing_information.append(
                "Preferred environment is missing"
            )

        if not self._has_text(
            profile.non_negotiables
        ):
            missing_information.append(
                "Non-negotiables are missing"
            )

        if not self._has_text(
            profile.additional_context
        ):
            missing_information.append(
                "Additional context is missing"
            )

        return missing_information

    def _get_available_categories(
        self,
        profile: Profile,
        has_hard_skills: bool,
        has_soft_skills: bool,
        has_languages: bool,
        has_certifications: bool,
        has_work_experiences: bool,
    ) -> list[str]:
        available_categories = [
            AVAILABLE_CATEGORY_PROFILE_INFORMATION,
        ]

        has_career_goals = any(
            [
                self._has_text(
                    profile.target_role_short_term
                ),
                self._has_text(
                    profile.target_role_long_term
                ),
                self._has_text(
                    profile.remote_preference
                ),
                self._has_text(
                    profile.preferred_countries
                ),
            ]
        )

        if has_career_goals:
            available_categories.append(
                AVAILABLE_CATEGORY_CAREER_GOALS
            )

        if has_hard_skills:
            available_categories.append(
                AVAILABLE_CATEGORY_HARD_SKILLS
            )

        if has_soft_skills:
            available_categories.append(
                AVAILABLE_CATEGORY_SOFT_SKILLS
            )

        if has_languages:
            available_categories.append(
                AVAILABLE_CATEGORY_LANGUAGES
            )

        if has_certifications:
            available_categories.append(
                AVAILABLE_CATEGORY_CERTIFICATIONS
            )

        if has_work_experiences:
            available_categories.append(
                AVAILABLE_CATEGORY_WORK_EXPERIENCES
            )

        has_additional_context = any(
            [
                self._has_text(
                    profile.professional_summary
                ),
                self._has_text(
                    profile.career_motivations
                ),
                self._has_text(
                    profile.preferred_environment
                ),
                self._has_text(
                    profile.non_negotiables
                ),
                self._has_text(
                    profile.additional_context
                ),
            ]
        )

        if has_additional_context:
            available_categories.append(
                AVAILABLE_CATEGORY_ADDITIONAL_CONTEXT
            )

        return available_categories

    @staticmethod
    def _get_missing_optional_categories(
        has_soft_skills: bool,
        has_certifications: bool,
    ) -> list[str]:
        missing_categories: list[str] = []

        if not has_soft_skills:
            missing_categories.append(
                AVAILABLE_CATEGORY_SOFT_SKILLS
            )

        if not has_certifications:
            missing_categories.append(
                AVAILABLE_CATEGORY_CERTIFICATIONS
            )

        return missing_categories

    def get_ai_context_preview(
        self,
        profile_id: int,
    ) -> AIContextPreviewResponse | None:
        profile = self.get_profile(
            profile_id
        )

        if profile is None:
            return None

        has_hard_skills = (
            self._has_hard_skills(
                profile_id
            )
        )
        has_soft_skills = (
            self._has_soft_skills(
                profile_id
            )
        )
        has_languages = (
            self._has_languages(
                profile_id
            )
        )
        has_certifications = (
            self._has_certifications(
                profile_id
            )
        )
        has_work_experiences = (
            self._has_work_experiences(
                profile_id
            )
        )

        missing_required_information = (
            self._get_missing_required_information(
                profile=profile,
                has_hard_skills=has_hard_skills,
                has_work_experiences=(
                    has_work_experiences
                ),
                has_languages=has_languages,
            )
        )

        is_ai_ready = not (
            missing_required_information
        )

        ai_settings = (
            self.settings_service.get_ai_settings()
        )

        ai_features_enabled = ai_settings[
            "ai_features_enabled"
        ]
        ai_consent_accepted = ai_settings[
            "ai_consent_accepted"
        ]

        ai_call_allowed = all(
            [
                is_ai_ready,
                ai_features_enabled,
                ai_consent_accepted,
            ]
        )

        return AIContextPreviewResponse(
            profile_id=profile_id,
            is_ai_ready=is_ai_ready,
            missing_required_information=(
                missing_required_information
            ),
            available_categories=(
                self._get_available_categories(
                    profile=profile,
                    has_hard_skills=(
                        has_hard_skills
                    ),
                    has_soft_skills=(
                        has_soft_skills
                    ),
                    has_languages=(
                        has_languages
                    ),
                    has_certifications=(
                        has_certifications
                    ),
                    has_work_experiences=(
                        has_work_experiences
                    ),
                )
            ),
            missing_optional_categories=(
                self._get_missing_optional_categories(
                    has_soft_skills=(
                        has_soft_skills
                    ),
                    has_certifications=(
                        has_certifications
                    ),
                )
            ),
            excluded_categories=list(
                EXCLUDED_CATEGORIES
            ),
            ai_features_enabled=(
                ai_features_enabled
            ),
            ai_consent_accepted=(
                ai_consent_accepted
            ),
            ai_call_allowed=ai_call_allowed,
        )