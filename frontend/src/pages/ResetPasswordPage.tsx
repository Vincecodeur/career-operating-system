import { useState } from "react";
import type { FormEvent } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { Card } from "../components/ui/Card";
import { resetPassword } from "../services/authApi";

export function ResetPasswordPage() {
  const [searchParams] = useSearchParams();
  const token = searchParams.get("token") ?? "";

  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    setError("");

    if (!token) {
      setError("This password reset link is invalid or incomplete.");
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
            <div className="mt-6">
              <p className="text-sm text-green-400">
                Your password has been reset successfully.
              </p>

              <div className="mt-6 text-center">
                <Link to="/login" className="text-blue-400 hover:text-blue-300">
                  Back To Login
                </Link>
              </div>
            </div>
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
                minLength={8}
                disabled={loading}
                className="w-full rounded border border-slate-700 bg-slate-800 p-2 text-white"
              />

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
                minLength={8}
                disabled={loading}
                className="w-full rounded border border-slate-700 bg-slate-800 p-2 text-white"
              />

              {error && (
                <div className="mt-4 rounded border border-red-900 bg-red-950 p-3 text-sm text-red-300">
                  {error}
                </div>
              )}

              <button
                type="submit"
                disabled={loading || !token}
                className="mt-4 w-full rounded bg-blue-600 px-4 py-2 font-semibold text-white hover:bg-blue-500 disabled:opacity-50">
                {loading ? "Updating..." : "Update Password"}
              </button>
            </form>
          )}
        </Card>
      </div>
    </main>
  );
}
