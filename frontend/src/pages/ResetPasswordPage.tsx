import { useState } from "react";
import type { FormEvent } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { Card } from "../components/ui/Card";
import { resetPassword } from "../services/authApi";
import {
  getPasswordPolicyChecks,
  isPasswordPolicyValid,
} from "../utils/passwordPolicy";

export function ResetPasswordPage() {
  const [searchParams] = useSearchParams();
  const token = searchParams.get("token") ?? "";

  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  const passwordChecks = getPasswordPolicyChecks(newPassword);
  const passwordIsValid = isPasswordPolicyValid(newPassword);
  const passwordsMatch =
    confirmPassword.length > 0 && newPassword === confirmPassword;

  const canSubmit =
    Boolean(token) && passwordIsValid && passwordsMatch && !loading;

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    setError("");

    if (!token) {
      setError("This password reset link is invalid or incomplete.");
      return;
    }

    if (!passwordIsValid) {
      setError("Password does not meet the required criteria.");
      return;
    }

    if (newPassword !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    setLoading(true);

    try {
      await resetPassword(token, newPassword, confirmPassword);

      setSuccess(true);
    } catch (caughtError) {
      setError(
        caughtError instanceof Error
          ? caughtError.message
          : "Unable to reset password.",
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-slate-950 px-4">
      <div className="w-full max-w-md">
        <Card>
          <h1 className="text-2xl font-bold text-white">Reset Password</h1>

          {!token && (
            <div className="mt-4 rounded border border-red-900 bg-red-950 p-3 text-sm text-red-300">
              This password reset link is invalid or incomplete. Please request
              a new one.
            </div>
          )}

          {success ? (
            <p className="mt-6 text-sm text-green-400">
              Your password has been reset successfully.
            </p>
          ) : (
            <form onSubmit={handleSubmit} className="mt-6">
              <label
                htmlFor="new_password"
                className="mb-2 block text-sm text-slate-300">
                New Password
              </label>

              <input
                id="new_password"
                type="password"
                value={newPassword}
                onChange={(event) => setNewPassword(event.target.value)}
                required
                disabled={loading}
                className="w-full rounded border border-slate-700 bg-slate-800 p-2 text-white"
              />

              {newPassword.length > 0 && (
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

              <label
                htmlFor="confirm_password"
                className="mb-2 mt-4 block text-sm text-slate-300">
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

              {error && (
                <div className="mt-4 rounded border border-red-900 bg-red-950 p-3 text-sm text-red-300">
                  {error}
                </div>
              )}

              <button
                type="submit"
                disabled={!canSubmit}
                className="mt-4 w-full rounded bg-blue-600 px-4 py-2 font-semibold text-white hover:bg-blue-500 disabled:opacity-50">
                {loading ? "Updating..." : "Update Password"}
              </button>
            </form>
          )}

          <div className="mt-6 text-center">
            <Link to="/login" className="text-blue-400 hover:text-blue-300">
              Back To Login
            </Link>
          </div>
        </Card>
      </div>
    </main>
  );
}
