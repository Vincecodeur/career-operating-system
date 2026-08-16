SOFT_SKILL_NAMES = {
    "adaptability",
    "agile mindset",
    "collaboration",
    "communication",
    "conflict resolution",
    "curious",
    "curiosity",
    "horizontal management",
    "leadership",
    "mentoring",
    "negotiation",
    "problem solving",
    "proactive",
    "reliable",
    "reliability",
    "resilience",
    "stress management",
    "team spirit",
    "teamwork",
    "versatile",
    "versatility",
    "cross-functional collaboration",
    "functional collaboration",
}

IGNORED_SKILL_VALUES = {
    "skill",
    "skills",
    "hard skill",
    "hard skills",
    "soft skill",
    "soft skills",
    "technical skill",
    "technical skills",
    "competency",
    "competencies",
    "core skill",
    "core skills",
}


def normalize_dictionary_value(
    value: str,
) -> str:
    return " ".join(
        value.strip().lower().split(),
    )


def is_ignored_skill_value(
    value: str,
) -> bool:
    return normalize_dictionary_value(
        value,
    ) in IGNORED_SKILL_VALUES


def is_soft_skill_name(
    value: str,
) -> bool:
    return normalize_dictionary_value(
        value,
    ) in SOFT_SKILL_NAMES