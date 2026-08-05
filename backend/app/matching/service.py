
from sqlalchemy.orm import Session

from app.jobs.job_offer_skill_models import JobOfferSkill
from app.jobs.models import JobOffer
from app.matching.schemas import MatchingResult
from app.matching.schemas import RankedJobOffer
from app.profile.profile_skill_models import ProfileSkill
from app.skills.models import Skill


def calculate_matching_result(
    profile_id: int,
    job_offer_id: int,
    db: Session
) -> MatchingResult:
    profile_skill_ids = {
        item.skill_id
        for item in db.query(ProfileSkill).filter(
            ProfileSkill.profile_id == profile_id
        ).all()
    }

    job_offer_skill_ids = {
        item.skill_id
        for item in db.query(JobOfferSkill).filter(
            JobOfferSkill.job_offer_id == job_offer_id
        ).all()
    }

    matching_ids = (
        profile_skill_ids
        & job_offer_skill_ids
    )

    missing_ids = (
        job_offer_skill_ids
        - profile_skill_ids
    )

    skill_ids = (
        matching_ids
        | missing_ids
    )

    skills = []

    if skill_ids:
        skills = db.query(Skill).filter(
            Skill.id.in_(skill_ids)
        ).all()

    skill_name_by_id = {
        skill.id: skill.name
        for skill in skills
    }

    matching_skills = sorted(
        [
            skill_name_by_id[skill_id]
            for skill_id in matching_ids
            if skill_id in skill_name_by_id
        ]
    )

    missing_skills = sorted(
        [
            skill_name_by_id[skill_id]
            for skill_id in missing_ids
            if skill_id in skill_name_by_id
        ]
    )

    if len(job_offer_skill_ids) == 0:
        score = 0.0
    else:
        score = round(
            (
                len(matching_ids)
                / len(job_offer_skill_ids)
            ) * 100,
            2
        )

    return MatchingResult(
        profile_id=profile_id,
        job_offer_id=job_offer_id,
        matching_score=score,
        matching_skills=matching_skills,
        missing_skills=missing_skills
    )


def rank_job_offers_for_profile(
    profile_id: int,
    db: Session
) -> list[RankedJobOffer]:
    job_offers = db.query(JobOffer).all()

    ranked_job_offers = []

    for job_offer in job_offers:
        matching_result = calculate_matching_result(
            profile_id=profile_id,
            job_offer_id=job_offer.id,
            db=db
        )

        ranked_job_offers.append(
            RankedJobOffer(
                job_offer_id=job_offer.id,
                title=job_offer.title,
                matching_score=matching_result.matching_score,
                matching_skills=matching_result.matching_skills,
                missing_skills=matching_result.missing_skills
            )
        )

    ranked_job_offers.sort(
        key=lambda item: item.matching_score,
        reverse=True
    )

    return ranked_job_offers