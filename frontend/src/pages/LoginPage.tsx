import { useState } from "react";
import type { FormEvent } from "react";

import { Link, useNavigate } from "react-router-dom";

import { Card } from "../components/ui/Card";
import { useAuthStore } from "../stores/authStore";

export function LoginPage() {
  const navigate = useNavigate();
  const login = useAuthStore((state) => state.login);

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    setError("");
    setLoading(true);

    try {
      await login(email, password);

      navigate("/dashboard", {
        replace: true,
      });
    } catch {
      setError("Invalid email or password.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-slate-950 px-4">
      <div className="w-full max-w-md">
        <Card>
          <div className="text-center">
            <h1 className="text-2xl font-bold text-white">
              Career Operating System
            </h1>

            <h2 className="mt-6 text-xl font-semibold text-white">
              Welcome Back
            </h2>

            <p className="mt-2 text-sm text-slate-400">
              Sign in to access your profiles, opportunities and application
              tracking.
            </p>
          </div>

          <form onSubmit={handleSubmit} className="mt-8 space-y-4">
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
                className="w-full rounded border border-slate-700 bg-slate-800 p-2 text-white"
              />
            </div>

            <div className="text-sm text-slate-500">
              Remember Me (Coming Soon)
            </div>

            {error && (
              <div className="rounded border border-red-900 bg-red-950 p-3 text-sm text-red-300">
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full rounded bg-blue-600 px-4 py-2 font-semibold text-white hover:bg-blue-500 disabled:opacity-50">
              {loading ? "Logging in..." : "Login"}
            </button>
          </form>

          <div className="mt-6 space-y-2 text-center text-sm">
            <Link
              to="/forgot-password"
              className="text-blue-400 hover:text-blue-300">
              Forgot Password?
            </Link>

            <p className="text-slate-500">
              Don't have an account?{" "}
              <Link to="/signup" className="text-blue-400 hover:text-blue-300">
                Sign Up
              </Link>
            </p>
          </div>
        </Card>
      </div>
    </main>
  );
}
