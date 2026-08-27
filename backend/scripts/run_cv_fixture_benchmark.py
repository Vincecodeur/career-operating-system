from pathlib import Path
import json



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
    
from app.cv.parsing_service import extract_text_from_cv
from app.cv.parsing_service import parse_cv_text

FIXTURE_DIR = (
    Path("tests")
    / "fixtures"
    / "cv_parser"
)


def count_match(actual, expected):
    return len(
        set(actual)
        & set(expected)
    )


def main():
    manifest = json.loads(
        (
            FIXTURE_DIR
            / "manifest.json"
        ).read_text(
            encoding="utf-8"
        )
    )

    expected = manifest[
        "expected_profile"
    ]

    results = []

    for fixture in sorted(
        FIXTURE_DIR.iterdir()
    ):
        if fixture.suffix.lower() not in (
            ".pdf",
            ".docx",
        ):
            continue

        print(
            f"\n=== {fixture.name} ==="
        )

        try:
            text = (
                extract_text_from_cv(
                    fixture
                )
            )

            parsed = parse_cv_text(
                text
            )

            score = 0

            checks = {}

            checks["name"] = (
                parsed.full_name
                == expected["full_name"]
            )

            checks["skills"] = (
                count_match(
                    parsed.skills,
                    expected["skills"],
                )
            )

            checks["languages"] = (
                count_match(
                    parsed.languages,
                    expected["languages"],
                )
            )

            checks["experiences"] = (
                len(
                    parsed.experiences
                )
            )

            if checks["name"]:
                score += 1

            if checks["skills"] >= 4:
                score += 1

            if checks["languages"] >= 2:
                score += 1

            if checks["experiences"] >= 2:
                score += 1

            results.append(
                {
                    "file":
                        fixture.name,
                    "score":
                        score,
                    "checks":
                        checks,
                }
            )

            print(
                json.dumps(
                    checks,
                    indent=2,
                    ensure_ascii=False,
                )
            )

        except Exception as exc:
            results.append(
                {
                    "file":
                        fixture.name,
                    "error":
                        str(exc),
                }
            )

            print(
                f"ERROR: {exc}"
            )

    output = {
        "results": results
    }

    Path(
        "cv_benchmark_results.json"
    ).write_text(
        json.dumps(
            output,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    print(
        "\nResults written to:"
    )
    print(
        "cv_benchmark_results.json"
    )


if __name__ == "__main__":
    main()