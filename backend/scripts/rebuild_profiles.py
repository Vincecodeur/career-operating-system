import argparse
import sys
from pathlib import Path

sys.path.append(
    str(
        Path(__file__)
        .resolve()
        .parent.parent
    )
)

from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.profile.models import Profile
from app.profile.profile_skill_models import ProfileSkill
from app.skills.models import Skill


EXPECTED_PROFILE_IDS = {
    1,
    2,
    3,
    4,
}


PROFILE_CONFIGURATION = {
    1: {
        "profile_name": (
            "Technical Partnerships"
        ),
        "current_title": (
            "Technical Partnerships Manager"
        ),
        "skills": [
            "API REST",
            "Azure",
            "Salesforce",
            "JIRA",
            "Confluence",
            "Documentation",
            "GraphQL",
        ],
    },
    2: {
        "profile_name": "Frontend",
        "current_title": (
            "Frontend Engineer"
        ),
        "skills": [
            "React",
            "JavaScript",
            "HTML",
            "CSS",
            "Node.js",
        ],
    },
    3: {
        "profile_name": "Cloud",
        "current_title": (
            "Cloud Architect"
        ),
        "skills": [
            "Azure",
            "Docker",
            "Kubernetes",
            "Terraform",
            "Ansible",
        ],
    },
    4: {
        "profile_name": "Data",
        "current_title": (
            "Data Analyst"
        ),
        "skills": [
            "Python",
            "PostgreSQL",
            "COGNOS",
            "Data mapping",
            "Power Platform",
            "PowerApps",
            "Power Automate",
            "Excel",
            "Pivot Tables",
            "VBA",
        ],
    },
}


def get_required_skill_names() -> set[str]:
    return {
        skill_name
        for configuration
        in PROFILE_CONFIGURATION.values()
        for skill_name
        in configuration["skills"]
    }


def validate_profiles(
    db: Session,
) -> dict[int, Profile]:
    profiles = (
        db.query(Profile)
        .filter(
            Profile.id.in_(
                EXPECTED_PROFILE_IDS
            )
        )
        .all()
    )

    profiles_by_id = {
        profile.id: profile
        for profile in profiles
    }

    found_profile_ids = set(
        profiles_by_id.keys()
    )

    missing_profile_ids = (
        EXPECTED_PROFILE_IDS
        - found_profile_ids
    )

    if missing_profile_ids:
        raise RuntimeError(
            "Missing required profiles: "
            f"{sorted(missing_profile_ids)}"
        )

    return profiles_by_id


def validate_skills(
    db: Session,
) -> dict[str, Skill]:
    required_skill_names = (
        get_required_skill_names()
    )

    skills = (
        db.query(Skill)
        .filter(
            Skill.name.in_(
                required_skill_names
            )
        )
        .all()
    )

    skills_by_name = {
        skill.name: skill
        for skill in skills
    }

    found_skill_names = set(
        skills_by_name.keys()
    )

    missing_skill_names = (
        required_skill_names
        - found_skill_names
    )

    if missing_skill_names:
        raise RuntimeError(
            "Missing required skills: "
            f"{sorted(missing_skill_names)}"
        )

    return skills_by_name


def print_current_state(
    db: Session,
    profiles_by_id: dict[int, Profile],
) -> None:
    print()
    print("=" * 80)
    print("CURRENT PROFILE STATE")
    print("=" * 80)

    for profile_id in sorted(
        profiles_by_id
    ):
        profile = profiles_by_id[
            profile_id
        ]

        current_skills = (
            db.query(Skill.name)
            .join(
                ProfileSkill,
                ProfileSkill.skill_id
                == Skill.id,
            )
            .filter(
                ProfileSkill.profile_id
                == profile_id,
            )
            .order_by(Skill.name)
            .all()
        )

        skill_names = [
            row[0]
            for row in current_skills
        ]

        print()
        print(
            f"Profile {profile_id}: "
            f"{profile.profile_name}"
        )

        print(
            "Current title: "
            f"{profile.current_title}"
        )

        print(
            "Current skills "
            f"({len(skill_names)}):"
        )

        if skill_names:
            for skill_name in skill_names:
                print(
                    f"  - {skill_name}"
                )
        else:
            print("  - None")


def print_planned_state() -> None:
    print()
    print("=" * 80)
    print("PLANNED PROFILE STATE")
    print("=" * 80)

    for profile_id in sorted(
        PROFILE_CONFIGURATION
    ):
        configuration = (
            PROFILE_CONFIGURATION[
                profile_id
            ]
        )

        print()
        print(
            f"Profile {profile_id}: "
            f"{configuration['profile_name']}"
        )

        print(
            "New title: "
            f"{configuration['current_title']}"
        )

        print(
            "New skills "
            f"({len(configuration['skills'])}):"
        )

        for skill_name in (
            configuration["skills"]
        ):
            print(
                f"  - {skill_name}"
            )


def delete_current_profile_skills(
    db: Session,
) -> int:
    deleted_count = (
        db.query(ProfileSkill)
        .filter(
            ProfileSkill.profile_id.in_(
                EXPECTED_PROFILE_IDS
            )
        )
        .delete(
            synchronize_session=False
        )
    )

    db.flush()

    return deleted_count


def update_profiles(
    profiles_by_id: dict[int, Profile],
) -> None:
    for profile_id, configuration in (
        PROFILE_CONFIGURATION.items()
    ):
        profile = profiles_by_id[
            profile_id
        ]

        profile.profile_name = (
            configuration[
                "profile_name"
            ]
        )

        profile.current_title = (
            configuration[
                "current_title"
            ]
        )

        profile.is_active = True


def create_profile_skills(
    db: Session,
    skills_by_name: dict[str, Skill],
) -> int:
    created_count = 0

    for profile_id, configuration in (
        PROFILE_CONFIGURATION.items()
    ):
        for skill_name in (
            configuration["skills"]
        ):
            skill = skills_by_name[
                skill_name
            ]

            db.add(
                ProfileSkill(
                    profile_id=profile_id,
                    skill_id=skill.id,
                    years_of_experience=3,
                    self_assessment_level=(
                        "Advanced"
                    ),
                )
            )

            created_count += 1

    db.flush()

    return created_count


def validate_final_state(
    db: Session,
) -> None:
    expected_total = sum(
        len(
            configuration["skills"]
        )
        for configuration
        in PROFILE_CONFIGURATION.values()
    )

    actual_total = (
        db.query(ProfileSkill)
        .filter(
            ProfileSkill.profile_id.in_(
                EXPECTED_PROFILE_IDS
            )
        )
        .count()
    )

    if actual_total != expected_total:
        raise RuntimeError(
            "Invalid number of profile "
            "skills after rebuild. "
            f"Expected {expected_total}, "
            f"found {actual_total}."
        )

    for profile_id, configuration in (
        PROFILE_CONFIGURATION.items()
    ):
        actual_skill_names = {
            row[0]
            for row in (
                db.query(Skill.name)
                .join(
                    ProfileSkill,
                    ProfileSkill.skill_id
                    == Skill.id,
                )
                .filter(
                    ProfileSkill.profile_id
                    == profile_id,
                )
                .all()
            )
        }

        expected_skill_names = set(
            configuration["skills"]
        )

        if (
            actual_skill_names
            != expected_skill_names
        ):
            missing_skills = (
                expected_skill_names
                - actual_skill_names
            )

            unexpected_skills = (
                actual_skill_names
                - expected_skill_names
            )

            raise RuntimeError(
                "Invalid skills for profile "
                f"{profile_id}. "
                "Missing: "
                f"{sorted(missing_skills)}. "
                "Unexpected: "
                f"{sorted(unexpected_skills)}."
            )

        profile = (
            db.query(Profile)
            .filter(
                Profile.id == profile_id
            )
            .one()
        )

        if (
            profile.profile_name
            != configuration[
                "profile_name"
            ]
        ):
            raise RuntimeError(
                "Invalid profile name for "
                f"profile {profile_id}."
            )

        if (
            profile.current_title
            != configuration[
                "current_title"
            ]
        ):
            raise RuntimeError(
                "Invalid current title for "
                f"profile {profile_id}."
            )

        if not profile.is_active:
            raise RuntimeError(
                "Profile is not active after "
                f"rebuild: {profile_id}."
            )

    print()
    print("=" * 80)
    print("FINAL VALIDATION")
    print("=" * 80)
    print()
    print(
        "Profile skills rebuilt: "
        f"{actual_total}"
    )
    print(
        "Profiles validated: "
        f"{len(EXPECTED_PROFILE_IDS)}"
    )
    print(
        "All profiles remain active."
    )


def preview() -> None:
    db = SessionLocal()

    try:
        profiles_by_id = (
            validate_profiles(db)
        )

        validate_skills(db)

        print_current_state(
            db,
            profiles_by_id,
        )

        print_planned_state()

        print()
        print(
            "Preview only. "
            "No data was modified."
        )

    finally:
        db.close()


def apply_rebuild() -> None:
    db = SessionLocal()

    try:
        profiles_by_id = (
            validate_profiles(db)
        )

        skills_by_name = (
            validate_skills(db)
        )

        print_current_state(
            db,
            profiles_by_id,
        )

        print_planned_state()

        print()
        print(
            "Applying profile rebuild..."
        )

        deleted_count = (
            delete_current_profile_skills(
                db
            )
        )

        update_profiles(
            profiles_by_id
        )

        created_count = (
            create_profile_skills(
                db,
                skills_by_name,
            )
        )

        validate_final_state(db)

        db.commit()

        print()
        print(
            "Profile rebuild committed."
        )

        print(
            "Deleted old profile skill "
            f"links: {deleted_count}"
        )

        print(
            "Created new profile skill "
            f"links: {created_count}"
        )

    except Exception as error:
        db.rollback()

        print()
        print(
            "Profile rebuild failed."
        )

        print(
            "Transaction rolled back."
        )

        print(str(error))

        raise

    finally:
        db.close()


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Rebuild the four Career OS "
            "demo profiles."
        )
    )

    parser.add_argument(
        "--apply",
        action="store_true",
        help=(
            "Apply the profile rebuild. "
            "Without this flag, the script "
            "runs in preview mode."
        ),
    )

    arguments = parser.parse_args()

    if arguments.apply:
        apply_rebuild()
    else:
        preview()


if __name__ == "__main__":
    main()