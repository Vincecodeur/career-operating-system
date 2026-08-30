import re
import unicodedata
from pathlib import Path
from typing import Any

from app.cv.parsing_schemas import ParsedCVData
from app.cv.parsing_schemas import ParsedCVExperience


SUPPORTED_PDF_SUFFIX = ".pdf"
SUPPORTED_DOCX_SUFFIX = ".docx"

PDF_LINE_TOLERANCE = 3.0
PDF_COLUMN_GAP_RATIO = 0.08
PDF_MIN_COLUMN_WORDS = 4
PDF_MIN_TEXT_LENGTH = 20

class CVParsingError(Exception):
    pass


def extract_text_from_pdf_pypdf2(
    file_path: Path,
) -> str:
    try:
        from PyPDF2 import PdfReader
    except ImportError as exc:
        raise CVParsingError(
            "PDF parsing requires PyPDF2 to be installed.",
        ) from exc

    reader = PdfReader(str(file_path))
    extracted_pages: list[str] = []

    for page in reader.pages:
        page_text = page.extract_text() or ""

        if page_text.strip():
            extracted_pages.append(
                page_text.strip(),
            )

    return "\n".join(extracted_pages).strip()


def group_pdf_words_into_lines(
    words: list[dict[str, Any]],
    y_tolerance: float = PDF_LINE_TOLERANCE,
) -> list[list[dict[str, Any]]]:
    if not words:
        return []

    sorted_words = sorted(
        words,
        key=lambda word: (
            float(word["top"]),
            float(word["x0"]),
        ),
    )

    grouped_lines: list[list[dict[str, Any]]] = []

    for word in sorted_words:
        word_top = float(word["top"])

        matching_line: list[dict[str, Any]] | None = None

        for line in reversed(grouped_lines):
            reference_top = sum(
                float(line_word["top"])
                for line_word in line
            ) / len(line)

            if abs(word_top - reference_top) <= y_tolerance:
                matching_line = line
                break

            if word_top - reference_top > y_tolerance:
                break

        if matching_line is None:
            grouped_lines.append(
                [word],
            )
        else:
            matching_line.append(
                word,
            )

    for line in grouped_lines:
        line.sort(
            key=lambda word: float(word["x0"]),
        )

    return grouped_lines


def render_pdf_word_lines(
    word_lines: list[list[dict[str, Any]]],
) -> str:
    rendered_lines: list[str] = []

    for word_line in word_lines:
        line_text = " ".join(
            str(word["text"]).strip()
            for word in word_line
            if str(word["text"]).strip()
        ).strip()

        if line_text:
            rendered_lines.append(line_text)

    return "\n".join(rendered_lines).strip()

def order_pdf_columns(
    left_words: list[dict[str, Any]],
    right_words: list[dict[str, Any]],
) -> list[list[dict[str, Any]]]:
    columns = [
        left_words,
        right_words,
    ]

    return sorted(
        columns,
        key=len,
        reverse=True,
    )

def find_pdf_column_split(
    words: list[dict[str, Any]],
    page_width: float,
) -> float | None:
    if len(words) < PDF_MIN_COLUMN_WORDS * 2:
        return None

    horizontal_positions = sorted(
        {
            round(float(word["x0"]), 1)
            for word in words
        }
    )

    if len(horizontal_positions) < 2:
        return None

    minimum_gap = page_width * PDF_COLUMN_GAP_RATIO
    page_middle = page_width / 2

    candidate_gaps: list[tuple[float, float]] = []

    for left_position, right_position in zip(
        horizontal_positions,
        horizontal_positions[1:],
    ):
        gap = right_position - left_position
        split_position = (
            left_position + right_position
        ) / 2

        if gap < minimum_gap:
            continue

        if not (
            page_width * 0.20
            <= split_position
            <= page_width * 0.80
        ):
            continue

        candidate_gaps.append(
            (
                gap,
                split_position,
            )
        )

    if not candidate_gaps:
        return None

    candidate_gaps.sort(
        key=lambda candidate: (
            candidate[0],
            -abs(candidate[1] - page_middle),
        ),
        reverse=True,
    )

    _, split_position = candidate_gaps[0]

    left_words = [
        word
        for word in words
        if float(word["x0"]) < split_position
    ]
    right_words = [
        word
        for word in words
        if float(word["x0"]) >= split_position
    ]

    if (
        len(left_words) < PDF_MIN_COLUMN_WORDS
        or len(right_words) < PDF_MIN_COLUMN_WORDS
    ):
        return None

    return split_position


def extract_pdf_page_layout_text(
    page: Any,
) -> str:
    words = page.extract_words(
        use_text_flow=False,
        keep_blank_chars=False,
    )

    if not words:
        return ""

    page_width = float(page.width)

    split_position = find_pdf_column_split(
        words,
        page_width,
    )

    if split_position is None:
        return render_pdf_word_lines(
            group_pdf_words_into_lines(words),
        )

    left_words = [
        word
        for word in words
        if float(word["x0"]) < split_position
    ]

    right_words = [
        word
        for word in words
        if float(word["x0"]) >= split_position
    ]

    ordered_columns = order_pdf_columns(
        left_words,
        right_words,
    )

    rendered_columns = [
        render_pdf_word_lines(
            group_pdf_words_into_lines(column_words),
        )
        for column_words in ordered_columns
    ]

    return "\n".join(
        column_text
        for column_text in rendered_columns
        if column_text
    ).strip()

def extract_text_from_pdf_pdfplumber(
    file_path: Path,
) -> str:
    try:
        import pdfplumber
    except ImportError as exc:
        raise CVParsingError(
            "PDF layout parsing requires pdfplumber to be installed.",
        ) from exc

    extracted_pages: list[str] = []

    with pdfplumber.open(str(file_path)) as pdf:
        for page in pdf.pages:
            page_text = extract_pdf_page_layout_text(page)

            if page_text:
                extracted_pages.append(page_text)

    return "\n".join(extracted_pages).strip()


def calculate_pdf_extraction_quality(
    extracted_text: str,
) -> tuple[int, int, int, int]:
    normalized_lines = normalize_text_lines(
        extracted_text,
    )

    if not normalized_lines:
        return (
            0,
            0,
            0,
            0,
        )

    parsed_data = parse_cv_text(
        extracted_text,
    )

    populated_sections = sum(
        [
            bool(parsed_data.summary),
            bool(parsed_data.skills),
            bool(parsed_data.languages),
            bool(parsed_data.certifications),
            bool(parsed_data.experiences),
        ]
    )

    identity_fields = sum(
        [
            bool(parsed_data.full_name),
            bool(parsed_data.professional_title),
        ]
    )

    suspicious_language_overflow = (
        len(parsed_data.languages)
        if (
            not parsed_data.skills
            and len(parsed_data.languages) > 6
        )
        else 0
    )

    return (
        populated_sections,
        identity_fields,
        -suspicious_language_overflow,
        len(extracted_text),
    )


def select_best_pdf_extraction(
    extractions: list[str],
) -> str:
    usable_extractions = [
        extraction.strip()
        for extraction in extractions
        if len(extraction.strip()) >= PDF_MIN_TEXT_LENGTH
    ]

    if not usable_extractions:
        return ""

    return max(
        usable_extractions,
        key=calculate_pdf_extraction_quality,
    )


def extract_text_from_pdf(
    file_path: Path,
) -> str:
    extracted_texts: list[str] = []
    extraction_errors: list[Exception] = []

    for extractor in [
        extract_text_from_pdf_pdfplumber,
        extract_text_from_pdf_pypdf2,
    ]:
        try:
            extracted_text = extractor(
                file_path,
            )

            if extracted_text:
                extracted_texts.append(
                    extracted_text,
                )
        except Exception as exc:
            extraction_errors.append(exc)

    best_extraction = select_best_pdf_extraction(
        extracted_texts,
    )

    if best_extraction:
        return best_extraction

    if extraction_errors:
        raise CVParsingError(
            "Unable to extract usable text from PDF file.",
        ) from extraction_errors[-1]

    raise CVParsingError(
        "Unable to extract usable text from PDF file.",
    )

def extract_text_from_docx(
    file_path: Path,
) -> str:
    try:
        from docx import Document
        from docx.table import Table
        from docx.text.paragraph import Paragraph
    except ImportError as exc:
        raise CVParsingError(
            "DOCX parsing requires python-docx to be installed.",
        ) from exc

    try:
        document = Document(str(file_path))
        extracted_lines: list[str] = []

        for child in document.element.body.iterchildren():
            if child.tag.endswith("}p"):
                paragraph = Paragraph(
                    child,
                    document,
                )
                paragraph_text = paragraph.text.strip()

                if paragraph_text:
                    extracted_lines.append(
                        paragraph_text,
                    )

            elif child.tag.endswith("}tbl"):
                table = Table(
                    child,
                    document,
                )

                for row in table.rows:
                    for cell in row.cells:
                        for paragraph in cell.paragraphs:
                            paragraph_text = paragraph.text.strip()

                            if paragraph_text:
                                extracted_lines.extend(
                                    line.strip()
                                    for line in paragraph_text.splitlines()
                                    if line.strip()
                                )

        return "\n".join(extracted_lines).strip()
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

    normalized_lines = merge_split_section_headings(
        normalized_lines
    )

    return ParsedCVData(
        full_name=detect_full_name(normalized_lines),
        professional_title=detect_professional_title(normalized_lines),
        summary=extract_section_text(
            normalized_lines,
            section_names=[
                "summary",
                "profile",
                "profil",
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
                    "competences",
                    "competences cles",
                    "key skills",
                    "programming languages",
                    "tools & programming languages",
                    "tools and programming languages",
                    "outils & langages de programmation",
                    "outils et langages de programmation",
                    "technologies",
                    "technical stack",
                
            ],
        ),
        languages=extract_languages(
            normalized_lines,
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
    
def merge_split_section_headings(
    lines: list[str],
) -> list[str]:
    merged_lines: list[str] = []
    index = 0

    known_split_headings = {
        "tools & programming languages":
            "Tools & Programming Languages",
        "tools and programming languages":
            "Tools and Programming Languages",
        "outils & langages de programmation":
            "Outils & Langages de Programmation",
        "outils et langages de programmation":
            "Outils et Langages de Programmation",
        "qualites & langues":
            "Qualités & Langues",
        "qualites et langues":
            "Qualités et Langues",
    }

    while index < len(lines):
        matched_heading: str | None = None
        consumed_lines = 0

        for line_count in [
            3,
            2,
        ]:
            if index + line_count > len(lines):
                continue

            candidate = " ".join(
                lines[
                    index:
                    index + line_count
                ]
            )

            normalized_candidate = normalize_heading(
                candidate,
            )

            if normalized_candidate in known_split_headings:
                matched_heading = known_split_headings[
                    normalized_candidate
                ]
                consumed_lines = line_count
                break

        if matched_heading is not None:
            merged_lines.append(
                matched_heading,
            )
            index += consumed_lines
            continue

        merged_lines.append(
            lines[index],
        )
        index += 1

    return merged_lines

def collapse_spaced_uppercase_name(
    value: str,
) -> str:
    parts = value.split()

    if (
        len(parts) >= 2
        and all(
            len(part) == 1
            and part.isalpha()
            and part.isupper()
            for part in parts
        )
    ):
        return "".join(parts)

    return value


def looks_like_name_fragment(
    value: str,
) -> bool:
    if is_known_section_heading(value):
        return False

    if any(
        character.isdigit()
        for character in value
    ):
        return False

    collapsed_value = collapse_spaced_uppercase_name(
        value,
    )

    words = collapsed_value.split()

    if not 1 <= len(words) <= 3:
        return False

    alpha_characters = [
        character
        for character in collapsed_value
        if character.isalpha()
    ]

    if len(alpha_characters) < 2:
        return False

    return all(
        character.isupper()
        for character in alpha_characters
    )


def find_full_name_location(
    lines: list[str],
) -> tuple[str, int] | None:
    for index in range(
        len(lines) - 1
    ):
        first_fragment = lines[index]
        second_fragment = lines[index + 1]

        if not looks_like_name_fragment(
            first_fragment,
        ):
            continue

        if not looks_like_name_fragment(
            second_fragment,
        ):
            continue

        first_name_part = collapse_spaced_uppercase_name(
            first_fragment,
        )
        second_name_part = collapse_spaced_uppercase_name(
            second_fragment,
        )

        return (
            f"{first_name_part} {second_name_part}",
            index,
        )

    return None

def detect_full_name(
    lines: list[str],
) -> str | None:
    if not lines:
        return None

    first_line = lines[0]

    if (
        not is_known_section_heading(first_line)
        and len(first_line.split()) <= 6
    ):
        return first_line

    detected_name = find_full_name_location(
        lines,
    )

    if detected_name is None:
        return None

    full_name, _ = detected_name

    return full_name.title()


def detect_professional_title(
    lines: list[str],
) -> str | None:
    if len(lines) < 2:
        return None

    first_line = lines[0]
    second_line = lines[1]

    if (
        not is_known_section_heading(first_line)
        and not is_section_heading(second_line)
        and len(second_line) <= 120
    ):
        return second_line

    detected_name = find_full_name_location(
        lines,
    )

    if detected_name is None:
        return None

    _, name_index = detected_name

    for candidate_line in lines[
        name_index + 2:
        name_index + 6
    ]:
        if is_section_heading(candidate_line):
            continue

        if any(
            character.isdigit()
            for character in candidate_line
        ):
            continue

        if "@" in candidate_line:
            continue

        if len(candidate_line) > 120:
            continue

        return candidate_line

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

    normalized_section_lines = merge_known_split_skill_lines(
        normalized_section_lines,
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

    while index < len(lines):
        current_line = lines[index].strip()

        next_line = (
            lines[index + 1].strip()
            if index + 1 < len(lines)
            else None
        )

        normalized_current_line = re.sub(
            r"\s*-\s*",
            "-",
            current_line,
        ).lower()

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
            and normalized_current_line == "low-code"
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
        normalize_heading(section_name,
        )
        for section_name in section_names
    }

    collected_lines: list[str] = []
    inside_section = False

    for line in lines:
        normalized_line = normalize_heading(
            line,
        )

        if normalized_line in normalized_section_names:
            inside_section = True
            continue

        if (
            inside_section
            and is_known_section_heading(line)
        ):
            inside_section = False
            continue

        if inside_section:
            collected_lines.append(
                line,
            )

    return collected_lines


def looks_like_language_value(
    value: str,
) -> bool:
    normalized_value = normalize_heading(
        value,
    )

    language_level_markers = {
        "native",
        "bilingual",
        "bilingue",
        "fluent",
        "courant",
        "professional",
        "professionnel",
        "beginner",
        "debutant",
        "intermediate",
        "intermediaire",
        "advanced",
        "avance",
        "mother tongue",
        "langue maternelle",
        "a1",
        "a2",
        "b1",
        "b2",
        "c1",
        "c2",
    }

    if ":" in value:
        return True

    words = set(
        re.findall(
            r"[a-z0-9]+",
            normalized_value,
        )
    )

    return bool(
        words & language_level_markers
    )


def extract_languages(
    lines: list[str],
) -> list[str]:
    languages = extract_list_section(
        lines,
        section_names=[
            "languages",
            "language",
            "langues",
            "langue",
        ],
    )

    mixed_section_lines = extract_section_lines(
        lines,
        section_names=[
            "qualites & langues",
            "qualites et langues",
        ],
    )

    for line in mixed_section_lines:
        split_values = split_list_line(
            line,
        )

        for value in split_values:
            clean_value = clean_list_value(
                value,
            )

            if (
                clean_value
                and looks_like_language_value(clean_value)
                and clean_value not in languages
            ):
                languages.append(
                    clean_value,
                )

    return languages

def extract_experience_date_values(
    value: str,
) -> list[str]:
    date_pattern = re.compile(
        r"\b(?:"
        r"\d{1,2}/\d{1,2}/(?:19|20)?\d{2}"
        r"|"
        r"(?:"
        r"janvier|février|fevrier|mars|avril|mai|juin|"
        r"juillet|août|aout|septembre|octobre|novembre|"
        r"décembre|decembre|"
        r"january|february|march|april|may|june|july|"
        r"august|september|october|november|december"
        r")\s+(?:19|20)\d{2}"
        r"|"
        r"(?:19|20)\d{2}"
        r")\b",
        re.IGNORECASE,
    )

    return [
        match.group(0).strip()
        for match in date_pattern.finditer(value)
    ]


def contains_experience_date(
    value: str,
) -> bool:
    return bool(
        extract_experience_date_values(value)
    )


def clean_experience_header(
    value: str,
) -> str:
    cleaned_value = value

    for date_value in extract_experience_date_values(value):
        cleaned_value = cleaned_value.replace(
            date_value,
            " ",
        )

    cleaned_value = re.sub(
        r"\s+",
        " ",
        cleaned_value,
    )

    return (
        cleaned_value
        .strip()
        .strip("-")
        .strip("–")
        .strip("|")
        .strip()
    )


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

    if any(
        separator in lower_line
        for separator in separators
    ):
        return True

    if not contains_experience_date(line):
        return False

    alpha_characters = [
        character
        for character in line
        if character.isalpha()
    ]

    if not alpha_characters:
        return False

    uppercase_ratio = (
        sum(
            1
            for character in alpha_characters
            if character.isupper()
        )
        / len(alpha_characters)
    )

    return uppercase_ratio >= 0.60


def looks_like_experience_organization(
    value: str,
) -> bool:
    normalized_value = normalize_heading(
        value,
    )

    organization_markers = [
        "university",
        "universite",
        "école",
        "ecole",
        "academy",
        "institute",
        "institut",
        "company",
        "agency",
        "agence",
        "laboratory",
        "laboratoire",
    ]

    if any(
        marker in normalized_value
        for marker in organization_markers
    ):
        return True

    if len(value) > 80:
        return False

    if any(
        punctuation in value
        for punctuation in [
            ".",
            ":",
            ";",
        ]
    ):
        return False

    return False


def looks_like_location_value(
    value: str,
) -> bool:
    normalized_value = normalize_heading(
        value,
    )

    location_markers = [
        "paris",
        "france",
        "london",
        "lyon",
        "marseille",
        "toulouse",
        "villeneuve-le-roi",
        "ivry-sur-seine",
        "levallois-perret",
        "kremlin-bicetre",
    ]

    return (
        "," in value
        or any(
            marker in normalized_value
            for marker in location_markers
        )
    )


def split_classic_experience_header(
    value: str,
) -> tuple[str, str | None]:
    separators = [
        " at ",
        " chez ",
    ]

    lower_value = value.lower()

    for separator in separators:
        separator_index = lower_value.find(
            separator,
        )

        if separator_index == -1:
            continue

        title = value[
            :separator_index
        ].strip()

        company = value[
            separator_index + len(separator):
        ].strip()

        return (
            title,
            company or None,
        )

    return (
        clean_experience_header(value),
        None,
    )


def build_parsed_experience(
    header_lines: list[str],
    body_lines: list[str],
) -> ParsedCVExperience | None:
    if not header_lines and not body_lines:
        return None

    all_dates: list[str] = []

    for header_line in header_lines:
        all_dates.extend(
            extract_experience_date_values(
                header_line,
            )
        )

    start_date = (
        all_dates[0]
        if all_dates
        else None
    )

    end_date = (
        all_dates[-1]
        if len(all_dates) >= 2
        else None
    )

    cleaned_headers = [
        cleaned_header
        for header_line in header_lines
        if (
            cleaned_header := clean_experience_header(
                header_line,
            )
        )
    ]

    remaining_body_lines = list(
        body_lines,
    )

    title: str | None = None
    company: str | None = None

    if len(cleaned_headers) == 1:
        title, company = split_classic_experience_header(
            cleaned_headers[0],
        )

    elif len(cleaned_headers) >= 2:
        first_header = cleaned_headers[0]
        second_header = cleaned_headers[1]

        normalized_first_header = normalize_heading(
            first_header,
        )

        if normalized_first_header.startswith(
            "projet "
        ):
            title = second_header

            if (
                remaining_body_lines
                and looks_like_experience_organization(
                    remaining_body_lines[0],
                )
            ):
                company = remaining_body_lines.pop(0)

        else:
            title = first_header

            if not looks_like_location_value(
                second_header,
            ):
                company = second_header
            else:
                remaining_body_lines.insert(
                    0,
                    second_header,
                )

        if len(cleaned_headers) > 2:
            remaining_body_lines = [
                *cleaned_headers[2:],
                *remaining_body_lines,
            ]

    elif remaining_body_lines:
        title = remaining_body_lines.pop(0)

    description = " ".join(
        remaining_body_lines,
    ).strip()

    return ParsedCVExperience(
        title=title or None,
        company=company,
        start_date=start_date,
        end_date=end_date,
        description=description or None,
    )


def extract_experiences(
    lines: list[str],
) -> list[str]:
    experience_lines = extract_section_lines(
        lines,
        section_names=[
            "experience",
            "experiences",
            "work experience",
            "professional experience",
            "professional experiences",
            "employment history",
            "experience professionnelle",
            "experiences professionnelles",
        ],
    )

    if not experience_lines:
        return []

    experience_blocks: list[
        tuple[list[str], list[str]]
    ] = []

    current_headers: list[str] = []
    current_body: list[str] = []

    def flush_current_block() -> None:
        nonlocal current_headers
        nonlocal current_body

        if current_headers or current_body:
            experience_blocks.append(
                (
                    current_headers,
                    current_body,
                )
            )

        current_headers = []
        current_body = []

    for line in experience_lines:
        if looks_like_experience_header(line):
            if current_headers and current_body:
                flush_current_block()

            elif len(current_headers) >= 2:
                flush_current_block()

            current_headers.append(line)
            continue

        current_body.append(line)

    flush_current_block()

    experiences: list[ParsedCVExperience] = []

    for header_lines, body_lines in experience_blocks:
        experience = build_parsed_experience(
            header_lines,
            body_lines,
        )

        if experience is not None:
            experiences.append(
                experience,
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

    if any(
        separator in lower_line
        for separator in separators
    ):
        return True

    date_pattern = re.compile(
        r"\b("
        r"(?:19|20)\d{2}"
        r"|"
        r"\d{1,2}/\d{1,2}/(?:19|20)?\d{2}"
        r")\b"
    )

    alpha_characters = [
        character
        for character in line
        if character.isalpha()
    ]

    if not alpha_characters:
        return False

    uppercase_ratio = (
        sum(
            1
            for character in alpha_characters
            if character.isupper()
        )
        / len(alpha_characters)
    )

    return (
        bool(date_pattern.search(line))
        and uppercase_ratio >= 0.60
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
    normalized_value = unicodedata.normalize(
        "NFKD",
        value,
    )

    normalized_value = "".join(
        character
        for character in normalized_value
        if not unicodedata.combining(character)
    )

    return (
        normalized_value
        .strip()
        .lower()
        .replace(":", "")
    )


def is_known_section_heading(
    value: str,
) -> bool:
    normalized = normalize_heading(value)

    known_headings = {
        "summary",
        "profile",
        "profil",
        "professional summary",
        "about",
        "about me",
        "skills",
        "technical skills",
        "core skills",
        "competencies",
        "key skills",
        "soft skills",
        "soft skill",
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
        "qualités",
        "qualites",
        "qualités personnelles",
        "qualites personnelles",
        "qualités & langues",
        "qualites & langues",
        "outils",
        "outils &",
        "outils & logiciels",
        "programming languages",
        "tools & programming languages",
        "tools and programming languages",
        "outils & langages de programmation",
        "outils et langages de programmation",
        "technologies",
        "technical stack",
        "competences",
        "competences cles",
        "experiences professionnelles",
        "qualites & langues",
        "qualites et langues",
    }

    return normalized in known_headings

def is_section_heading(
    value: str,
) -> bool:
    if is_known_section_heading(value):
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

    if len(alpha_chars) <= 4:
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