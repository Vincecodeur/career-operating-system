from pathlib import Path

import pytest
from docx import Document

from app.cv.parsing_service import extract_text_from_docx

from app.cv.parsing_service import CVParsingError
from app.cv.parsing_service import extract_text_from_cv
from app.cv.parsing_service import parse_cv_text
from app.cv.parsing_service import extract_section_lines
from app.cv.parsing_service import normalize_text_lines


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


def test_extract_text_from_docx_preserves_table_content_order(
    tmp_path: Path,
):
    document = Document()

    document.add_paragraph("SOPHIE DUBOIS")
    document.add_paragraph(
        "Data & Business Intelligence Analyst",
    )

    document.add_paragraph("Professional Summary")
    document.add_paragraph(
        "Business intelligence analyst with six years of experience.",
    )

    document.add_paragraph("Technical Skills")
    skills_table = document.add_table(
        rows=1,
        cols=2,
    )
    skills_table.cell(0, 0).text = "Power BI\nSQL"
    skills_table.cell(0, 1).text = "Python\nPostgreSQL"

    document.add_paragraph("Languages")
    languages_table = document.add_table(
        rows=1,
        cols=2,
    )
    languages_table.cell(0, 0).text = "French: Native"
    languages_table.cell(0, 1).text = "English: Professional"

    document.add_paragraph("Certifications")
    certifications_table = document.add_table(
        rows=1,
        cols=1,
    )
    certifications_table.cell(0, 0).text = "Microsoft PL-300"

    cv_path = tmp_path / "cv-table.docx"
    document.save(cv_path)

    raw_text = extract_text_from_docx(cv_path)
    parsed_cv = parse_cv_text(raw_text)


    assert parsed_cv.full_name == "SOPHIE DUBOIS"
    assert (
        parsed_cv.professional_title
        == "Data & Business Intelligence Analyst"
    )
    assert "Power BI" in parsed_cv.skills
    assert "SQL" in parsed_cv.skills
    assert "Python" in parsed_cv.skills
    assert "PostgreSQL" in parsed_cv.skills
    assert "French: Native" in parsed_cv.languages
    assert "English: Professional" in parsed_cv.languages
    assert "Microsoft PL-300" in parsed_cv.certifications

    assert raw_text.index("Technical Skills") < raw_text.index("Power BI")
    assert raw_text.index("Power BI") < raw_text.index("Languages")


def test_parse_cv_text_maps_french_profil_to_summary():
    raw_text = """
JEAN DUPONT
Chef de projet informatique

PROFIL
Chef de projet avec 10 ans d'expérience.

COMPÉTENCES
Python, API REST
"""

    parsed_cv = parse_cv_text(raw_text)

    assert parsed_cv.summary == (
        "Chef de projet avec 10 ans d'expérience."
    )

def test_parse_cv_text_rejects_section_heading_as_full_name():
    raw_text = """
OUTILS &
LANGAGES DE PROGRAMMATION
Python
"""

    parsed_cv = parse_cv_text(raw_text)

    assert parsed_cv.full_name is None


def test_parse_cv_text_stops_skills_at_soft_skills_heading():
    raw_text = """
Alex Martin
Software Engineer

Technical Skills
Python, FastAPI, PostgreSQL

Soft Skills
Curious
Reliable
Team spirit

Languages
French: Native
"""

    parsed_cv = parse_cv_text(raw_text)

    assert parsed_cv.skills == [
        "Python",
        "FastAPI",
        "PostgreSQL",
    ]
    assert "Curious" not in parsed_cv.skills
    assert "Reliable" not in parsed_cv.skills
    assert "Team spirit" not in parsed_cv.skills


def test_parse_cv_text_merges_known_split_skill_lines():
    raw_text = """
Alex Martin
Software Engineer

Technical Skills
Cross
functional collaboration
Low -code
development

Languages
English: Professional
"""

    parsed_cv = parse_cv_text(raw_text)

    assert "Cross-functional collaboration" in parsed_cv.skills
    assert "Low-code development" in parsed_cv.skills
    assert "Cross" not in parsed_cv.skills
    assert "development" not in parsed_cv.skills


def test_parse_cv_text_does_not_treat_skill_acronyms_as_headings():
    raw_text = """
Alex Martin
Software Engineer

Technical Skills
SQL
VBA
UAT
CSS
HTML

Languages
English: Professional
"""

    parsed_cv = parse_cv_text(
        raw_text,
    )

    assert parsed_cv.skills == [
        "SQL",
        "VBA",
        "UAT",
        "CSS",
        "HTML",
    ]

    assert parsed_cv.languages == [
        "English: Professional",
    ]

    assert parsed_cv.summary is None
    assert parsed_cv.certifications == []
    assert parsed_cv.experiences == []
    
    

    
def test_extract_section_lines_collects_multiple_matching_sections():
    lines = normalize_text_lines(
        """
Alex Martin
Software Engineer

COMPETENCIES
API design
Database modelling

PROFESSIONAL EXPERIENCE
Software Engineer at Northwind Labs

TOOLS &
PROGRAMMING LANGUAGES
Python
FastAPI
PostgreSQL

LANGUAGES
French: Native
"""
    )

    skill_lines = extract_section_lines(
        lines,
        section_names=[
            "skills",
            "technical skills",
            "competencies",
            "programming languages",
            "tools & programming languages",
        ],
    )

    assert skill_lines == [
        "API design",
        "Database modelling",
        "Python",
        "FastAPI",
        "PostgreSQL",
    ]