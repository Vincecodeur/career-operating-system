import { useEffect, useState } from "react";
import type { FormEvent } from "react";
import { useNavigate } from "react-router-dom";
import { Card } from "../components/ui/Card";
import { PageHeader } from "../components/ui/PageHeader";
import { useAuthStore } from "../stores/authStore";
import { requestEmailChange } from "../services/authApi";

export function AccountPage() {
  const navigate = useNavigate();

  const user = useAuthStore((state) => state.user);

  const loadCurrentUser = useAuthStore((state) => state.loadCurrentUser);

  const logout = useAuthStore((state) => state.logout);

  const accessToken = useAuthStore((state) => state.accessToken);

  const [newEmail, setNewEmail] = useState("");
  const [emailChangeLoading, setEmailChangeLoading] = useState(false);
  const [emailChangeMessage, setEmailChangeMessage] = useState("");
  const [emailChangeError, setEmailChangeError] = useState("");

  useEffect(() => {
    loadCurrentUser();
  }, [loadCurrentUser]);

  function handleLogout() {
    logout();

    navigate("/login", {
      replace: true,
    });
  }

  async function handleRequestEmailChange(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!accessToken) {
      return;
    }

    setEmailChangeError("");
    setEmailChangeMessage("");
    setEmailChangeLoading(true);

    try {
      const response = await requestEmailChange(accessToken, newEmail);

      setEmailChangeMessage(response.message);
      setNewEmail("");
    } catch (caughtError) {
      setEmailChangeError(
        caughtError instanceof Error
          ? caughtError.message
          : "Unable to request email change.",
      );
    } finally {
      setEmailChangeLoading(false);
    }
  }

  return (
    <main className="space-y-6">
      <PageHeader
        title="My Account"
        description="Manage authentication and account preferences."
      />

      <Card>
        <h2 className="mb-4 text-lg font-semibold text-white">
          Account Information
        </h2>

        <p className="text-slate-300">
          <strong>Email:</strong> {user?.email ?? "Not loaded"}
        </p>

        <p className="mt-2 text-slate-300">
          <strong>Status:</strong> {user?.is_active ? "Active" : "Unknown"}
        </p>
      </Card>

      <Card>
        <h2 className="mb-4 text-lg font-semibold text-white">
          Authentication
        </h2>

        <p className="text-slate-300">
          Authentication Method: JWT Access Token
        </p>

        <p className="mt-2 text-slate-300">Account Mode: Single User MVP</p>

        <div className="mt-6 border-t border-slate-700 pt-6">
          <h3 className="mb-2 text-sm font-semibold text-white">
            Change Email
          </h3>

          <p className="mb-3 text-sm text-slate-400">
            A confirmation link will be sent to your current email address.
          </p>

          <form onSubmit={handleRequestEmailChange}>
            <label
              htmlFor="new_email"
              className="mb-2 block text-sm text-slate-300">
              New Email
            </label>

            <input
              id="new_email"
              type="email"
              value={newEmail}
              onChange={(event) => setNewEmail(event.target.value)}
              required
              disabled={emailChangeLoading}
              className="w-full rounded border border-slate-700 bg-slate-800 p-2 text-white"
            />

            {emailChangeError && (
              <div className="mt-3 rounded border border-red-900 bg-red-950 p-3 text-sm text-red-300">
                {emailChangeError}
              </div>
            )}

            {emailChangeMessage && (
              <div className="mt-3 rounded border border-green-900 bg-green-950 p-3 text-sm text-green-300">
                {emailChangeMessage}
              </div>
            )}

            <button
              type="submit"
              disabled={emailChangeLoading}
              className="mt-3 rounded bg-blue-600 px-4 py-2 text-sm font-semibold text-white hover:bg-blue-500 disabled:opacity-50">
              {emailChangeLoading ? "Sending..." : "Request Email Change"}
            </button>
          </form>
        </div>
      </Card>

      <Card>
        <h2 className="mb-4 text-lg font-semibold text-white">
          Authentication Roadmap
        </h2>

        <ul className="space-y-2 text-slate-400">
          <li>✅ Login</li>
          <li>✅ Password Recovery</li>
          <li>✅ Email Recovery</li>
          <li>✅ Sign Up</li>
          <li>✅ Remember Me</li>
          <li>⬜ MFA</li>
          <li>⬜ SSO</li>
        </ul>
      </Card>

      <Card>
        <h2 className="mb-4 text-lg font-semibold text-white">Session</h2>

        <button
          type="button"
          onClick={handleLogout}
          className="rounded bg-red-600 px-4 py-2 text-white hover:bg-red-500">
          Logout
        </button>
      </Card>
    </main>
  );
}
