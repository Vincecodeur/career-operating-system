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

export async function loginUser(
  email: string,
  password: string,
): Promise<LoginResponse> {
  const response = await fetch(
    `${API_BASE_URL}/auth/login`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email,
        password,
      }),
    },
  );

  if (!response.ok) {
    throw new Error(
      "Invalid email or password.",
    );
  }

  return response.json();
}

export async function getCurrentUser(
  accessToken: string,
): Promise<AuthUser> {
  const response = await fetch(
    `${API_BASE_URL}/auth/me`,
    {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    },
  );

  if (!response.ok) {
    throw new Error(
      "Unable to load current user.",
    );
  }

  return response.json();
}

export type MessageResponse = {
  message: string;
};

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
      "Unable to send password recovery email.",
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
    const data = await response.json();

    throw new Error(
      data.detail ??
      "Unable to reset password.",
    );
  }

  return response.json();
}