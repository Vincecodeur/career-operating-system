import re


PASSWORD_MIN_LENGTH = 8


def get_password_policy_violations(
    password: str,
) -> list[str]:
    violations: list[str] = []

    if len(password) < PASSWORD_MIN_LENGTH:
        violations.append(
            f"at least {PASSWORD_MIN_LENGTH} characters"
        )

    if not re.search(r"[A-Z]", password):
        violations.append(
            "one uppercase letter"
        )

    if not re.search(r"[a-z]", password):
        violations.append(
            "one lowercase letter"
        )

    if not re.search(r"[0-9]", password):
        violations.append(
            "one digit"
        )

    if not re.search(r"[^A-Za-z0-9]", password):
        violations.append(
            "one special character"
        )

    return violations