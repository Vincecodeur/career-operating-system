import { useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { Card } from "../components/ui/Card";
import { confirmEmailChange } from "../services/authApi";

export function ConfirmEmailChangePage() {
  const [searchParams] = useSearchParams();
  const token = searchParams.get("token") ?? "";

  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState("");

  async function handleConfirm() {
    setError("");
    setLoading(true);

    try {
      await confirmEmailChange(token);

      setSuccess(true);
    } catch (caughtError) {
      setError(
        caughtError instanceof Error
          ? caughtError.message
          : "Unable to confirm email change.",
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-slate-950 px-4">
      <div className="w-full max-w-md">
        <Card>
          <h1 className="text-2xl font-bold text-white">
            Confirm Email Change
          </h1>

          {!token && (
            <div className="mt-4 rounded border border-red-900 bg-red-950 p-3 text-sm text-red-300">
              This confirmation link is invalid or incomplete.
            </div>
          )}

          {success ? (
            <p className="mt-6 text-sm text-green-400">
              Your email address has been updated successfully. Please log in
              with your new email address.
            </p>
          ) : (
            token && (
              <>
                <p className="mt-4 text-slate-400">
                  Click the button below to confirm the change of your email
                  address.
                </p>

                {error && (
                  <div className="mt-4 rounded border border-red-900 bg-red-950 p-3 text-sm text-red-300">
                    {error}
                  </div>
                )}

                <button
                  type="button"
                  onClick={handleConfirm}
                  disabled={loading}
                  className="mt-6 w-full rounded bg-blue-600 px-4 py-2 font-semibold text-white hover:bg-blue-500 disabled:opacity-50">
                  {loading ? "Confirming..." : "Confirm Email Change"}
                </button>
              </>
            )
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
