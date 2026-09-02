import { useState } from "react";
import type { FormEvent } from "react";
import { Card } from "../components/ui/Card";
import { Link } from "react-router-dom";
import { requestPasswordReset } from "../services/authApi";

export function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    setError("");
    setLoading(true);

    try {
      await requestPasswordReset(email);

      setSubmitted(true);
    } catch {
      setError(
        "Unable to send password recovery instructions. Please try again.",
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-slate-950 px-4">
      <div className="w-full max-w-md">
        <Card>
          <h1 className="text-2xl font-bold text-white">Password Recovery</h1>

          <p className="mt-4 text-slate-400">
            Enter your email address and we will send you a link to reset your
            password.
          </p>

          <form onSubmit={handleSubmit} className="mt-6">
            <label
              htmlFor="email"
              className="mb-2 block text-sm text-slate-300">
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

            {error && (
              <div className="mt-4 rounded border border-red-900 bg-red-950 p-3 text-sm text-red-300">
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="mt-4 w-full rounded bg-blue-600 px-4 py-2 font-semibold text-white hover:bg-blue-500 disabled:opacity-50">
              {loading ? "Sending..." : "Send Reset Link"}
            </button>
          </form>

          {submitted && (
            <p className="mt-4 text-sm text-green-400">
              If an account exists for this email, password recovery
              instructions have been sent.
            </p>
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
