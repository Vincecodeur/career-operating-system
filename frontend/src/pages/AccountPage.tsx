import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

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
    <main style={{ padding: "2rem" }}>
      <h1>My Account</h1>

      <section>
        <h2>Account Information</h2>

        <p>
          <strong>Email:</strong> {user?.email ?? "Not loaded"}
        </p>

        <p>
          <strong>Status:</strong> {user?.is_active ? "Active" : "Unknown"}
        </p>
      </section>

      <section style={{ marginTop: "2rem" }}>
        <h2>Preferences</h2>

        <p>Language and theme preferences will be implemented later.</p>
      </section>

      <button
        type="button"
        onClick={handleLogout}
        style={{ marginTop: "2rem" }}>
        Logout
      </button>
    </main>
  );
}
