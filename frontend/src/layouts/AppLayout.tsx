import { Link, Outlet, useNavigate } from "react-router-dom";

import { useAuthStore } from "../stores/authStore";

export function AppLayout() {
  const navigate = useNavigate();

  const logout = useAuthStore((state) => state.logout);

  function handleLogout() {
    logout();

    navigate("/login", {
      replace: true,
    });
  }

  return (
    <div>
      <nav
        style={{
          padding: "1rem",
          borderBottom: "1px solid #ddd",
          display: "flex",
          gap: "1rem",
        }}>
        <Link to="/dashboard">Dashboard</Link>

        <Link to="/account">Account</Link>

        <button type="button" onClick={handleLogout}>
          Logout
        </button>
      </nav>

      <header
        style={{
          padding: "1rem",
          borderBottom: "1px solid #ddd",
        }}>
        Header Placeholder
      </header>

      <main
        style={{
          padding: "1rem",
        }}>
        <Outlet />
      </main>
    </div>
  );
}
