from uuid import uuid4

from fastapi.testclient import TestClient

from app.core.database import create_tables
from app.cv.parsing_schemas import ParsedCVData
from app.cv.parsing_schemas import ParsedCVExperience
from app.main import app
from app.profile_enrichment import service as profile_enrichment_service


create_tables()

client = TestClient(app)


def create_test_profile(authenticated_headers):
    profile_name = f"Profile_{uuid4()}"

    response = client.post(
        "/profiles",
        json={
            "profile_name": profile_name,
            "full_name": "Test User",
            "current_title": "Product Manager",
            "location": "Paris",
            "years_of_experience": 8,
            "target_role_short_term": "Senior Product Manager",
            "target_role_long_term": "Head of Product",
            "remote_preference": "Hybrid",
            "preferred_countries": "France",
        },
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    return response.json()


def create_test_cv(
    profile_id: int,
    authenticated_headers,
    file_name: str = "test-cv.pdf",
    content: bytes = b"Test CV content",
    language: str = "fr",
    version_label: str = "Test Version",
    is_default: bool = False,
):
    response = client.post(
        f"/profiles/{profile_id}/cvs",
        files={
            "cv_file": (
                file_name,
                content,
                "application/pdf",
            ),
        },
        data={
            "language": language,
            "version_label": version_label,
            "is_default": str(is_default).lower(),
        },
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    return response.json()


def create_test_skill(
    name: str | None = None,
):
    skill_name = name or f"Skill_{uuid4()}"

    response = client.post(
        "/skills",
        json={
            "name": skill_name,
            "category": "Technical",
        },
    )

    assert response.status_code == 200

    return response.json()


def get_profile_soft_skills(
    profile_id: int,
    authenticated_headers,
):
    response = client.get(
        f"/profiles/{profile_id}/soft-skills",
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    return response.json()


def create_test_language(
    name: str | None = None,
):
    language_name = name or f"Language_{uuid4()}"

    response = client.post(
        "/languages",
        json={
            "name": language_name,
        },
    )

    assert response.status_code == 200

    return response.json()


def create_test_certification(
    name: str | None = None,
):
    certification_name = name or f"Certification_{uuid4()}"

    response = client.post(
        "/certifications",
        json={
            "name": certification_name,
            "issuing_organization": "Test Organization",
        },
    )

    assert response.status_code == 200

    return response.json()


def build_parsed_cv_data(
    skill_name: str,
    language_name: str,
    certification_name: str,
) -> ParsedCVData:
    return ParsedCVData(
        full_name="Parsed Test User",
        professional_title="Solution Architect",
        summary="Experienced professional profile extracted from CV.",
        skills=[
            skill_name,
        ],
        languages=[
            language_name,
        ],
        certifications=[
            certification_name,
        ],
        experiences=[
            ParsedCVExperience(
                title="Technical Partnerships Manager",
                company="Test Company",
                start_date="2020",
                end_date=None,
                description="Managed technical partnerships and integrations.",
            ),
        ],
    )


def mock_parse_cv_file(
    monkeypatch,
    parsed_data: ParsedCVData,
):
    def fake_parse_cv_file(file_path):
        return (
            "Mock raw CV text",
            parsed_data,
        )

    monkeypatch.setattr(
        profile_enrichment_service,
        "parse_cv_file",
        fake_parse_cv_file,
    )


def test_generate_cv_enrichment_proposals_cv_not_found():
    response = client.post(
        "/cvs/99999999/enrichment/generate"
    )

    assert response.status_code == 404


def test_get_profile_enrichment_proposals_profile_not_found():
    response = client.get(
        "/profiles/99999999/enrichment"
    )

    assert response.status_code == 404


def test_accept_proposal_not_found():
    response = client.post(
        "/enrichment/99999999/accept"
    )

    assert response.status_code == 404


def test_reject_proposal_not_found():
    response = client.post(
        "/enrichment/99999999/reject"
    )

    assert response.status_code == 404


def test_list_profile_enrichment_proposals_empty(authenticated_headers):
    profile = create_test_profile(authenticated_headers)

    response = client.get(
        f"/profiles/{profile['id']}/enrichment"
    )

    assert response.status_code == 200
    assert response.json() == []


def test_generate_cv_enrichment_proposals(
    monkeypatch,
    authenticated_headers,
):
    profile = create_test_profile(authenticated_headers)
    cv = create_test_cv(
        profile_id=profile["id"],
        authenticated_headers=authenticated_headers,
    )

    skill = create_test_skill()
    language = create_test_language()
    certification = create_test_certification()

    parsed_data = build_parsed_cv_data(
        skill_name=skill["name"],
        language_name=language["name"],
        certification_name=certification["name"],
    )

    mock_parse_cv_file(
        monkeypatch,
        parsed_data,
    )

    response = client.post(
        f"/cvs/{cv['id']}/enrichment/generate"
    )

    assert response.status_code == 200

    proposals = response.json()

    proposal_types = {
        proposal["proposal_type"]
        for proposal in proposals
    }

    assert "PROFILE_FIELD" in proposal_types
    assert "HARD_SKILL" in proposal_types
    assert "LANGUAGE" in proposal_types
    assert "CERTIFICATION" in proposal_types
    assert "EXPERIENCE" in proposal_types

    assert all(
        proposal["status"] == "PENDING"
        for proposal in proposals
    )


def test_generate_cv_enrichment_proposals_does_not_update_profile(
    monkeypatch,
    authenticated_headers,
):
    profile = create_test_profile(authenticated_headers)
    cv = create_test_cv(
        profile_id=profile["id"],
        authenticated_headers=authenticated_headers,
    )

    skill = create_test_skill()
    language = create_test_language()
    certification = create_test_certification()

    parsed_data = build_parsed_cv_data(
        skill_name=skill["name"],
        language_name=language["name"],
        certification_name=certification["name"],
    )

    mock_parse_cv_file(
        monkeypatch,
        parsed_data,
    )

    response = client.post(
        f"/cvs/{cv['id']}/enrichment/generate"
    )

    assert response.status_code == 200

    profile_response = client.get(
        f"/profiles/{profile['id']}",
        headers=authenticated_headers,
    )

    assert profile_response.status_code == 200

    updated_profile = profile_response.json()

    assert updated_profile["full_name"] == profile["full_name"]
    assert updated_profile["current_title"] == profile["current_title"]


def test_generate_cv_enrichment_proposals_avoids_duplicate_pending_proposals(
    monkeypatch,
    authenticated_headers,
):
    profile = create_test_profile(authenticated_headers)
    cv = create_test_cv(
        profile_id=profile["id"],
        authenticated_headers=authenticated_headers,
    )

    skill = create_test_skill()
    language = create_test_language()
    certification = create_test_certification()

    parsed_data = build_parsed_cv_data(
        skill_name=skill["name"],
        language_name=language["name"],
        certification_name=certification["name"],
    )

    mock_parse_cv_file(
        monkeypatch,
        parsed_data,
    )

    first_response = client.post(
        f"/cvs/{cv['id']}/enrichment/generate"
    )

    assert first_response.status_code == 200
    assert len(first_response.json()) > 0

    second_response = client.post(
        f"/cvs/{cv['id']}/enrichment/generate"
    )

    assert second_response.status_code == 200
    assert second_response.json() == []


def test_list_profile_enrichment_proposals_after_generation(
    monkeypatch,
    authenticated_headers,
):
    profile = create_test_profile(authenticated_headers)
    cv = create_test_cv(
        profile_id=profile["id"],
        authenticated_headers=authenticated_headers,
    )

    skill = create_test_skill()
    language = create_test_language()
    certification = create_test_certification()

    parsed_data = build_parsed_cv_data(
        skill_name=skill["name"],
        language_name=language["name"],
        certification_name=certification["name"],
    )

    mock_parse_cv_file(
        monkeypatch,
        parsed_data,
    )

    generate_response = client.post(
        f"/cvs/{cv['id']}/enrichment/generate"
    )

    assert generate_response.status_code == 200

    list_response = client.get(
        f"/profiles/{profile['id']}/enrichment"
    )

    assert list_response.status_code == 200

    proposals = list_response.json()

    assert isinstance(proposals, list)
    assert len(proposals) > 0

    assert all(
        proposal["profile_id"] == profile["id"]
        for proposal in proposals
    )


def get_first_pending_proposal(
    profile_id: int,
):
    response = client.get(
        f"/profiles/{profile_id}/enrichment"
    )

    assert response.status_code == 200

    proposals = response.json()

    pending_proposals = [
        proposal
        for proposal in proposals
        if proposal["status"] == "PENDING"
    ]

    assert len(pending_proposals) > 0

    return pending_proposals[0]


def test_reject_proposal(
    monkeypatch,
    authenticated_headers,
):
    profile = create_test_profile(authenticated_headers)
    cv = create_test_cv(
        profile_id=profile["id"],
        authenticated_headers=authenticated_headers,
    )

    skill = create_test_skill()
    language = create_test_language()
    certification = create_test_certification()

    parsed_data = build_parsed_cv_data(
        skill_name=skill["name"],
        language_name=language["name"],
        certification_name=certification["name"],
    )

    mock_parse_cv_file(
        monkeypatch,
        parsed_data,
    )

    client.post(
        f"/cvs/{cv['id']}/enrichment/generate"
    )

    proposal = get_first_pending_proposal(
        profile["id"],
    )

    response = client.post(
        f"/enrichment/{proposal['id']}/reject"
    )

    assert response.status_code == 200

    rejected_proposal = response.json()

    assert rejected_proposal["status"] == "REJECTED"
    assert rejected_proposal["validated_at"] is not None


def test_cannot_reject_already_processed_proposal(
    monkeypatch,
    authenticated_headers,
):
    profile = create_test_profile(authenticated_headers)
    cv = create_test_cv(
        profile_id=profile["id"],
        authenticated_headers=authenticated_headers,
    )

    skill = create_test_skill()
    language = create_test_language()
    certification = create_test_certification()

    parsed_data = build_parsed_cv_data(
        skill_name=skill["name"],
        language_name=language["name"],
        certification_name=certification["name"],
    )

    mock_parse_cv_file(
        monkeypatch,
        parsed_data,
    )

    client.post(
        f"/cvs/{cv['id']}/enrichment/generate"
    )

    proposal = get_first_pending_proposal(
        profile["id"],
    )

    first_response = client.post(
        f"/enrichment/{proposal['id']}/reject"
    )

    assert first_response.status_code == 200

    second_response = client.post(
        f"/enrichment/{proposal['id']}/reject"
    )

    assert second_response.status_code == 400


def test_accept_profile_field_proposal(
    monkeypatch,
    authenticated_headers,
):
    profile = create_test_profile(authenticated_headers)
    cv = create_test_cv(
        profile_id=profile["id"],
        authenticated_headers=authenticated_headers,
    )

    parsed_data = ParsedCVData(
        full_name="Updated Parsed User",
        professional_title="Solution Architect",
        summary="Summary",
        skills=[],
        languages=[],
        certifications=[],
        experiences=[],
    )

    mock_parse_cv_file(
        monkeypatch,
        parsed_data,
    )

    client.post(
        f"/cvs/{cv['id']}/enrichment/generate"
    )

    response = client.get(
        f"/profiles/{profile['id']}/enrichment"
    )

    proposals = response.json()

    profile_field_proposal = next(
        proposal
        for proposal in proposals
        if proposal["proposal_type"] == "PROFILE_FIELD"
    )

    accept_response = client.post(
        f"/enrichment/{profile_field_proposal['id']}/accept"
    )

    assert accept_response.status_code == 200

    accepted_proposal = accept_response.json()

    assert accepted_proposal["status"] == "ACCEPTED"


def test_accept_skill_proposal(
    monkeypatch,
    authenticated_headers,
):
    profile = create_test_profile(authenticated_headers)
    cv = create_test_cv(
        profile_id=profile["id"],
        authenticated_headers=authenticated_headers,
    )

    skill = create_test_skill()

    parsed_data = ParsedCVData(
        full_name=None,
        professional_title=None,
        summary=None,
        skills=[skill["name"]],
        languages=[],
        certifications=[],
        experiences=[],
    )

    mock_parse_cv_file(
        monkeypatch,
        parsed_data,
    )

    client.post(
        f"/cvs/{cv['id']}/enrichment/generate"
    )

    response = client.get(
        f"/profiles/{profile['id']}/enrichment"
    )

    proposals = response.json()

    skill_proposal = next(
        proposal
        for proposal in proposals
        if proposal["proposal_type"] == "HARD_SKILL"
    )

    accept_response = client.post(
        f"/enrichment/{skill_proposal['id']}/accept"
    )

    assert accept_response.status_code == 200

    accepted_proposal = accept_response.json()

    assert accepted_proposal["status"] == "ACCEPTED"


def test_accept_language_proposal(
    monkeypatch,
    authenticated_headers,
):
    profile = create_test_profile(authenticated_headers)
    cv = create_test_cv(
        profile_id=profile["id"],
        authenticated_headers=authenticated_headers,
    )

    language = create_test_language()

    parsed_data = ParsedCVData(
        full_name=None,
        professional_title=None,
        summary=None,
        skills=[],
        languages=[language["name"]],
        certifications=[],
        experiences=[],
    )

    mock_parse_cv_file(
        monkeypatch,
        parsed_data,
    )

    client.post(
        f"/cvs/{cv['id']}/enrichment/generate"
    )

    response = client.get(
        f"/profiles/{profile['id']}/enrichment"
    )

    proposals = response.json()

    language_proposal = next(
        proposal
        for proposal in proposals
        if proposal["proposal_type"] == "LANGUAGE"
    )

    accept_response = client.post(
        f"/enrichment/{language_proposal['id']}/accept"
    )

    assert accept_response.status_code == 200

    accepted_proposal = accept_response.json()

    assert accepted_proposal["status"] == "ACCEPTED"


def test_accept_certification_proposal(
    monkeypatch,
    authenticated_headers,
):
    profile = create_test_profile(authenticated_headers)
    cv = create_test_cv(
        profile_id=profile["id"],
        authenticated_headers=authenticated_headers,
    )

    certification = create_test_certification()

    parsed_data = ParsedCVData(
        full_name=None,
        professional_title=None,
        summary=None,
        skills=[],
        languages=[],
        certifications=[certification["name"]],
        experiences=[],
    )

    mock_parse_cv_file(
        monkeypatch,
        parsed_data,
    )

    client.post(
        f"/cvs/{cv['id']}/enrichment/generate"
    )

    response = client.get(
        f"/profiles/{profile['id']}/enrichment"
    )

    proposals = response.json()

    certification_proposal = next(
        proposal
        for proposal in proposals
        if proposal["proposal_type"] == "CERTIFICATION"
    )

    accept_response = client.post(
        f"/enrichment/{certification_proposal['id']}/accept"
    )

    assert accept_response.status_code == 200

    accepted_proposal = accept_response.json()

    assert accepted_proposal["status"] == "ACCEPTED"


def test_accept_experience_proposal(
    monkeypatch,
    authenticated_headers,
):
    profile = create_test_profile(authenticated_headers)
    cv = create_test_cv(
        profile_id=profile["id"],
        authenticated_headers=authenticated_headers,
    )

    parsed_data = ParsedCVData(
        full_name=None,
        professional_title=None,
        summary=None,
        skills=[],
        languages=[],
        certifications=[],
        experiences=[
            ParsedCVExperience(
                title="Technical Partnerships Manager",
                company="Example Company",
                start_date="2020",
                end_date=None,
                description="Partnership management",
            ),
        ],
    )

    mock_parse_cv_file(
        monkeypatch,
        parsed_data,
    )

    client.post(
        f"/cvs/{cv['id']}/enrichment/generate"
    )

    response = client.get(
        f"/profiles/{profile['id']}/enrichment"
    )

    proposals = response.json()

    experience_proposal = next(
        proposal
        for proposal in proposals
        if proposal["proposal_type"] == "EXPERIENCE"
    )

    accept_response = client.post(
        f"/enrichment/{experience_proposal['id']}/accept"
    )

    assert accept_response.status_code == 200

    accepted_proposal = accept_response.json()

    assert accepted_proposal["status"] == "ACCEPTED"


def test_cannot_accept_already_processed_proposal(
    monkeypatch,
    authenticated_headers,
):
    profile = create_test_profile(authenticated_headers)
    cv = create_test_cv(
        profile_id=profile["id"],
        authenticated_headers=authenticated_headers,
    )

    skill = create_test_skill()

    parsed_data = ParsedCVData(
        full_name=None,
        professional_title=None,
        summary=None,
        skills=[skill["name"]],
        languages=[],
        certifications=[],
        experiences=[],
    )

    mock_parse_cv_file(
        monkeypatch,
        parsed_data,
    )

    client.post(
        f"/cvs/{cv['id']}/enrichment/generate"
    )

    response = client.get(
        f"/profiles/{profile['id']}/enrichment"
    )

    proposals = response.json()

    proposal = next(
        proposal
        for proposal in proposals
        if proposal["proposal_type"] == "HARD_SKILL"
    )

    first_response = client.post(
        f"/enrichment/{proposal['id']}/accept"
    )

    assert first_response.status_code == 200

    second_response = client.post(
        f"/enrichment/{proposal['id']}/accept"
    )

    assert second_response.status_code == 400


def test_generate_soft_skill_proposal_for_skill_not_in_catalog(
    monkeypatch,
    authenticated_headers,
):
    profile = create_test_profile(authenticated_headers)
    cv = create_test_cv(
        profile_id=profile["id"],
        authenticated_headers=authenticated_headers,
    )

    language = create_test_language()
    certification = create_test_certification()

    soft_skill_name = "Leadership"

    parsed_data = build_parsed_cv_data(
        skill_name=soft_skill_name,
        language_name=language["name"],
        certification_name=certification["name"],
    )

    mock_parse_cv_file(
        monkeypatch,
        parsed_data,
    )

    response = client.post(
        f"/cvs/{cv['id']}/enrichment/generate"
    )

    assert response.status_code == 200

    proposals = response.json()

    soft_skill_proposals = [
        proposal
        for proposal in proposals
        if proposal["proposal_type"] == "SOFT_SKILL"
    ]

    assert len(soft_skill_proposals) == 1
    assert soft_skill_proposals[0]["proposed_value"] == soft_skill_name


def test_accept_soft_skill_proposal_creates_profile_soft_skill(
    monkeypatch,
    authenticated_headers,
):
    profile = create_test_profile(authenticated_headers)
    cv = create_test_cv(
        profile_id=profile["id"],
        authenticated_headers=authenticated_headers,
    )

    language = create_test_language()
    certification = create_test_certification()

    soft_skill_name = "Communication"

    parsed_data = build_parsed_cv_data(
        skill_name=soft_skill_name,
        language_name=language["name"],
        certification_name=certification["name"],
    )

    mock_parse_cv_file(
        monkeypatch,
        parsed_data,
    )

    generate_response = client.post(
        f"/cvs/{cv['id']}/enrichment/generate"
    )

    assert generate_response.status_code == 200

    proposals = generate_response.json()

    soft_skill_proposal = next(
        proposal
        for proposal in proposals
        if proposal["proposal_type"] == "SOFT_SKILL"
    )

    accept_response = client.post(
        f"/enrichment/{soft_skill_proposal['id']}/accept"
    )

    assert accept_response.status_code == 200

    accepted_proposal = accept_response.json()

    assert accepted_proposal["status"] == "ACCEPTED"

    soft_skills = get_profile_soft_skills(
        profile["id"],
        authenticated_headers,
    )

    soft_skill_names = {
        soft_skill["name"]
        for soft_skill in soft_skills
    }

    assert soft_skill_name in soft_skill_names


def test_accept_hard_skill_proposal_creates_profile_skill(
    monkeypatch,
    authenticated_headers,
):
    profile = create_test_profile(authenticated_headers)
    cv = create_test_cv(
        profile_id=profile["id"],
        authenticated_headers=authenticated_headers,
    )

    skill = create_test_skill()
    language = create_test_language()
    certification = create_test_certification()

    parsed_data = build_parsed_cv_data(
        skill_name=skill["name"],
        language_name=language["name"],
        certification_name=certification["name"],
    )

    mock_parse_cv_file(
        monkeypatch,
        parsed_data,
    )

    generate_response = client.post(
        f"/cvs/{cv['id']}/enrichment/generate"
    )

    assert generate_response.status_code == 200

    proposals = generate_response.json()

    hard_skill_proposal = next(
        proposal
        for proposal in proposals
        if proposal["proposal_type"] == "HARD_SKILL"
    )

    accept_response = client.post(
        f"/enrichment/{hard_skill_proposal['id']}/accept"
    )

    assert accept_response.status_code == 200

    profile_skills_response = client.get(
        f"/profiles/{profile['id']}/skills",
        headers=authenticated_headers,
    )

    assert profile_skills_response.status_code == 200

    profile_skills = profile_skills_response.json()

    profile_skill_ids = {
        profile_skill["skill_id"]
        for profile_skill in profile_skills
    }

    assert skill["id"] in profile_skill_ids


def test_generate_hard_skill_proposal_for_unknown_non_soft_skill(
    monkeypatch,
    authenticated_headers,
):
    profile = create_test_profile(authenticated_headers)
    cv = create_test_cv(
        profile_id=profile["id"],
        authenticated_headers=authenticated_headers,
    )

    language = create_test_language()
    certification = create_test_certification()

    unknown_hard_skill_name = f"Technical_Platform_{uuid4()}"

    parsed_data = build_parsed_cv_data(
        skill_name=unknown_hard_skill_name,
        language_name=language["name"],
        certification_name=certification["name"],
    )

    mock_parse_cv_file(
        monkeypatch,
        parsed_data,
    )

    response = client.post(
        f"/cvs/{cv['id']}/enrichment/generate"
    )

    assert response.status_code == 200

    proposals = response.json()

    hard_skill_proposals = [
        proposal
        for proposal in proposals
        if proposal["proposal_type"] == "HARD_SKILL"
    ]

    assert len(hard_skill_proposals) == 1
    assert hard_skill_proposals[0]["proposed_value"] == unknown_hard_skill_name
    assert hard_skill_proposals[0]["reference_id"] is None
    assert hard_skill_proposals[0]["target_field"] == "profile_skill"


def test_accept_all_proposals(
    monkeypatch,
    authenticated_headers,
):
    profile = create_test_profile(authenticated_headers)

    cv = create_test_cv(
        profile_id=profile["id"],
        authenticated_headers=authenticated_headers,
    )

    skill = create_test_skill()

    language = create_test_language()

    certification = create_test_certification()

    parsed_data = build_parsed_cv_data(
        skill_name=skill["name"],
        language_name=language["name"],
        certification_name=certification["name"],
    )

    mock_parse_cv_file(
        monkeypatch,
        parsed_data,
    )

    generate_response = client.post(
        f"/cvs/{cv['id']}/enrichment/generate"
    )

    assert generate_response.status_code == 200

    response = client.post(
        "/enrichment/accept-all",
        json={
            "profile_id": profile["id"],
            "cv_id": cv["id"],
        },
    )

    assert response.status_code == 200

    result = response.json()

    assert result["processed"] > 0


def test_reject_all_proposals(
    monkeypatch,
    authenticated_headers,
):
    profile = create_test_profile(authenticated_headers)

    cv = create_test_cv(
        profile_id=profile["id"],
        authenticated_headers=authenticated_headers,
    )

    skill = create_test_skill()

    language = create_test_language()

    certification = create_test_certification()

    parsed_data = build_parsed_cv_data(
        skill_name=skill["name"],
        language_name=language["name"],
        certification_name=certification["name"],
    )

    mock_parse_cv_file(
        monkeypatch,
        parsed_data,
    )

    generate_response = client.post(
        f"/cvs/{cv['id']}/enrichment/generate"
    )

    assert generate_response.status_code == 200

    response = client.post(
        "/enrichment/reject-all",
        json={
            "profile_id": profile["id"],
            "cv_id": cv["id"],
        },
    )

    assert response.status_code == 200

    result = response.json()

    assert result["processed"] > 0


def test_accept_unknown_hard_skill_creates_catalog_skill(
    monkeypatch,
    authenticated_headers,
):
    profile = create_test_profile(authenticated_headers)

    cv = create_test_cv(
        profile_id=profile["id"],
        authenticated_headers=authenticated_headers,
    )

    language = create_test_language()

    certification = create_test_certification()

    unknown_hard_skill_name = "API REST"

    parsed_data = build_parsed_cv_data(
        skill_name=unknown_hard_skill_name,
        language_name=language["name"],
        certification_name=certification["name"],
    )

    mock_parse_cv_file(
        monkeypatch,
        parsed_data,
    )

    generate_response = client.post(
        f"/cvs/{cv['id']}/enrichment/generate"
    )

    assert generate_response.status_code == 200

    proposals = generate_response.json()

    hard_skill_proposal = next(
        proposal
        for proposal in proposals
        if proposal["proposal_type"] == "HARD_SKILL"
    )

    accept_response = client.post(
        f"/enrichment/{hard_skill_proposal['id']}/accept"
    )

    assert accept_response.status_code == 200

    skill_response = client.get(
        "/skills"
    )

    assert skill_response.status_code == 200

    created_skill = next(
        (
            skill
            for skill in skill_response.json()
            if skill["name"] == unknown_hard_skill_name
        ),
        None,
    )

    assert created_skill is not None

    profile_skills_response = client.get(
        f"/profiles/{profile['id']}/skills",
        headers=authenticated_headers,
    )

    assert profile_skills_response.status_code == 200

    profile_skills = profile_skills_response.json()

    assert any(
        profile_skill["skill_id"] == created_skill["id"]
        for profile_skill in profile_skills
    )
