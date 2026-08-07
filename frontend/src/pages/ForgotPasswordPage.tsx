import { useState } from "react";
import type { FormEvent } from "react";

import { Link } from "react-router-dom";

export function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [submitted, setSubmitted] = useState(false);

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    setSubmitted(true);
  }

  return (
    <main style={{ padding: "2rem" }}>
      <h1>Forgot Password</h1>

      <p>
        Password reset is not implemented yet. This page is a frontend
        placeholder for the MVP authentication flow.
      </p>

      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="email">Email</label>
          <br />
          <input
            id="email"
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            required
          />
        </div>

        <button type="submit" style={{ marginTop: "1rem" }}>
          Send reset link
        </button>
      </form>

      {submitted && (
        <p>
          If password reset is enabled later, instructions will be sent to this
          email.
        </p>
      )}

      <p style={{ marginTop: "1rem" }}>
        <Link to="/login">Back to login</Link>
      </p>
    </main>
  );
}
