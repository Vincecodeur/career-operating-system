from datetime import date
from datetime import datetime
from datetime import timezone
from uuid import uuid4

import pytest

from app.ai.models import JobOfferAIExplanation
from app.ai.scheduler import AIExplanationScheduler
from app.ai.schemas import AIExplanation
from app.ai.schemas import AIExplanationResult
from app.auth.models import User
from app.core.database import SessionLocal
from app.core.settings import settings
from app.experience.models import WorkExperience
from app.jobs.models import JobOffer
from app.languages.models import Language
from app.languages.models import ProfileLanguage
from app.matching.schemas import MatchingResult
from app.matching.schemas import OpportunityAnalysis
from app.profile.models import Profile
from app.profile.profile_skill_models import ProfileSkill
from app.settings.service import SettingsService
from app.skills.models import Skill


TEST_USER_EMAIL = "test-primary-user@career-os.local"


def unique_value(prefix: str) -> str:
    return f"{prefix}_{uuid4()}"


def get_test_user_id(db) -> int:
    user = db.query(User).filter(
        User.email == TEST_USER_EMAIL
    ).first()

    return user.id


def build_matching_result(
    profile_id: int,
    job_offer_id: int,
    matching_score: float,
    is_calculable: bool = True,
) -> MatchingResult:
    return MatchingResult(
        profile_id=profile_id,
        job_offer_id=job_offer_id,
        matching_score=matching_score,
        skills_score=matching_score,
        experience_score=matching_score,
        work_mode_score=matching_score,
        location_score=matching_score,
        matching_skills=["Python"],
        missing_skills=["Kubernetes"],
        strengths=["Strong technical background."],
        weaknesses=["Missing some required skills."],
        explanations=[],
        opportunity_analysis=OpportunityAnalysis(
            verdict="weak",
            recommendation="low_priority",
            summary="Test summary.",
        ),
        is_calculable=is_calculable,
    )


def scoped_matching_result(
    allowed_profile_id,
    allowed_offer_ids,
    matching_score=50.0,
):
    """
    Returns a calculate_matching_result replacement that only treats
    the (allowed_profile_id, offer in allowed_offer_ids) pair as
    calculable with the given score. Any other (profile_id,
    job_offer_id) combination is treated as not calculable.

    Necessary because AIExplanationScheduler.run_once() queries ALL
    active Profile rows for the primary test user, and ALL JobOffer
    rows with quality_level == "COMPLETE", with no ID filter on
    either - exactly like the real production scheduler.

    Real issue found (2026-09-22): when this test file runs alone,
    only this test's own fixtures exist, so filtering by offer id was
    enough. When running the FULL test suite, other test files
    (test_profiles.py, test_work_experiences.py,
    test_profile_enrichment.py, etc.) commit real, AI-ready active
    profiles for the same shared primary test user
    (test-primary-user@career-os.local) without necessarily being
    cleaned up before this test runs. Since ai_features_enabled/
    ai_consent_accepted is an account-level setting (not per
    profile), enabling it here made ALL of those leftover profiles
    eligible too, inflating generated/failed counts (e.g. 10 instead
    of 1). Scoping by profile_id as well as job_offer_id fixes this
    regardless of what other test files leave behind.
    """

    def _calculate(profile_id, job_offer_id, db):
        if (
            profile_id != allowed_profile_id
            or job_offer_id not in allowed_offer_ids
        ):
            return build_matching_result(
                profile_id,
                job_offer_id,
                matching_score=0.0,
                is_calculable=False,
            )

        return build_matching_result(
            profile_id,
            job_offer_id,
            matching_score=matching_score,
        )

    return _calculate


class FakeExplanationService:
    def __init__(self, should_succeed: bool = True):
        self.should_succeed = should_succeed
        self.call_count = 0

    def generate_explanation(self, context):
        self.call_count += 1

        if not self.should_succeed:
            return AIExplanationResult(
                success=False,
                explanation=None,
                error_message="Fake failure for testing.",
            )

        return AIExplanationResult(
            success=True,
            explanation=AIExplanation(
                summary=(
                    "This is a fake AI generated summary for testing."
                ),
                detailed_explanation=(
                    "This is a fake detailed explanation with enough "
                    "content to satisfy schema validation rules."
                ),
                action_plan=["Review the fake weaknesses."],
                generated_at=datetime.now(timezone.utc),
                provider_name="fake",
                model_name="fake-model",
                prompt_version="score_explanation_v2",
            ),
            error_message=None,
        )


@pytest.fixture
def db():
    session = SessionLocal()

    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture
def ai_ready_profile(db):
    user_id = get_test_user_id(db)

    settings_service = SettingsService(db)

    original_ai_settings = settings_service.get_ai_settings(user_id)

    settings_service.update_ai_settings(
        user_id,
        {
            "ai_features_enabled": True,
            "ai_consent_accepted": True,
        },
    )

    skill = Skill(
        name=unique_value("Zzz-Test-Scheduler-Skill"),
        category="Technical",
    )
    db.add(skill)
    db.flush()

    language = Language(
        name=unique_value("Zzz-Test-Scheduler-Language"),
    )
    db.add(language)
    db.flush()

    profile = Profile(
        user_id=user_id,
        profile_name=unique_value("Zzz Test Scheduler Profile"),
        full_name="Zzz Test Scheduler Candidate",
        current_title="Fake Test Engineer",
        location="Fake City",
        years_of_experience=5,
        target_role_short_term="Fake Short Term Role",
        target_role_long_term="Fake Long Term Role",
        remote_preference="Remote",
        preferred_countries="FR",
        professional_summary="Fake professional summary.",
        career_motivations="Fake career motivations.",
        preferred_environment="Fake preferred environment.",
        non_negotiables="Fake non-negotiables.",
        additional_context="Fake additional context.",
        is_active=True,
    )
    db.add(profile)
    db.flush()

    db.add(
        ProfileSkill(
            profile_id=profile.id,
            skill_id=skill.id,
            years_of_experience=5,
            self_assessment_level="Expert",
        )
    )

    db.add(
        WorkExperience(
            profile_id=profile.id,
            company_name="Zzz Test Scheduler Company",
            job_title="Fake Test Engineer",
            start_date=date(2020, 1, 1),
            end_date=None,
            is_current_position=True,
            description="Fake work experience description.",
        )
    )

    db.add(
        ProfileLanguage(
            profile_id=profile.id,
            language_id=language.id,
            proficiency_level="Native",
        )
    )

    db.commit()
    db.refresh(profile)

    try:
        yield profile
    finally:
        db.query(JobOfferAIExplanation).filter(
            JobOfferAIExplanation.profile_id == profile.id
        ).delete()

        db.query(ProfileLanguage).filter(
            ProfileLanguage.profile_id == profile.id
        ).delete()

        db.query(WorkExperience).filter(
            WorkExperience.profile_id == profile.id
        ).delete()

        db.query(ProfileSkill).filter(
            ProfileSkill.profile_id == profile.id
        ).delete()

        db.query(Profile).filter(
            Profile.id == profile.id
        ).delete()

        db.query(Skill).filter(Skill.id == skill.id).delete()
        db.query(Language).filter(
            Language.id == language.id
        ).delete()

        settings_service.update_ai_settings(
            user_id,
            {
                "ai_features_enabled": original_ai_settings[
                    "ai_features_enabled"
                ],
                "ai_consent_accepted": original_ai_settings[
                    "ai_consent_accepted"
                ],
            },
        )

        db.commit()


def create_complete_offer(db) -> JobOffer:
    offer = JobOffer(
        title=unique_value("Zzz Test Scheduler Offer"),
        company_name="Zzz Test Scheduler Employer",
        location="Fake City, FR",
        city="Fake City",
        country="FR",
        source="Zzz-Test",
        description="Fake complete offer description.",
        language="EN",
        work_mode="Remote",
        contract_type="CDI",
        seniority="UNKNOWN",
        quality_level="COMPLETE",
        status="ACTIVE",
    )
    db.add(offer)
    db.commit()
    db.refresh(offer)

    return offer


def delete_offer(db, offer_id: int) -> None:
    db.query(JobOfferAIExplanation).filter(
        JobOfferAIExplanation.job_offer_id == offer_id
    ).delete()

    db.query(JobOffer).filter(JobOffer.id == offer_id).delete()
    db.commit()


def test_run_once_generates_explanation_for_calculable_offer(
    db,
    ai_ready_profile,
    monkeypatch,
):
    offer = create_complete_offer(db)

    monkeypatch.setattr(
        settings,
        "PRIMARY_USER_EMAIL",
        TEST_USER_EMAIL,
    )

    fake_service = FakeExplanationService(should_succeed=True)

    monkeypatch.setattr(
        AIExplanationScheduler,
        "_build_explanation_service",
        staticmethod(lambda: fake_service),
    )

    monkeypatch.setattr(
        "app.ai.scheduler.calculate_matching_result",
        scoped_matching_result(ai_ready_profile.id, {offer.id}),
    )

    monkeypatch.setattr(
        "app.ai.scheduler.time.sleep",
        lambda seconds: None,
    )

    try:
        scheduler = AIExplanationScheduler(
            session_factory=SessionLocal,
        )

        result = scheduler.run_once()

        assert result["generated"] == 1
        assert result["failed"] == 0
        assert fake_service.call_count == 1

        explanation = db.query(JobOfferAIExplanation).filter(
            JobOfferAIExplanation.profile_id == ai_ready_profile.id,
            JobOfferAIExplanation.job_offer_id == offer.id,
        ).first()

        assert explanation is not None
        assert explanation.provider_name == "fake"
    finally:
        delete_offer(db, offer.id)


def test_run_once_skips_profile_without_consent(
    db,
    ai_ready_profile,
    monkeypatch,
):
    offer = create_complete_offer(db)

    user_id = get_test_user_id(db)

    settings_service = SettingsService(db)
    settings_service.update_ai_settings(
        user_id,
        {
            "ai_features_enabled": False,
            "ai_consent_accepted": False,
        },
    )

    monkeypatch.setattr(
        settings,
        "PRIMARY_USER_EMAIL",
        TEST_USER_EMAIL,
    )

    fake_service = FakeExplanationService(should_succeed=True)

    monkeypatch.setattr(
        AIExplanationScheduler,
        "_build_explanation_service",
        staticmethod(lambda: fake_service),
    )

    monkeypatch.setattr(
        "app.ai.scheduler.time.sleep",
        lambda seconds: None,
    )

    try:
        scheduler = AIExplanationScheduler(
            session_factory=SessionLocal,
        )

        result = scheduler.run_once()

        assert result["generated"] == 0
        assert result["skipped_no_consent"] >= 1
        assert fake_service.call_count == 0
    finally:
        delete_offer(db, offer.id)

        settings_service.update_ai_settings(
            user_id,
            {
                "ai_features_enabled": True,
                "ai_consent_accepted": True,
            },
        )


def test_run_once_skips_not_calculable_offer(
    db,
    ai_ready_profile,
    monkeypatch,
):
    offer = create_complete_offer(db)

    monkeypatch.setattr(
        settings,
        "PRIMARY_USER_EMAIL",
        TEST_USER_EMAIL,
    )

    fake_service = FakeExplanationService(should_succeed=True)

    monkeypatch.setattr(
        AIExplanationScheduler,
        "_build_explanation_service",
        staticmethod(lambda: fake_service),
    )

    monkeypatch.setattr(
        "app.ai.scheduler.calculate_matching_result",
        lambda profile_id, job_offer_id, db: build_matching_result(
            profile_id,
            job_offer_id,
            matching_score=0.0,
            is_calculable=False,
        ),
    )

    monkeypatch.setattr(
        "app.ai.scheduler.time.sleep",
        lambda seconds: None,
    )

    try:
        scheduler = AIExplanationScheduler(
            session_factory=SessionLocal,
        )

        result = scheduler.run_once()

        assert result["generated"] == 0
        assert fake_service.call_count == 0
    finally:
        delete_offer(db, offer.id)


def test_run_once_skips_offer_below_minimum_score(
    db,
    ai_ready_profile,
    monkeypatch,
):
    offer = create_complete_offer(db)

    monkeypatch.setattr(
        settings,
        "PRIMARY_USER_EMAIL",
        TEST_USER_EMAIL,
    )

    fake_service = FakeExplanationService(should_succeed=True)

    monkeypatch.setattr(
        AIExplanationScheduler,
        "_build_explanation_service",
        staticmethod(lambda: fake_service),
    )

    monkeypatch.setattr(
        "app.ai.scheduler.calculate_matching_result",
        lambda profile_id, job_offer_id, db: build_matching_result(
            profile_id,
            job_offer_id,
            matching_score=1.0,
        ),
    )

    monkeypatch.setattr(
        "app.ai.scheduler.time.sleep",
        lambda seconds: None,
    )

    try:
        scheduler = AIExplanationScheduler(
            session_factory=SessionLocal,
        )

        result = scheduler.run_once()

        assert result["generated"] == 0
        assert result["skipped_below_threshold"] >= 1
        assert fake_service.call_count == 0
    finally:
        delete_offer(db, offer.id)


def test_run_once_does_not_regenerate_existing_explanation(
    db,
    ai_ready_profile,
    monkeypatch,
):
    offer = create_complete_offer(db)

    db.add(
        JobOfferAIExplanation(
            profile_id=ai_ready_profile.id,
            job_offer_id=offer.id,
            summary="Existing summary long enough to pass validation.",
            detailed_explanation=(
                "Existing detailed explanation long enough to pass "
                "validation rules for this field."
            ),
            action_plan=["Existing action."],
            provider_name="fake",
            model_name="fake-model",
            prompt_version="score_explanation_v2",
            generated_at=datetime.now(timezone.utc),
        )
    )
    db.commit()

    monkeypatch.setattr(
        settings,
        "PRIMARY_USER_EMAIL",
        TEST_USER_EMAIL,
    )

    fake_service = FakeExplanationService(should_succeed=True)

    monkeypatch.setattr(
        AIExplanationScheduler,
        "_build_explanation_service",
        staticmethod(lambda: fake_service),
    )

    # Real issue found (2026-09-22): without scoping the matching
    # result, other leftover active profiles from other test files
    # (with no existing explanation for this offer) would fall
    # through to the REAL calculate_matching_result(), which could
    # legitimately return is_calculable=True on shared test data,
    # inflating fake_service.call_count when running the full suite.
    monkeypatch.setattr(
        "app.ai.scheduler.calculate_matching_result",
        scoped_matching_result(ai_ready_profile.id, {offer.id}),
    )

    monkeypatch.setattr(
        "app.ai.scheduler.time.sleep",
        lambda seconds: None,
    )

    try:
        scheduler = AIExplanationScheduler(
            session_factory=SessionLocal,
        )

        result = scheduler.run_once()

        assert result["generated"] == 0
        assert fake_service.call_count == 0
    finally:
        delete_offer(db, offer.id)


def test_run_once_respects_max_per_run_batch_limit(
    db,
    ai_ready_profile,
    monkeypatch,
):
    offers = [create_complete_offer(db) for _ in range(3)]

    monkeypatch.setattr(
        settings,
        "PRIMARY_USER_EMAIL",
        TEST_USER_EMAIL,
    )

    monkeypatch.setattr(
        settings,
        "AI_EXPLANATION_MAX_PER_RUN",
        2,
    )

    fake_service = FakeExplanationService(should_succeed=True)

    monkeypatch.setattr(
        AIExplanationScheduler,
        "_build_explanation_service",
        staticmethod(lambda: fake_service),
    )

    monkeypatch.setattr(
        "app.ai.scheduler.calculate_matching_result",
        scoped_matching_result(ai_ready_profile.id, {o.id for o in offers}),
    )

    monkeypatch.setattr(
        "app.ai.scheduler.time.sleep",
        lambda seconds: None,
    )

    try:
        scheduler = AIExplanationScheduler(
            session_factory=SessionLocal,
        )

        result = scheduler.run_once()

        assert result["generated"] == 2
        assert fake_service.call_count == 2
    finally:
        for offer in offers:
            delete_offer(db, offer.id)


def test_run_once_applies_pacing_between_calls(
    db,
    ai_ready_profile,
    monkeypatch,
):
    offers = [create_complete_offer(db) for _ in range(2)]

    monkeypatch.setattr(
        settings,
        "PRIMARY_USER_EMAIL",
        TEST_USER_EMAIL,
    )

    fake_service = FakeExplanationService(should_succeed=True)

    monkeypatch.setattr(
        AIExplanationScheduler,
        "_build_explanation_service",
        staticmethod(lambda: fake_service),
    )

    monkeypatch.setattr(
        "app.ai.scheduler.calculate_matching_result",
        scoped_matching_result(ai_ready_profile.id, {o.id for o in offers}),
    )

    sleep_calls = []

    monkeypatch.setattr(
        "app.ai.scheduler.time.sleep",
        lambda seconds: sleep_calls.append(seconds),
    )

    try:
        scheduler = AIExplanationScheduler(
            session_factory=SessionLocal,
        )

        result = scheduler.run_once()

        assert result["generated"] == 2
        assert len(sleep_calls) == 2
        assert all(
            call == settings.AI_EXPLANATION_REQUEST_INTERVAL_SECONDS
            for call in sleep_calls
        )
    finally:
        for offer in offers:
            delete_offer(db, offer.id)


def test_run_once_counts_failed_generation(
    db,
    ai_ready_profile,
    monkeypatch,
):
    offer = create_complete_offer(db)

    monkeypatch.setattr(
        settings,
        "PRIMARY_USER_EMAIL",
        TEST_USER_EMAIL,
    )

    fake_service = FakeExplanationService(should_succeed=False)

    monkeypatch.setattr(
        AIExplanationScheduler,
        "_build_explanation_service",
        staticmethod(lambda: fake_service),
    )

    monkeypatch.setattr(
        "app.ai.scheduler.calculate_matching_result",
        scoped_matching_result(ai_ready_profile.id, {offer.id}),
    )

    monkeypatch.setattr(
        "app.ai.scheduler.time.sleep",
        lambda seconds: None,
    )

    try:
        scheduler = AIExplanationScheduler(
            session_factory=SessionLocal,
        )

        result = scheduler.run_once()

        assert result["generated"] == 0
        assert result["failed"] == 1

        explanation = db.query(JobOfferAIExplanation).filter(
            JobOfferAIExplanation.profile_id == ai_ready_profile.id,
            JobOfferAIExplanation.job_offer_id == offer.id,
        ).first()

        assert explanation is None
    finally:
        delete_offer(db, offer.id)
