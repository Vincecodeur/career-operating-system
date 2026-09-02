import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Card } from "../components/ui/Card";
import { PageHeader } from "../components/ui/PageHeader";
import { useAuthStore } from "../stores/authStore";

export function AccountPage() {
  const navigate = useNavigate();

  const user = useAuthStore((state) => state.user);

  const loadCurrentUser = useAuthStore((state) => state.loadCurrentUser);

  const logout = useAuthStore((state) => state.logout);

  useEffect(() => {
    loadCurrentUser();
  }, [loadCurrentUser]);

  function handleLogout() {
    logout();

    navigate("/login", {
      replace: true,
    });
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
      </Card>

      <Card>
        <h2 className="mb-4 text-lg font-semibold text-white">
          Authentication Roadmap
        </h2>

        <ul className="space-y-2 text-slate-400">
          <li>✅ Login</li>
          <li>✅ Password Recovery</li>
          <li>⬜ Sign Up</li>
          <li>⬜ Remember Me</li>
          <li>⬜ Email Recovery</li>
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
