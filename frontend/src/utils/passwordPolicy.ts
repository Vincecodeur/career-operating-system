export type PasswordPolicyCheck = {
  label: string;
  isValid: boolean;
};

const PASSWORD_MIN_LENGTH = 8;

export function getPasswordPolicyChecks(
  password: string,
): PasswordPolicyCheck[] {
  return [
    {
      label: `At least ${PASSWORD_MIN_LENGTH} characters`,
      isValid: password.length >= PASSWORD_MIN_LENGTH,
    },
    {
      label: "One uppercase letter",
      isValid: /[A-Z]/.test(password),
    },
    {
      label: "One lowercase letter",
      isValid: /[a-z]/.test(password),
    },
    {
      label: "One digit",
      isValid: /[0-9]/.test(password),
    },
    {
      label: "One special character",
      isValid: /[^A-Za-z0-9]/.test(password),
    },
  ];
}

export function isPasswordPolicyValid(
  password: string,
): boolean {
  return getPasswordPolicyChecks(password).every(
    (check) => check.isValid,
  );
}