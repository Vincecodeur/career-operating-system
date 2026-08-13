from datetime import date
from datetime import datetime
from pathlib import Path

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.certifications.models import Certification
from app.certifications.models import ProfileCertification
from app.cv.models import CV
from app.cv.parsing_schemas import ParsedCVData
from app.cv.parsing_schemas import ParsedCVExperience
from app.cv.parsing_service import CVParsingError
from app.cv.parsing_service import parse_cv_file
from app.experience.models import WorkExperience
from app.languages.models import Language
from app.languages.models import ProfileLanguage
from app.profile.models import Profile
from app.profile.profile_skill_models import ProfileSkill
from app.profile_enrichment.enums import ProfileEnrichmentProposalStatus
from app.profile_enrichment.enums import ProfileEnrichmentProposalType
from app.profile_enrichment.models import ProfileEnrichmentProposal
from app.skills.models import Skill


DEFAULT_SKILL_LEVEL = "Intermediate"
DEFAULT_LANGUAGE_LEVEL = "Unknown"
DEFAULT_EXPERIENCE_COMPANY = "Unknown"
DEFAULT_EXPERIENCE_START_DATE = date(1900, 1, 1)


def normalize_value(
    value: str | None,
) -> str:
    if value is None:
        return ""

    return " ".join(
        value.strip().lower().split(),
    )


def get_cv_or_404(
    cv_id: int,
    db: Session,
) -> CV:
    cv = db.query(CV).filter(
        CV.id == cv_id,
    ).first()

    if cv is None:
        raise HTTPException(
            status_code=404,
            detail="CV not found.",
        )

    return cv


def get_profile_or_404(
    profile_id: int,
    db: Session,
) -> Profile:
    profile = db.query(Profile).filter(
        Profile.id == profile_id,
    ).first()

    if profile is None:
        raise HTTPException(
            status_code=404,
            detail="Profile not found.",
        )

    return profile


def get_proposal_or_404(
    proposal_id: int,
    db: Session,
) -> ProfileEnrichmentProposal:
    proposal = db.query(ProfileEnrichmentProposal).filter(
        ProfileEnrichmentProposal.id == proposal_id,
    ).first()

    if proposal is None:
        raise HTTPException(
            status_code=404,
            detail="Enrichment proposal not found.",
        )

    return proposal


def ensure_pending_proposal(
    proposal: ProfileEnrichmentProposal,
) -> None:
    if proposal.status != ProfileEnrichmentProposalStatus.PENDING.value:
        raise HTTPException(
            status_code=400,
            detail="Only pending enrichment proposals can be processed.",
        )


def proposal_exists(
    profile_id: int,
    cv_id: int,
    proposal_type: str,
    target_field: str,
    normalized_value: str,
    db: Session,
) -> bool:
    existing_proposal = db.query(ProfileEnrichmentProposal).filter(
        ProfileEnrichmentProposal.profile_id == profile_id,
        ProfileEnrichmentProposal.cv_id == cv_id,
        ProfileEnrichmentProposal.proposal_type == proposal_type,
        ProfileEnrichmentProposal.target_field == target_field,
        ProfileEnrichmentProposal.normalized_value == normalized_value,
        ProfileEnrichmentProposal.status
        == ProfileEnrichmentProposalStatus.PENDING.value,
    ).first()

    return existing_proposal is not None


def create_proposal_if_missing(
    profile_id: int,
    cv_id: int,
    proposal_type: ProfileEnrichmentProposalType,
    source_field: str,
    target_field: str,
    observed_value: str,
    proposed_value: str,
    current_profile_value: str | None,
    reference_id: int | None,
    conflict_detected: bool,
    db: Session,
) -> ProfileEnrichmentProposal | None:
    normalized_value = normalize_value(proposed_value)

    if not normalized_value:
        return None

    if proposal_exists(
        profile_id=profile_id,
        cv_id=cv_id,
        proposal_type=proposal_type.value,
        target_field=target_field,
        normalized_value=normalized_value,
        db=db,
    ):
        return None

    proposal = ProfileEnrichmentProposal(
        profile_id=profile_id,
        cv_id=cv_id,
        proposal_type=proposal_type.value,
        status=ProfileEnrichmentProposalStatus.PENDING.value,
        source_field=source_field,
        target_field=target_field,
        observed_value=observed_value,
        normalized_value=normalized_value,
        current_profile_value=current_profile_value,
        proposed_value=proposed_value,
        reference_id=reference_id,
        conflict_detected=conflict_detected,
    )

    db.add(proposal)

    return proposal


def find_skill_by_name(
    name: str,
    db: Session,
) -> Skill | None:
    normalized_name = normalize_value(name)

    return db.query(Skill).filter(
        Skill.name.ilike(normalized_name),
    ).first()


def find_language_by_name(
    name: str,
    db: Session,
) -> Language | None:
    normalized_name = normalize_value(name)

    return db.query(Language).filter(
        Language.name.ilike(normalized_name),
    ).first()


def find_certification_by_name(
    name: str,
    db: Session,
) -> Certification | None:
    normalized_name = normalize_value(name)

    return db.query(Certification).filter(
        Certification.name.ilike(normalized_name),
    ).first()


def profile_has_skill(
    profile_id: int,
    skill_id: int,
    db: Session,
) -> bool:
    profile_skill = db.query(ProfileSkill).filter(
        ProfileSkill.profile_id == profile_id,
        ProfileSkill.skill_id == skill_id,
    ).first()

    return profile_skill is not None


def profile_has_language(
    profile_id: int,
    language_id: int,
    db: Session,
) -> bool:
    profile_language = db.query(ProfileLanguage).filter(
        ProfileLanguage.profile_id == profile_id,
        ProfileLanguage.language_id == language_id,
    ).first()

    return profile_language is not None


def profile_has_certification(
    profile_id: int,
    certification_id: int,
    db: Session,
) -> bool:
    profile_certification = db.query(ProfileCertification).filter(
        ProfileCertification.profile_id == profile_id,
        ProfileCertification.certification_id == certification_id,
    ).first()

    return profile_certification is not None


def profile_has_similar_experience(
    profile_id: int,
    parsed_experience: ParsedCVExperience,
    db: Session,
) -> bool:
    existing_experiences = db.query(WorkExperience).filter(
        WorkExperience.profile_id == profile_id,
    ).all()

    parsed_value = normalize_value(
        format_parsed_experience(parsed_experience),
    )

    if not parsed_value:
        return True

    for existing_experience in existing_experiences:
        existing_value = normalize_value(
            " ".join(
                [
                    existing_experience.company_name,
                    existing_experience.job_title,
                    existing_experience.description,
                ],
            ),
        )

        if parsed_value in existing_value or existing_value in parsed_value:
            return True

    return False


def format_parsed_experience(
    parsed_experience: ParsedCVExperience,
) -> str:
    values = [
        parsed_experience.title,
        parsed_experience.company,
        parsed_experience.start_date,
        parsed_experience.end_date,
        parsed_experience.description,
    ]

    clean_values = [
        value
        for value in values
        if value
    ]

    return " | ".join(clean_values)


def generate_profile_field_proposals(
    profile: Profile,
    cv: CV,
    parsed_data: ParsedCVData,
    db: Session,
) -> list[ProfileEnrichmentProposal]:
    proposals: list[ProfileEnrichmentProposal] = []

    field_mappings = [
        (
            "full_name",
            "full_name",
            parsed_data.full_name,
            profile.full_name,
        ),
        (
            "professional_title",
            "current_title",
            parsed_data.professional_title,
            profile.current_title,
        ),
    ]

    for source_field, target_field, observed_value, current_value in field_mappings:
        if not observed_value:
            continue

        if normalize_value(observed_value) == normalize_value(current_value):
            continue

        proposal = create_proposal_if_missing(
            profile_id=profile.id,
            cv_id=cv.id,
            proposal_type=ProfileEnrichmentProposalType.PROFILE_FIELD,
            source_field=source_field,
            target_field=target_field,
            observed_value=observed_value,
            proposed_value=observed_value,
            current_profile_value=current_value,
            reference_id=None,
            conflict_detected=bool(current_value),
            db=db,
        )

        if proposal is not None:
            proposals.append(proposal)

    return proposals


def generate_skill_proposals(
    profile: Profile,
    cv: CV,
    parsed_data: ParsedCVData,
    db: Session,
) -> list[ProfileEnrichmentProposal]:
    proposals: list[ProfileEnrichmentProposal] = []

    for skill_name in parsed_data.skills:
        skill = find_skill_by_name(
            skill_name,
            db,
        )

        if skill is not None and profile_has_skill(
            profile.id,
            skill.id,
            db,
        ):
            continue

        proposal = create_proposal_if_missing(
            profile_id=profile.id,
            cv_id=cv.id,
            proposal_type=ProfileEnrichmentProposalType.SKILL,
            source_field="skills",
            target_field="profile_skill",
            observed_value=skill_name,
            proposed_value=skill_name,
            current_profile_value=None,
            reference_id=skill.id if skill is not None else None,
            conflict_detected=False,
            db=db,
        )

        if proposal is not None:
            proposals.append(proposal)

    return proposals


def generate_language_proposals(
    profile: Profile,
    cv: CV,
    parsed_data: ParsedCVData,
    db: Session,
) -> list[ProfileEnrichmentProposal]:
    proposals: list[ProfileEnrichmentProposal] = []

    for language_name in parsed_data.languages:
        language = find_language_by_name(
            language_name,
            db,
        )

        if language is not None and profile_has_language(
            profile.id,
            language.id,
            db,
        ):
            continue

        proposal = create_proposal_if_missing(
            profile_id=profile.id,
            cv_id=cv.id,
            proposal_type=ProfileEnrichmentProposalType.LANGUAGE,
            source_field="languages",
            target_field="profile_language",
            observed_value=language_name,
            proposed_value=language_name,
            current_profile_value=None,
            reference_id=language.id if language is not None else None,
            conflict_detected=False,
            db=db,
        )

        if proposal is not None:
            proposals.append(proposal)

    return proposals


def generate_certification_proposals(
    profile: Profile,
    cv: CV,
    parsed_data: ParsedCVData,
    db: Session,
) -> list[ProfileEnrichmentProposal]:
    proposals: list[ProfileEnrichmentProposal] = []

    for certification_name in parsed_data.certifications:
        certification = find_certification_by_name(
            certification_name,
            db,
        )

        if certification is not None and profile_has_certification(
            profile.id,
            certification.id,
            db,
        ):
            continue

        proposal = create_proposal_if_missing(
            profile_id=profile.id,
            cv_id=cv.id,
            proposal_type=ProfileEnrichmentProposalType.CERTIFICATION,
            source_field="certifications",
            target_field="profile_certification",
            observed_value=certification_name,
            proposed_value=certification_name,
            current_profile_value=None,
            reference_id=certification.id if certification is not None else None,
            conflict_detected=False,
            db=db,
        )

        if proposal is not None:
            proposals.append(proposal)

    return proposals


def generate_experience_proposals(
    profile: Profile,
    cv: CV,
    parsed_data: ParsedCVData,
    db: Session,
) -> list[ProfileEnrichmentProposal]:
    proposals: list[ProfileEnrichmentProposal] = []

    for parsed_experience in parsed_data.experiences:
        proposed_value = format_parsed_experience(
            parsed_experience,
        )

        if not proposed_value:
            continue

        if profile_has_similar_experience(
            profile.id,
            parsed_experience,
            db,
        ):
            continue

        proposal = create_proposal_if_missing(
            profile_id=profile.id,
            cv_id=cv.id,
            proposal_type=ProfileEnrichmentProposalType.EXPERIENCE,
            source_field="experiences",
            target_field="work_experience",
            observed_value=proposed_value,
            proposed_value=proposed_value,
            current_profile_value=None,
            reference_id=None,
            conflict_detected=False,
            db=db,
        )

        if proposal is not None:
            proposals.append(proposal)

    return proposals


def generate_proposals_for_cv(
    cv_id: int,
    db: Session,
) -> list[ProfileEnrichmentProposal]:
    cv = get_cv_or_404(
        cv_id,
        db,
    )

    profile = get_profile_or_404(
        cv.profile_id,
        db,
    )

    try:
        _, parsed_data = parse_cv_file(
            Path(cv.storage_path),
        )
    except CVParsingError as exc:
        cv.parsing_status = "FAILED"
        db.commit()

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    cv.parsing_status = "COMPLETED"

    proposals: list[ProfileEnrichmentProposal] = []
    proposals.extend(
        generate_profile_field_proposals(
            profile,
            cv,
            parsed_data,
            db,
        ),
    )
    proposals.extend(
        generate_skill_proposals(
            profile,
            cv,
            parsed_data,
            db,
        ),
    )
    proposals.extend(
        generate_language_proposals(
            profile,
            cv,
            parsed_data,
            db,
        ),
    )
    proposals.extend(
        generate_certification_proposals(
            profile,
            cv,
            parsed_data,
            db,
        ),
    )
    proposals.extend(
        generate_experience_proposals(
            profile,
            cv,
            parsed_data,
            db,
        ),
    )

    db.commit()

    for proposal in proposals:
        db.refresh(proposal)

    db.refresh(cv)

    return proposals


def list_proposals_for_profile(
    profile_id: int,
    db: Session,
) -> list[ProfileEnrichmentProposal]:
    profile = get_profile_or_404(
        profile_id,
        db,
    )

    return db.query(ProfileEnrichmentProposal).filter(
        ProfileEnrichmentProposal.profile_id == profile_id,
    ).order_by(
        ProfileEnrichmentProposal.status.asc(),
        ProfileEnrichmentProposal.created_at.desc(),
    ).all()


def accept_profile_field_proposal(
    proposal: ProfileEnrichmentProposal,
    value_to_apply: str,
    db: Session,
) -> None:
    profile = get_profile_or_404(
        proposal.profile_id,
        db,
    )

    if proposal.target_field == "full_name":
        profile.full_name = value_to_apply
        return

    if proposal.target_field == "current_title":
        profile.current_title = value_to_apply
        return

    raise HTTPException(
        status_code=400,
        detail="Unsupported profile field enrichment proposal.",
    )


def accept_skill_proposal(
    proposal: ProfileEnrichmentProposal,
    db: Session,
) -> None:
    skill: Skill | None = None

    if proposal.reference_id is not None:
        skill = db.query(Skill).filter(
            Skill.id == proposal.reference_id,
        ).first()

        if skill is None:
            raise HTTPException(
                status_code=404,
                detail="Skill not found.",
            )

    if skill is None:
        skill = find_skill_by_name(
            proposal.proposed_value,
            db,
        )

    if skill is None:
        raise HTTPException(
            status_code=400,
            detail=(
                "Skill not found in catalog. "
                "Create or map the skill before accepting the proposal."
            ),
        )

    proposal.reference_id = skill.id

    if profile_has_skill(
        proposal.profile_id,
        skill.id,
        db,
    ):
        return

    profile_skill = ProfileSkill(
        profile_id=proposal.profile_id,
        skill_id=skill.id,
        years_of_experience=0,
        self_assessment_level=DEFAULT_SKILL_LEVEL,
    )

    db.add(profile_skill)


def accept_language_proposal(
    proposal: ProfileEnrichmentProposal,
    db: Session,
) -> None:
    language: Language | None = None

    if proposal.reference_id is not None:
        language = db.query(Language).filter(
            Language.id == proposal.reference_id,
        ).first()

        if language is None:
            raise HTTPException(
                status_code=404,
                detail="Language not found.",
            )

    if language is None:
        language = find_language_by_name(
            proposal.proposed_value,
            db,
        )

    if language is None:
        language = Language(
            name=proposal.proposed_value,
        )
        db.add(language)
        db.flush()

    proposal.reference_id = language.id

    if profile_has_language(
        proposal.profile_id,
        language.id,
        db,
    ):
        return

    profile_language = ProfileLanguage(
        profile_id=proposal.profile_id,
        language_id=language.id,
        proficiency_level=DEFAULT_LANGUAGE_LEVEL,
    )

    db.add(profile_language)


def accept_certification_proposal(
    proposal: ProfileEnrichmentProposal,
    db: Session,
) -> None:
    certification: Certification | None = None

    if proposal.reference_id is not None:
        certification = db.query(Certification).filter(
            Certification.id == proposal.reference_id,
        ).first()

        if certification is None:
            raise HTTPException(
                status_code=404,
                detail="Certification not found.",
            )

    if certification is None:
        certification = find_certification_by_name(
            proposal.proposed_value,
            db,
        )

    if certification is None:
        certification = Certification(
            name=proposal.proposed_value,
            issuing_organization=None,
        )
        db.add(certification)
        db.flush()

    proposal.reference_id = certification.id

    if profile_has_certification(
        proposal.profile_id,
        certification.id,
        db,
    ):
        return

    profile_certification = ProfileCertification(
        profile_id=proposal.profile_id,
        certification_id=certification.id,
        obtained_date=None,
        expiration_date=None,
        credential_id=None,
    )

    db.add(profile_certification)


def accept_experience_proposal(
    proposal: ProfileEnrichmentProposal,
    value_to_apply: str,
    db: Session,
) -> None:
    work_experience = WorkExperience(
        profile_id=proposal.profile_id,
        company_name=DEFAULT_EXPERIENCE_COMPANY,
        job_title=value_to_apply[:255],
        start_date=DEFAULT_EXPERIENCE_START_DATE,
        end_date=None,
        is_current_position=False,
        description=value_to_apply,
    )

    db.add(work_experience)


def accept_proposal(
    proposal_id: int,
    proposed_value_override: str | None,
    db: Session,
) -> ProfileEnrichmentProposal:
    proposal = get_proposal_or_404(
        proposal_id,
        db,
    )

    ensure_pending_proposal(
        proposal,
    )

    value_to_apply = (
        proposed_value_override
        if proposed_value_override
        else proposal.proposed_value
    )

    if proposal.proposal_type == ProfileEnrichmentProposalType.PROFILE_FIELD.value:
        accept_profile_field_proposal(
            proposal,
            value_to_apply,
            db,
        )
    elif proposal.proposal_type == ProfileEnrichmentProposalType.SKILL.value:
        accept_skill_proposal(
            proposal,
            db,
        )
    elif proposal.proposal_type == ProfileEnrichmentProposalType.LANGUAGE.value:
        accept_language_proposal(
            proposal,
            db,
        )
    elif proposal.proposal_type == ProfileEnrichmentProposalType.CERTIFICATION.value:
        accept_certification_proposal(
            proposal,
            db,
        )
    elif proposal.proposal_type == ProfileEnrichmentProposalType.EXPERIENCE.value:
        accept_experience_proposal(
            proposal,
            value_to_apply,
            db,
        )
    else:
        raise HTTPException(
            status_code=400,
            detail="Unsupported enrichment proposal type.",
        )

    proposal.proposed_value = value_to_apply
    proposal.normalized_value = normalize_value(value_to_apply)
    proposal.status = ProfileEnrichmentProposalStatus.ACCEPTED.value
    proposal.validated_at = datetime.utcnow()

    db.commit()
    db.refresh(proposal)

    return proposal


def reject_proposal(
    proposal_id: int,
    db: Session,
) -> ProfileEnrichmentProposal:
    proposal = get_proposal_or_404(
        proposal_id,
        db,
    )

    ensure_pending_proposal(
        proposal,
    )

    proposal.status = ProfileEnrichmentProposalStatus.REJECTED.value
    proposal.validated_at = datetime.utcnow()

    db.commit()
    db.refresh(proposal)

    return proposal