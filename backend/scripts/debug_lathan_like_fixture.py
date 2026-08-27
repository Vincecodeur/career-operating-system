from pathlib import Path
import sys

PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parents[1]
)

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(PROJECT_ROOT),
    )

from app.cv.parsing_service import (
    parse_cv_text,
)

INPUT_FILE = (
    Path("tests")
    / "fixtures"
    / "cv_parser"
    / "09_pdf_interleaved_internal_order.txt"
)

raw_text = INPUT_FILE.read_text(
    encoding="utf-8"
)

parsed = parse_cv_text(
    raw_text
)

print(
    parsed.model_dump_json(
        indent=2
    )
)
