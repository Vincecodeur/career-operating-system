import { useState } from "react";
import type { FormEvent } from "react";
import { Card } from "../components/ui/Card";
import { Link } from "react-router-dom";

export function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [submitted, setSubmitted] = useState(false);

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    setSubmitted(true);
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-slate-950 px-4">
      <div className="w-full max-w-md">
        <Card>
          <h1 className="text-2xl font-bold text-white">Password Recovery</h1>

          <p className="mt-4 text-slate-400">
            Password recovery will be implemented during the Authentication
            Learning Features phase.
          </p>

          <div className="mt-6 rounded border border-slate-700 bg-slate-950 p-4">
            <h2 className="font-semibold text-white">
              Planned Authentication Features
            </h2>

            <ul className="mt-3 space-y-2 text-sm text-slate-400">
              <li>• Remember Me</li>
              <li>• Password Recovery</li>
              <li>• Email Recovery</li>
              <li>• Session Management</li>
            </ul>
          </div>

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
              className="w-full rounded border border-slate-700 bg-slate-800 p-2 text-white"
            />

            <button
              type="submit"
              className="mt-4 w-full rounded bg-blue-600 px-4 py-2 font-semibold text-white hover:bg-blue-500">
              Send Reset Link
            </button>
          </form>

          {submitted && (
            <p className="mt-4 text-sm text-green-400">
              Recovery workflow is not enabled yet.
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
