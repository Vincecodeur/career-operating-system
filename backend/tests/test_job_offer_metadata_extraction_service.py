from uuid import uuid4

import pytest

from app.ai.providers.gemini_provider import GeminiProvider
from app.core.database import SessionLocal
from app.core.settings import settings
from app.jobs.job_offer_metadata_extraction_schemas import (
    ExtractedJobOfferMetadata,
)
from app.jobs.job_offer_metadata_extraction_service import (
    JobOfferMetadataExtractionService,
)
from app.jobs.job_offer_skill_models import JobOfferSkill
from app.jobs.models import JobOffer
from app.skills.models import Skill


def unique_value(prefix: str) -> str:
    return f"{prefix}_{uuid4()}"


@pytest.fixture
def db():
    session = SessionLocal()

    try:
        yield session
    finally:
        session.rollback()
        session.close()


def create_test_offer(
    db,
    description: str = (
        "A complete job description mentioning relevant skills."
    ),
) -> JobOffer:
    offer = JobOffer(
        title=unique_value("Zzz Test Metadata Extraction Offer"),
        company_name="Zzz Test Company",
        location="Paris",
        source="LinkedIn",
        description=description,
        quality_level="COMPLETE",
        status="ACTIVE",
    )
    db.add(offer)
    db.commit()
    db.refresh(offer)

    return offer


def create_test_skill(db, name: str) -> Skill:
    skill = Skill(
        name=unique_value(name),
        category="Technical",
    )
    db.add(skill)
    db.commit()
    db.refresh(skill)

    return skill


def delete_test_offer(db, offer_id: int) -> None:
    db.query(JobOfferSkill).filter(
        JobOfferSkill.job_offer_id == offer_id
    ).delete()

    db.query(JobOffer).filter(JobOffer.id == offer_id).delete()
    db.commit()


def delete_test_skill(db, skill_id: int) -> None:
    db.query(Skill).filter(Skill.id == skill_id).delete()
    db.commit()


def test_extract_and_persist_returns_false_for_unknown_offer(
    db,
):
    success = JobOfferMetadataExtractionService.extract_and_persist(
        db=db,
        job_offer_id=999999,
    )

    assert success is False


def test_extract_and_persist_matches_known_skill_and_reports_unmatched(
    db,
    monkeypatch,
):
    monkeypatch.setattr(
        settings,
        "GEMINI_API_KEY",
        "fake-test-api-key",
    )

    skill = create_test_skill(db, "Zzz-Test-Python")
    offer = create_test_offer(db)

    fake_result = ExtractedJobOfferMetadata(
        matched_skills=[skill.name],
        unmatched_skill_mentions=["SomeUnlistedTool"],
        seniority="Senior",
        work_mode="Remote",
    )

    monkeypatch.setattr(
        GeminiProvider,
        "extract_job_offer_metadata",
        lambda self, prompt: fake_result,
    )

    try:
        success = (
            JobOfferMetadataExtractionService.extract_and_persist(
                db=db,
                job_offer_id=offer.id,
            )
        )

        assert success is True

        db.refresh(offer)

        assert offer.seniority == "Senior"
        assert offer.work_mode == "Remote"
        assert offer.skills_normalized == [skill.name]
        assert offer.skills_extracted == ["SomeUnlistedTool"]

        job_offer_skills = db.query(JobOfferSkill).filter(
            JobOfferSkill.job_offer_id == offer.id
        ).all()

        assert len(job_offer_skills) == 1
        assert job_offer_skills[0].skill_id == skill.id
    finally:
        delete_test_offer(db, offer.id)
        delete_test_skill(db, skill.id)


def test_extract_and_persist_matches_skill_case_insensitively(
    db,
    monkeypatch,
):
    monkeypatch.setattr(
        settings,
        "GEMINI_API_KEY",
        "fake-test-api-key",
    )

    skill = create_test_skill(db, "Zzz-Test-Docker")
    offer = create_test_offer(db)

    fake_result = ExtractedJobOfferMetadata(
        matched_skills=[skill.name.upper()],
        unmatched_skill_mentions=[],
        seniority="UNKNOWN",
        work_mode="UNKNOWN",
    )

    monkeypatch.setattr(
        GeminiProvider,
        "extract_job_offer_metadata",
        lambda self, prompt: fake_result,
    )

    try:
        success = (
            JobOfferMetadataExtractionService.extract_and_persist(
                db=db,
                job_offer_id=offer.id,
            )
        )

        assert success is True

        job_offer_skills = db.query(JobOfferSkill).filter(
            JobOfferSkill.job_offer_id == offer.id
        ).all()

        assert len(job_offer_skills) == 1
        assert job_offer_skills[0].skill_id == skill.id
    finally:
        delete_test_offer(db, offer.id)
        delete_test_skill(db, skill.id)


def test_extract_and_persist_ignores_matched_skill_not_in_catalog(
    db,
    monkeypatch,
):
    monkeypatch.setattr(
        settings,
        "GEMINI_API_KEY",
        "fake-test-api-key",
    )

    offer = create_test_offer(db)

    fake_result = ExtractedJobOfferMetadata(
        matched_skills=["Zzz-Nonexistent-Skill-Name"],
        unmatched_skill_mentions=[],
        seniority="Mid",
        work_mode="Hybrid",
    )

    monkeypatch.setattr(
        GeminiProvider,
        "extract_job_offer_metadata",
        lambda self, prompt: fake_result,
    )

    try:
        success = (
            JobOfferMetadataExtractionService.extract_and_persist(
                db=db,
                job_offer_id=offer.id,
            )
        )

        assert success is True

        db.refresh(offer)

        assert offer.skills_normalized == []

        job_offer_skills = db.query(JobOfferSkill).filter(
            JobOfferSkill.job_offer_id == offer.id
        ).all()

        assert len(job_offer_skills) == 0
    finally:
        delete_test_offer(db, offer.id)


def test_extract_and_persist_replaces_previous_skills(
    db,
    monkeypatch,
):
    monkeypatch.setattr(
        settings,
        "GEMINI_API_KEY",
        "fake-test-api-key",
    )

    old_skill = create_test_skill(db, "Zzz-Test-Old-Skill")
    new_skill = create_test_skill(db, "Zzz-Test-New-Skill")
    offer = create_test_offer(db)

    db.add(
        JobOfferSkill(
            job_offer_id=offer.id,
            skill_id=old_skill.id,
            is_required=True,
        )
    )
    db.commit()

    fake_result = ExtractedJobOfferMetadata(
        matched_skills=[new_skill.name],
        unmatched_skill_mentions=[],
        seniority="UNKNOWN",
        work_mode="UNKNOWN",
    )

    monkeypatch.setattr(
        GeminiProvider,
        "extract_job_offer_metadata",
        lambda self, prompt: fake_result,
    )

    try:
        JobOfferMetadataExtractionService.extract_and_persist(
            db=db,
            job_offer_id=offer.id,
        )

        job_offer_skills = db.query(JobOfferSkill).filter(
            JobOfferSkill.job_offer_id == offer.id
        ).all()

        skill_ids = {item.skill_id for item in job_offer_skills}

        assert skill_ids == {new_skill.id}
    finally:
        delete_test_offer(db, offer.id)
        delete_test_skill(db, old_skill.id)
        delete_test_skill(db, new_skill.id)
