import re
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
                "compétences",
                "competences",
                "compétences clés",
                "competences cles",
            ],
        ),
        languages=extract_list_section(
            normalized_lines,
            section_names=[
                "languages",
                "language",
                "langues",
                "langue",
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

    normalized_section_lines = normalize_list_section_lines(
        section_lines,
    )

    values: list[str] = []

    for line in normalized_section_lines:
        split_values = split_list_line(line)

        for value in split_values:
            clean_value = clean_list_value(value)

            if clean_value and clean_value not in values:
                values.append(clean_value)

    return values

def normalize_list_section_lines(
    lines: list[str],
) -> list[str]:
    normalized_lines: list[str] = []

    buffer: list[str] = []
    parenthesis_balance = 0

    for line in lines:
        stripped_line = line.strip()

        if not stripped_line:
            continue

        if not buffer:
            buffer.append(
                stripped_line,
            )

            parenthesis_balance = (
                stripped_line.count("(")
                - stripped_line.count(")")
            )

            if parenthesis_balance <= 0:
                normalized_lines.append(
                    buffer[0],
                )
                buffer: list[str] = []

            continue

        buffer.append(
            stripped_line,
        )

        parenthesis_balance += (
            stripped_line.count("(")
            - stripped_line.count(")")
        )

        if parenthesis_balance <= 0:
            normalized_lines.append(
                " ".join(buffer),
            )

            buffer = []
            parenthesis_balance = 0

    if buffer:
        normalized_lines.append(
            " ".join(buffer),
        )

    return normalized_lines


def merge_parenthetical_buffer(
    values: list[str],
) -> str:
    if len(values) == 1:
        return values[0]

    first_value = values[0]
    second_value = values[1]

    separator = ", "

    if second_value.strip().lower().startswith("tables"):
        separator = " "

    merged_value = f"{first_value}{separator}{second_value}"

    if len(values) > 2:
        merged_value = (
            merged_value
            + ", "
            + ", ".join(values[2:])
        )

    return merged_value


def merge_known_split_skill_lines(
    lines: list[str],
) -> list[str]:
    merged_lines: list[str] = []
    index = 0

    while indexs():
        current_line = lines[index].strip()

        next_line = (
            lines[index + 1].strip()
            if index + 1 < len(lines)
            else None
        )

        if (
            next_line is not None
            and current_line.lower() == "cross"
            and next_line.lower() == "functional collaboration"
        ):
            merged_lines.append(
                "Cross-functional collaboration",
            )
            index += 2
            continue

        if (
            next_line is not None
            and normalize_skill_alias(current_line) == "Low-code"
            and next_line.lower() == "development"
        ):
            merged_lines.append(
                "Low-code development",
            )
            index += 2
            continue

        merged_lines.append(
            current_line,
        )

        index += 1

    return merged_lines


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
            "expérience",
            "expériences",
            "experience professionnelle",
            "expériences professionnelles",
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
    expanded_values = expand_parenthetical_values(
        line,
    )

    split_values: list[str] = []

    for value in expanded_values:
        split_values.extend(
            split_compound_skill_value(
                value,
            ),
        )

    return split_values

def expand_parenthetical_values(
    value: str,
) -> list[str]:
    if "(" in value and ")" in value:
        parenthetical_values = re.findall(
            r"\(([^()]*)\)",
            value,
        )

        base_value = re.sub(
            r"\([^()]*\)",
            " ",
            value,
        )

        return [
            base_value,
            *parenthetical_values,
        ]

    if "(" in value and ")" not in value:
        return value.replace(
            "(",
            ",",
        ).split(",")

    if ")" in value and "(" not in value:
        return [
            value.replace(
                ")",
                "",
            ),
        ]

    return [
        value,
    ]


def split_compound_skill_value(
    value: str,
) -> list[str]:
    normalized_value = value

    normalized_value = normalized_value.replace(
        " and ",
        ",",
    )
    normalized_value = normalized_value.replace(
        " & ",
        ",",
    )
    normalized_value = normalized_value.replace(
        " / ",
        ",",
    )
    normalized_value = normalized_value.replace(
        "â€¢",
        ",",
    )
    normalized_value = normalized_value.replace(
        "Â·",
        ",",
    )

    if normalized_value.strip().startswith("&"):
        normalized_value = normalized_value.strip()[1:]

    return re.split(
        r"[,;|]",
        normalized_value,
    )

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
        "compétences",
        "competences",
        "compétences clés",
        "competences cles",
        "langues",
        "langue",
        "expérience",
        "expériences",
        "experience professionnelle",
        "expériences professionnelles",
        "formation",
        "formations",
        "outils",
        "outils & logiciels",
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