from pathlib import Path

import pytest

from app.cv.parsing_service import CVParsingError
from app.cv.parsing_service import extract_text_from_cv
from app.cv.parsing_service import parse_cv_text


def test_parse_cv_text_extracts_basic_profile_information():
    raw_text = """
Vincent Gueret
Technical Partnerships Manager

Summary
Technical partnerships profile with API integration experience.

Skills
Python, FastAPI, React, PostgreSQL

Languages
French, English, Portuguese

Certifications
Azure Fundamentals
Scrum

Experience
Technical Partnerships Manager at Software Company
Managed marketplace, webstore and carrier integrations.
"""

    parsed_cv = parse_cv_text(raw_text)

    assert parsed_cv.full_name == "Vincent Gueret"
    assert parsed_cv.professional_title == "Technical Partnerships Manager"
    assert parsed_cv.summary == (
        "Technical partnerships profile with API integration experience."
    )
    assert "Python" in parsed_cv.skills
    assert "FastAPI" in parsed_cv.skills
    assert "React" in parsed_cv.skills
    assert "PostgreSQL" in parsed_cv.skills
    assert "French" in parsed_cv.languages
    assert "English" in parsed_cv.languages
    assert "Portuguese" in parsed_cv.languages
    assert "Azure Fundamentals" in parsed_cv.certifications
    assert "Scrum" in parsed_cv.certifications
    assert len(parsed_cv.experiences) >= 1


def test_parse_cv_text_returns_empty_lists_when_sections_are_missing():
    raw_text = """
Vincent Gueret
Technical Partnerships Manager
"""

    parsed_cv = parse_cv_text(raw_text)

    assert parsed_cv.full_name == "Vincent Gueret"
    assert parsed_cv.professional_title == "Technical Partnerships Manager"
    assert parsed_cv.summary is None
    assert parsed_cv.skills == []
    assert parsed_cv.languages == []
    assert parsed_cv.certifications == []
    assert parsed_cv.experiences == []


def test_extract_text_from_cv_rejects_unsupported_file_format(
    tmp_path: Path,
):
    unsupported_file = tmp_path / "cv.txt"
    unsupported_file.write_text(
        "Plain text CV",
        encoding="utf-8",
    )

    with pytest.raises(CVParsingError) as exc_info:
        extract_text_from_cv(unsupported_file)

    assert "Unsupported CV file format" in str(exc_info.value)


def test_extract_text_from_cv_rejects_missing_file(
    tmp_path: Path,
):
    missing_file = tmp_path / "missing.pdf"

    with pytest.raises(CVParsingError) as exc_info:
        extract_text_from_cv(missing_file)

    assert "CV file does not exist" in str(exc_info.value)
    
def clean_list_value(
    value: str,
) -> str:
    cleaned_value = " ".join(
        value.strip().split(),
    )

    cleaned_value = (
        cleaned_value
        .strip("-")
        .strip("&")
        .strip("/")
        .strip("â€¢")
        .strip("Â·")
        .strip("(")
        .strip(")")
        .strip()
    )

    return cleaned_value


