from pathlib import Path

from app.cv.parsing_schemas import ParsedCVData
from app.cv.parsing_schemas import ParsedCVExperience


SUPPORTED_PDF_SUFFIX = ".pdf"
SUPPORTED_DOCX_SUFFIX = ".docx"


class CVParsingError(Exception):
    pass


def extract_text_from_pdf(
    file_path: Path,
) -> str:
    try:
        from PyPDF2 import PdfReader
    except ImportError as exc:
        raise CVParsingError(
            "PDF parsing requires PyPDF2 to be installed.",
        ) from exc

    try:
        reader = PdfReader(str(file_path))
        extracted_pages: list[str] = []

        for page in reader.pages:
            page_text = page.extract_text() or ""
            extracted_pages.append(page_text)

        return "\n".join(extracted_pages).strip()
    except Exception as exc:
        raise CVParsingError(
            "Unable to extract text from PDF file.",
        ) from exc


def extract_text_from_docx(
    file_path: Path,
) -> str:
    try:
        from docx import Document
    except ImportError as exc:
        raise CVParsingError(
            "DOCX parsing requires python-docx to be installed.",
        ) from exc

    try:
        document = Document(str(file_path))
        paragraphs = [
            paragraph.text.strip()
            for paragraph in document.paragraphs
            if paragraph.text.strip()
        ]

        return "\n".join(paragraphs).strip()
    except Exception as exc:
        raise CVParsingError(
            "Unable to extract text from DOCX file.",
        ) from exc


def extract_text_from_cv(
    file_path: Path,
) -> str:
    if not file_path.exists() or not file_path.is_file():
        raise CVParsingError(
            "CV file does not exist.",
        )

    suffix = file_path.suffix.lower()

    if suffix == SUPPORTED_PDF_SUFFIX:
        return extract_text_from_pdf(file_path)

    if suffix == SUPPORTED_DOCX_SUFFIX:
        return extract_text_from_docx(file_path)

    raise CVParsingError(
        "Unsupported CV file format. Supported formats are PDF and DOCX.",
    )


def parse_cv_file(
    file_path: Path,
) -> tuple[str, ParsedCVData]:
    raw_text = extract_text_from_cv(file_path)
    parsed_data = parse_cv_text(raw_text)

    return raw_text, parsed_data


def parse_cv_text(
    raw_text: str,
) -> ParsedCVData:
    normalized_lines = normalize_text_lines(raw_text)

    return ParsedCVData(
        full_name=detect_full_name(normalized_lines),
        professional_title=detect_professional_title(normalized_lines),
        summary=extract_section_text(
            normalized_lines,
            section_names=[
                "summary",
                "profile",
                "professional summary",
                "about",
                "about me",
            ],
        ),
        skills=extract_list_section(
            normalized_lines,
            section_names=[
                "skills",
                "technical skills",
                "core skills",
                "competencies",
                "key skills",
            ],
        ),
        languages=extract_list_section(
            normalized_lines,
            section_names=[
                "languages",
                "language",
            ],
        ),
        certifications=extract_list_section(
            normalized_lines,
            section_names=[
                "certifications",
                "certification",
                "licenses",
                "licences",
            ],
        ),
        experiences=extract_experiences(normalized_lines),
    )


def normalize_text_lines(
    raw_text: str,
) -> list[str]:
    return [
        line.strip()
        for line in raw_text.replace("\r", "\n").split("\n")
        if line.strip()
    ]


def detect_full_name(
    lines: list[str],
) -> str | None:
    if not lines:
        return None

    first_line = lines[0]

    if len(first_line.split()) <= 6:
        return first_line

    return None


def detect_professional_title(
    lines: list[str],
) -> str | None:
    if len(lines) < 2:
        return None

    second_line = lines[1]

    if is_section_heading(second_line):
        return None

    if len(second_line) <= 120:
        return second_line

    return None


def extract_section_text(
    lines: list[str],
    section_names: list[str],
) -> str | None:
    section_lines = extract_section_lines(
        lines,
        section_names,
    )

    if not section_lines:
        return None

    return " ".join(section_lines).strip()


def extract_list_section(
    lines: list[str],
    section_names: list[str],
) -> list[str]:
    section_lines = extract_section_lines(
        lines,
        section_names,
    )

    values: list[str] = []

    for line in section_lines:
        split_values = split_list_line(line)

        for value in split_values:
            clean_value = clean_list_value(value)

            if clean_value and clean_value not in values:
                values.append(clean_value)

    return values


def extract_section_lines(
    lines: list[str],
    section_names: list[str],
) -> list[str]:
    normalized_section_names = {
        section_name.lower()
        for section_name in section_names
    }

    collected_lines: list[str] = []
    inside_section = False

    for line in lines:
        normalized_line = normalize_heading(line)

        if normalized_line in normalized_section_names:
            inside_section = True
            continue

        if inside_section and is_section_heading(line):
            break

        if inside_section:
            collected_lines.append(line)

    return collected_lines


def extract_experiences(
    lines: list[str],
) -> list[ParsedCVExperience]:
    experience_lines = extract_section_lines(
        lines,
        section_names=[
            "experience",
            "work experience",
            "professional experience",
            "employment history",
        ],
    )

    if not experience_lines:
        return []

    experiences: list[ParsedCVExperience] = []
    current_description: list[str] = []

    for line in experience_lines:
        if looks_like_experience_header(line):
            if current_description:
                experiences.append(
                    ParsedCVExperience(
                        description=" ".join(current_description).strip(),
                    ),
                )
                current_description = []

            experiences.append(
                ParsedCVExperience(
                    title=line,
                    description=None,
                ),
            )
        else:
            current_description.append(line)

    if current_description:
        if experiences and experiences[-1].description is None:
            experiences[-1].description = " ".join(
                current_description,
            ).strip()
        else:
            experiences.append(
                ParsedCVExperience(
                    description=" ".join(current_description).strip(),
                ),
            )

    return experiences


def looks_like_experience_header(
    line: str,
) -> bool:
    separators = [
        " at ",
        " - ",
        " | ",
        " chez ",
    ]

    lower_line = line.lower()

    return any(
        separator in lower_line
        for separator in separators
    )


def split_list_line(
    line: str,
) -> list[str]:
    separators = [
        ",",
        ";",
        "|",
        "•",
        "·",
    ]

    values = [line]

    for separator in separators:
        updated_values: list[str] = []

        for value in values:
            updated_values.extend(value.split(separator))

        values = updated_values

    return values


def clean_list_value(
    value: str,
) -> str:
    return (
        value.strip()
        .strip("-")
        .strip("•")
        .strip("·")
        .strip()
    )


def normalize_heading(
    value: str,
) -> str:
    return (
        value.strip()
        .lower()
        .replace(":", "")
    )


def is_section_heading(
    value: str,
) -> bool:
    normalized = normalize_heading(value)

    known_headings = {
        "summary",
        "profile",
        "professional summary",
        "about",
        "about me",
        "skills",
        "technical skills",
        "core skills",
        "competencies",
        "key skills",
        "languages",
        "language",
        "certifications",
        "certification",
        "licenses",
        "licences",
        "experience",
        "work experience",
        "professional experience",
        "employment history",
        "education",
        "projects",
    }

    if normalized in known_headings:
        return True

    if len(value) > 80:
        return False

    alpha_chars = [
        char
        for char in value
        if char.isalpha()
    ]

    if not alpha_chars:
        return False

    uppercase_ratio = (
        sum(
            1
            for char in alpha_chars
            if char.isupper()
        )
        / len(alpha_chars)
    )

    return uppercase_ratio >= 0.8