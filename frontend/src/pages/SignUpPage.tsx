import { useState } from "react";
import type { FormEvent } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Card } from "../components/ui/Card";
import { registerUser } from "../services/authApi";
import {
  getPasswordPolicyChecks,
  isPasswordPolicyValid,
} from "../utils/passwordPolicy";

export function SignUpPage() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  const passwordChecks = getPasswordPolicyChecks(password);
  const passwordIsValid = isPasswordPolicyValid(password);
  const passwordsMatch =
    confirmPassword.length > 0 && password === confirmPassword;

  const canSubmit =
    email.length > 0 && passwordIsValid && passwordsMatch && !loading;

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    setError("");

    if (!passwordIsValid) {
      setError("Password does not meet the required criteria.");
      return;
    }

    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    setLoading(true);

    try {
      await registerUser(email, password, confirmPassword);

      setSuccess(true);
    } catch (caughtError) {
      setError(
        caughtError instanceof Error
          ? caughtError.message
          : "Unable to create account.",
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-slate-950 px-4">
      <div className="w-full max-w-md">
        <Card>
          <h1 className="text-2xl font-bold text-white">Create Account</h1>

          {success ? (
            <div className="mt-6">
              <p className="text-sm text-green-400">
                Your account has been created successfully.
              </p>

              <button
                type="button"
                onClick={() => navigate("/login")}
                className="mt-4 w-full rounded bg-blue-600 px-4 py-2 font-semibold text-white hover:bg-blue-500">
                Go to Login
              </button>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="mt-6 space-y-4">
              <div>
                <label
                  htmlFor="email"
                  className="mb-1 block text-sm text-slate-300">
                  Email
                </label>

                <input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(event) => setEmail(event.target.value)}
                  required
                  disabled={loading}
                  className="w-full rounded border border-slate-700 bg-slate-800 p-2 text-white"
                />
              </div>

              <div>
                <label
                  htmlFor="password"
                  className="mb-1 block text-sm text-slate-300">
                  Password
                </label>

                <input
                  id="password"
                  type="password"
                  value={password}
                  onChange={(event) => setPassword(event.target.value)}
                  required
                  disabled={loading}
                  className="w-full rounded border border-slate-700 bg-slate-800 p-2 text-white"
                />

                {password.length > 0 && (
                  <ul className="mt-2 space-y-1 text-xs">
                    {passwordChecks.map((check) => (
                      <li
                        key={check.label}
                        className={
                          check.isValid ? "text-green-400" : "text-slate-500"
                        }>
                        {check.isValid ? "✓" : "○"} {check.label}
                      </li>
                    ))}
                  </ul>
                )}
              </div>

              <div>
                <label
                  htmlFor="confirm_password"
                  className="mb-1 block text-sm text-slate-300">
                  Confirm Password
                </label>

                <input
                  id="confirm_password"
                  type="password"
                  value={confirmPassword}
                  onChange={(event) => setConfirmPassword(event.target.value)}
                  required
                  disabled={loading}
                  className="w-full rounded border border-slate-700 bg-slate-800 p-2 text-white"
                />

                {confirmPassword.length > 0 && (
                  <p
                    className={
                      passwordsMatch
                        ? "mt-2 text-xs text-green-400"
                        : "mt-2 text-xs text-red-400"
                    }>
                    {passwordsMatch
                      ? "✓ Passwords match"
                      : "○ Passwords do not match"}
                  </p>
                )}
              </div>

              {error && (
                <div className="rounded border border-red-900 bg-red-950 p-3 text-sm text-red-300">
                  {error}
                </div>
              )}

              <button
                type="submit"
                disabled={!canSubmit}
                className="w-full rounded bg-blue-600 px-4 py-2 font-semibold text-white hover:bg-blue-500 disabled:opacity-50">
                {loading ? "Creating account..." : "Create Account"}
              </button>
            </form>
          )}

          <div className="mt-6 text-center text-sm">
            <Link to="/login" className="text-blue-400 hover:text-blue-300">
              Already have an account? Login
            </Link>
          </div>
        </Card>
      </div>
    </main>
  );
}
