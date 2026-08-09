from sqlalchemy.orm import Session

from app.jobs.job_offer_skill_models import JobOfferSkill
from app.jobs.models import JobOffer
from app.matching.schemas import MatchingResult
from app.matching.schemas import RankedJobOffer
from app.matching.schemas import ScoreExplanation
from app.matching.schemas import OpportunityAnalysis
from app.profile.models import Profile
from app.profile.profile_skill_models import ProfileSkill
from app.skills.models import Skill


SKILLS_WEIGHT = 0.70
EXPERIENCE_WEIGHT = 0.15
WORK_MODE_WEIGHT = 0.10
LOCATION_WEIGHT = 0.05


def calculate_matching_result(
    profile_id: int,
    job_offer_id: int,
    db: Session,
) -> MatchingResult:
    profile = db.query(Profile).filter(
        Profile.id == profile_id
    ).first()

    job_offer = db.query(JobOffer).filter(
        JobOffer.id == job_offer_id
    ).first()

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

    skills_score = calculate_skills_score(
        matching_ids=matching_ids,
        job_offer_skill_ids=job_offer_skill_ids,
    )

    experience_score = calculate_experience_score(
        profile=profile,
        job_offer=job_offer,
    )

    work_mode_score = calculate_work_mode_score(
        profile=profile,
        job_offer=job_offer,
    )

    location_score = calculate_location_score(
        profile=profile,
        job_offer=job_offer,
    )

    matching_score = calculate_final_score(
        skills_score=skills_score,
        experience_score=experience_score,
        work_mode_score=work_mode_score,
        location_score=location_score,
    )

    strengths = build_strengths(
        skills_score=skills_score,
        experience_score=experience_score,
        work_mode_score=work_mode_score,
        location_score=location_score,
        matching_skills=matching_skills,
    )

    weaknesses = build_weaknesses(
        skills_score=skills_score,
        experience_score=experience_score,
        work_mode_score=work_mode_score,
        location_score=location_score,
        missing_skills=missing_skills,
    )
    explanations = build_explanations(
        skills_score=skills_score,
        experience_score=experience_score,
        work_mode_score=work_mode_score,
        location_score=location_score,
        matching_skills=matching_skills,
        missing_skills=missing_skills,
    )
    opportunity_analysis = build_opportunity_analysis(
        matching_score=matching_score,
    )

    return MatchingResult(
        profile_id=profile_id,
        job_offer_id=job_offer_id,
        matching_score=matching_score,
        skills_score=skills_score,
        experience_score=experience_score,
        work_mode_score=work_mode_score,
        location_score=location_score,
        matching_skills=matching_skills,
        missing_skills=missing_skills,
        strengths=strengths,
        weaknesses=weaknesses,
        explanations=explanations,
        opportunity_analysis=opportunity_analysis,
    )


def rank_job_offers_for_profile(
    profile_id: int,
    db: Session,
) -> list[RankedJobOffer]:
    job_offers = db.query(JobOffer).all()

    ranked_job_offers = []

    for job_offer in job_offers:
        matching_result = calculate_matching_result(
            profile_id=profile_id,
            job_offer_id=job_offer.id,
            db=db,
        )

        ranked_job_offers.append(
            RankedJobOffer(
                job_offer_id=job_offer.id,
                title=job_offer.title,
                matching_score=matching_result.matching_score,
                skills_score=matching_result.skills_score,
                experience_score=matching_result.experience_score,
                work_mode_score=matching_result.work_mode_score,
                location_score=matching_result.location_score,
                matching_skills=matching_result.matching_skills,
                missing_skills=matching_result.missing_skills,
            )
        )

    ranked_job_offers.sort(
        key=lambda item: item.matching_score,
        reverse=True,
    )

    return ranked_job_offers


def calculate_skills_score(
    matching_ids: set[int],
    job_offer_skill_ids: set[int],
) -> float:
    if len(job_offer_skill_ids) == 0:
        return 0.0

    return round(
        (
            len(matching_ids)
            / len(job_offer_skill_ids)
        ) * 100,
        2,
    )


def calculate_experience_score(
    profile: Profile | None,
    job_offer: JobOffer | None,
) -> float:
    if profile is None or job_offer is None:
        return 50.0

    required_years = get_required_years_from_seniority(
        job_offer.seniority
    )

    if required_years is None:
        return 50.0

    if required_years == 0:
        return 100.0

    profile_years = profile.years_of_experience or 0

    if profile_years >= required_years:
        return 100.0

    ratio = profile_years / required_years

    if ratio >= 0.75:
        return 75.0

    if ratio >= 0.50:
        return 50.0

    return 25.0


def get_required_years_from_seniority(
    seniority: str | None,
) -> int | None:
    if seniority is None:
        return None

    normalized_seniority = normalize_text(
        seniority
    )

    if is_unknown(normalized_seniority):
        return None

    junior_values = {
        "intern",
        "internship",
        "apprentice",
        "apprenticeship",
        "alternance",
        "alternant",
        "junior",
        "entry",
        "entry-level",
        "debutant",
        "débutant",
    }

    mid_values = {
        "mid",
        "middle",
        "confirmed",
        "confirme",
        "confirmé",
        "intermediate",
    }

    senior_values = {
        "senior",
        "experienced",
        "experimente",
        "expérimenté",
    }

    lead_values = {
        "lead",
        "principal",
        "manager",
        "head",
    }

    executive_values = {
        "director",
        "executive",
        "vp",
        "c-level",
    }

    if normalized_seniority in junior_values:
        return 1

    if normalized_seniority in mid_values:
        return 3

    if normalized_seniority in senior_values:
        return 5

    if normalized_seniority in lead_values:
        return 7

    if normalized_seniority in executive_values:
        return 10

    return None


def calculate_work_mode_score(
    profile: Profile | None,
    job_offer: JobOffer | None,
) -> float:
    if profile is None or job_offer is None:
        return 50.0

    profile_preference = normalize_work_mode(
        profile.remote_preference
    )

    offer_work_mode = normalize_work_mode(
        job_offer.work_mode
    )

    if (
        profile_preference == "unknown"
        or offer_work_mode == "unknown"
    ):
        return 50.0

    if profile_preference == offer_work_mode:
        return 100.0

    compatible_pairs = {
        ("remote", "hybrid"),
        ("hybrid", "remote"),
        ("hybrid", "onsite"),
        ("onsite", "hybrid"),
    }

    if (
        profile_preference,
        offer_work_mode,
    ) in compatible_pairs:
        return 50.0

    return 0.0


def calculate_location_score(
    profile: Profile | None,
    job_offer: JobOffer | None,
) -> float:
    if profile is None or job_offer is None:
        return 50.0

    offer_work_mode = normalize_work_mode(
        job_offer.work_mode
    )

    if offer_work_mode == "remote":
        return 100.0

    profile_location = normalize_text(
        profile.location
    )

    preferred_countries = normalize_text(
        profile.preferred_countries
    )

    offer_location = normalize_text(
        job_offer.location
    )

    offer_city = normalize_text(
        job_offer.city
    )

    offer_region = normalize_text(
        job_offer.region
    )

    offer_country = normalize_text(
        job_offer.country
    )

    if is_unknown(profile_location):
        return 50.0

    if (
        is_unknown(offer_location)
        and is_unknown(offer_city)
        and is_unknown(offer_region)
        and is_unknown(offer_country)
    ):
        return 50.0

    if (
        offer_city
        and not is_unknown(offer_city)
        and offer_city in profile_location
    ):
        return 100.0

    if (
        offer_location
        and not is_unknown(offer_location)
        and profile_location in offer_location
    ):
        return 100.0

    if (
        offer_region
        and not is_unknown(offer_region)
        and offer_region in profile_location
    ):
        return 75.0

    if (
        offer_country
        and not is_unknown(offer_country)
        and offer_country in profile_location
    ):
        return 50.0

    if (
        offer_country
        and not is_unknown(offer_country)
        and offer_country in preferred_countries
    ):
        return 50.0

    return 0.0


def calculate_final_score(
    skills_score: float,
    experience_score: float,
    work_mode_score: float,
    location_score: float,
) -> float:
    return round(
        (
            skills_score * SKILLS_WEIGHT
            + experience_score * EXPERIENCE_WEIGHT
            + work_mode_score * WORK_MODE_WEIGHT
            + location_score * LOCATION_WEIGHT
        ),
        2,
    )


def build_strengths(
    skills_score: float,
    experience_score: float,
    work_mode_score: float,
    location_score: float,
    matching_skills: list[str],
) -> list[str]:
    strengths = []

    if skills_score >= 75:
        strengths.append(
            "Strong skills alignment."
        )

    if matching_skills:
        strengths.append(
            "The profile matches required skills."
        )

    if experience_score >= 75:
        strengths.append(
            "Experience level is compatible with the opportunity."
        )

    if work_mode_score >= 75:
        strengths.append(
            "Work mode is compatible with the profile preference."
        )

    if location_score >= 75:
        strengths.append(
            "Location is compatible with the profile."
        )

    return strengths


def build_weaknesses(
    skills_score: float,
    experience_score: float,
    work_mode_score: float,
    location_score: float,
    missing_skills: list[str],
) -> list[str]:
    weaknesses = []

    if skills_score < 50:
        weaknesses.append(
            "Skills alignment is limited."
        )

    if missing_skills:
        weaknesses.append(
            "Some required skills are missing."
        )

    if experience_score < 50:
        weaknesses.append(
            "Experience level may be below the expected level."
        )

    if work_mode_score < 50:
        weaknesses.append(
            "Work mode may not match the profile preference."
        )

    if location_score < 50:
        weaknesses.append(
            "Location may not match the profile preference."
        )

    return weaknesses

def build_explanations(
    skills_score: float,
    experience_score: float,
    work_mode_score: float,
    location_score: float,
    matching_skills: list[str],
    missing_skills: list[str],
) -> list[ScoreExplanation]:
    return [
        ScoreExplanation(
            criterion="skills",
            score=skills_score,
            message=(
                f"{len(matching_skills)} matching skills "
                f"and {len(missing_skills)} missing skills."
            ),
        ),
        ScoreExplanation(
            criterion="experience",
            score=experience_score,
            message=(
                "Experience score calculated from profile "
                "experience and job seniority."
            ),
        ),
        ScoreExplanation(
            criterion="work_mode",
            score=work_mode_score,
            message=(
                "Work mode compatibility between profile "
                "preference and opportunity."
            ),
        ),
        ScoreExplanation(
            criterion="location",
            score=location_score,
            message=(
                "Location compatibility between profile "
                "and opportunity."
            ),
        ),
    ]

def build_opportunity_analysis(
    matching_score: float,
) -> OpportunityAnalysis:
    if matching_score >= 80:
        return OpportunityAnalysis(
            verdict="excellent",
            recommendation="apply_now",
            summary="Highly compatible opportunity.",
        )

    if matching_score >= 60:
        return OpportunityAnalysis(
            verdict="good",
            recommendation="consider",
            summary="Opportunity looks compatible.",
        )

    if matching_score >= 40:
        return OpportunityAnalysis(
            verdict="moderate",
            recommendation="review",
            summary="Opportunity requires further review.",
        )

    return OpportunityAnalysis(
        verdict="weak",
        recommendation="low_priority",
        summary="Opportunity has limited compatibility.",
    )

def normalize_work_mode(
    value: str | None,
) -> str:
    normalized_value = normalize_text(
        value
    )

    if is_unknown(normalized_value):
        return "unknown"

    if (
        "remote" in normalized_value
        or "full remote" in normalized_value
        or "teletravail" in normalized_value
        or "télétravail" in normalized_value
    ):
        return "remote"

    if (
        "hybrid" in normalized_value
        or "hybride" in normalized_value
    ):
        return "hybrid"

    if (
        "onsite" in normalized_value
        or "on-site" in normalized_value
        or "site" == normalized_value
        or "presentiel" in normalized_value
        or "présentiel" in normalized_value
    ):
        return "onsite"

    return normalized_value


def normalize_text(
    value: str | None,
) -> str:
    if value is None:
        return ""

    return value.strip().lower()


def is_unknown(
    value: str | None,
) -> bool:
    if value is None:
        return True

    normalized_value = normalize_text(
        value
    )

    return normalized_value in {
        "",
        "unknown",
        "n/a",
        "na",
        "none",
        "null",
    }
    
