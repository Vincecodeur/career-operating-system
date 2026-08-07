import { Link, Outlet, useNavigate } from "react-router-dom";

import { useAuthStore } from "../stores/authStore";

export function AppLayout() {
  const navigate = useNavigate();

  const logout = useAuthStore((state) => state.logout);

  const user = useAuthStore((state) => state.user);

  function handleLogout() {
    logout();

    navigate("/login", {
      replace: true,
    });
  }

  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns: "240px 1fr",
        minHeight: "100vh",
      }}>
      <aside
        style={{
          borderRight: "1px solid #ddd",
          padding: "1rem",
        }}>
        <h2>Career OS</h2>

        <nav
          style={{
            display: "flex",
            flexDirection: "column",
            gap: "1rem",
            marginTop: "2rem",
          }}>
          <Link to="/dashboard">Dashboard</Link>

          <Link to="/account">Account</Link>
        </nav>

        <button
          type="button"
          onClick={handleLogout}
          style={{
            marginTop: "2rem",
          }}>
          Logout
        </button>
      </aside>

      <div>
        <header
          style={{
            borderBottom: "1px solid #ddd",
            padding: "1rem",
            display: "flex",
            justifyContent: "space-between",
          }}>
          <strong>Career Operating System</strong>

          <span>{user?.email ?? "Anonymous"}</span>
        </header>

        <main
          style={{
            padding: "1rem",
          }}>
          <Outlet />
        </main>
      </div>
    </div>
  );
}
