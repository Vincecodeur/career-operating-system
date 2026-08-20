import sys
from pathlib import Path
from collections import defaultdict

sys.path.append(
    str(
        Path(__file__)
        .resolve()
        .parent.parent
    )
)

from app.core.database import SessionLocal
from app.skills.models import Skill
from app.profile.profile_skill_models import ProfileSkill
from app.jobs.job_offer_skill_models import JobOfferSkill


KEEP_EXACT = {
    "Python",
    "FastAPI",
    "PostgreSQL",
    "React",
    "Azure",
    "Docker",
    "Kubernetes",
    "Terraform",
    "Ansible",
    "API REST",
    "GraphQL",
    "Power Platform",
    "PowerApps",
    "Power Automate",
    "PowerQuery",
    "HTML",
    "CSS",
    "JavaScript",
    "MongoDB",
    "Node.js",
    "Salesforce",
    "ServiceNow",
    "COGNOS",
    "JIRA",
    "Confluence",
    "Documentation",
    "Data mapping",
    "Process automation",
    "Agile",
    "Software testing",
    "UAT",
    "Regression",
    "Change Request",
    "Excel",
    "Pivot Tables",
    "VBA",
    "Apps Script",
    "Google Appsheet",
}

DELETE_PREFIXES = (
    "Skill_",
    "Docker_",
    "FastAPI_",
    "FastApi_",
    "Kubernetes_",
    "Terraform_",
)

DELETE_EXACT = {
    "17/01/2022",
    "Kubernetes_Test_001",
}

REVIEW_KEYWORDS = (
    "Cross",
    "development",
    "Tables",
    "Low -code",
    "Excel (Pivot",
    "JS",
    "FastApi",
)


def classify_skill(skill_name: str) -> str:

    if skill_name in KEEP_EXACT:
        return "KEEP"

    if skill_name in DELETE_EXACT:
        return "DELETE"

    if skill_name.startswith(
        DELETE_PREFIXES
    ):
        return "DELETE"

    for keyword in REVIEW_KEYWORDS:
        if keyword.lower() in skill_name.lower():
            return "REVIEW"

    return "REVIEW"


def main():

    db = SessionLocal()

    try:

        skills = (
            db.query(Skill)
            .order_by(
                Skill.name
            )
            .all()
        )

        profile_skill_usage = defaultdict(
            int
        )

        job_offer_skill_usage = defaultdict(
            int
        )

        for link in (
            db.query(
                ProfileSkill
            ).all()
        ):
            profile_skill_usage[
                link.skill_id
            ] += 1

        for link in (
            db.query(
                JobOfferSkill
            ).all()
        ):
            job_offer_skill_usage[
                link.skill_id
            ] += 1

        keep_skills = []
        delete_skills = []
        review_skills = []

        print()
        print("=" * 80)
        print("SKILLS AUDIT")
        print("=" * 80)

        print()
        print(
            f"Total skills: {len(skills)}"
        )

        for skill in skills:

            category = classify_skill(
                skill.name
            )

            profile_usage = (
                profile_skill_usage[
                    skill.id
                ]
            )

            offer_usage = (
                job_offer_skill_usage[
                    skill.id
                ]
            )

            entry = {
                "id": skill.id,
                "name": skill.name,
                "profile_usage":
                    profile_usage,
                "offer_usage":
                    offer_usage,
            }

            if category == "KEEP":
                keep_skills.append(
                    entry
                )

            elif category == "DELETE":
                delete_skills.append(
                    entry
                )

            else:
                review_skills.append(
                    entry
                )

        print()
        print(
            f"KEEP   : {len(keep_skills)}"
        )

        print(
            f"DELETE : {len(delete_skills)}"
        )

        print(
            f"REVIEW : {len(review_skills)}"
        )

        report_path = (
            Path(__file__).parent
            / "skills_audit_report.txt"
        )

        with open(
            report_path,
            "w",
            encoding="utf-8",
        ) as report:

            report.write(
                "SKILLS AUDIT REPORT\n"
            )

            report.write(
                "=" * 80
            )

            report.write("\n\n")

            report.write(
                f"Total Skills : {len(skills)}\n"
            )

            report.write(
                f"KEEP         : {len(keep_skills)}\n"
            )

            report.write(
                f"DELETE       : {len(delete_skills)}\n"
            )

            report.write(
                f"REVIEW       : {len(review_skills)}\n\n"
            )

            report.write("KEEP\n")
            report.write("-" * 80)
            report.write("\n")

            for item in keep_skills:

                report.write(
                    f"[{item['id']}] "
                    f"{item['name']} | "
                    f"profile_usage="
                    f"{item['profile_usage']} | "
                    f"offer_usage="
                    f"{item['offer_usage']}\n"
                )

            report.write(
                "\n\nDELETE\n"
            )

            report.write(
                "-" * 80
            )

            report.write("\n")

            for item in delete_skills:

                report.write(
                    f"[{item['id']}] "
                    f"{item['name']} | "
                    f"profile_usage="
                    f"{item['profile_usage']} | "
                    f"offer_usage="
                    f"{item['offer_usage']}\n"
                )

            report.write(
                "\n\nREVIEW\n"
            )

            report.write(
                "-" * 80
            )

            report.write("\n")

            for item in review_skills:

                report.write(
                    f"[{item['id']}] "
                    f"{item['name']} | "
                    f"profile_usage="
                    f"{item['profile_usage']} | "
                    f"offer_usage="
                    f"{item['offer_usage']}\n"
                )

        print()
        print(
            "Report generated:"
        )
        print(report_path)

        print()
        print(
            "Audit completed."
        )

    finally:
        db.close()


if __name__ == "__main__":
    main()