const API_BASE_URL = "http://127.0.0.1:8000";

export type AuthUser = {
  id: number;
  email: string;
  is_active: boolean;
};

export type LoginResponse = {
  access_token: string;
  token_type: string;
  user: AuthUser;
};

export type MessageResponse = {
  message: string;
};

async function getAuthApiErrorMessage(
  response: Response,
  fallbackMessage: string,
): Promise<string> {
  try {
    const data = await response.json();

    if (data && typeof data.detail === "string") {
      return data.detail;
    }

    return fallbackMessage;
  } catch {
    return fallbackMessage;
  }
}

export async function loginUser(
  email: string,
  password: string,
  rememberMe = false,
): Promise<LoginResponse> {
  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      email,
      password,
      remember_me: rememberMe,
    }),
  });

  if (!response.ok) {
    throw new Error("Invalid email or password.");
  }

  return response.json();
}
export async function getCurrentUser(
  accessToken: string,
): Promise<AuthUser> {
  const response = await fetch(`${API_BASE_URL}/auth/me`, {
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  });

  if (!response.ok) {
    throw new Error("Unable to load current user.");
  }

  return response.json();
}

export async function requestPasswordReset(
  email: string,
): Promise<MessageResponse> {
  const response = await fetch(
    `${API_BASE_URL}/auth/forgot-password`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email,
      }),
    },
  );

  if (!response.ok) {
    throw new Error(
      "Unable to send password recovery instructions.",
    );
  }

  return response.json();
}

export async function resetPassword(
  token: string,
  newPassword: string,
  confirmPassword: string,
): Promise<MessageResponse> {
  const response = await fetch(
    `${API_BASE_URL}/auth/reset-password`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        token,
        new_password: newPassword,
        confirm_password: confirmPassword,
      }),
    },
  );

  if (!response.ok) {
    throw new Error(
      await getAuthApiErrorMessage(
        response,
        "Unable to reset password.",
      ),
    );
  }

  return response.json();
}

export async function requestEmailChange(
  accessToken: string,
  newEmail: string,
): Promise<MessageResponse> {
  const response = await fetch(
    `${API_BASE_URL}/auth/change-email`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${accessToken}`,
      },
      body: JSON.stringify({
        new_email: newEmail,
      }),
    },
  );

  if (!response.ok) {
    throw new Error(
      await getAuthApiErrorMessage(
        response,
        "Unable to request email change.",
      ),
    );
  }

  return response.json();
}

export async function confirmEmailChange(
  token: string,
): Promise<MessageResponse> {
  const response = await fetch(
    `${API_BASE_URL}/auth/change-email/confirm`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        token,
      }),
    },
  );

  if (!response.ok) {
    throw new Error(
      await getAuthApiErrorMessage(
        response,
        "Unable to confirm email change.",
      ),
    );
  }

  return response.json();
}

export type RegisterResponse = {
  id: number;
  email: string;
  is_active: boolean;
};

export async function registerUser(
  email: string,
  password: string,
  confirmPassword: string,
): Promise<RegisterResponse> {
  const response = await fetch(
    `${API_BASE_URL}/auth/register`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email,
        password,
        confirm_password: confirmPassword,
      }),
    },
  );

  if (!response.ok) {
    throw new Error(
      await getAuthApiErrorMessage(
        response,
        "Unable to create account.",
      ),
    );
  }

  return response.json();
}