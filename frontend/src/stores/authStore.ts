import { create } from "zustand";

import {
  type AuthUser,
  getCurrentUser,
  loginUser,
} from "../services/authApi";

type AuthStore = {
  accessToken: string | null;
  user: AuthUser | null;
  isAuthenticated: boolean;
  login: (
    email: string,
    password: string,
    rememberMe?: boolean,
  ) => Promise<void>;
  logout: () => void;
  loadCurrentUser: () => Promise<void>;
};

const ACCESS_TOKEN_STORAGE_KEY = "career_os_access_token";

function getStoredAccessToken(): string | null {
  return localStorage.getItem(
    ACCESS_TOKEN_STORAGE_KEY,
  );
}

export const useAuthStore = create<AuthStore>((set, get) => ({
  accessToken: getStoredAccessToken(),
  user: null,
  isAuthenticated: Boolean(
    getStoredAccessToken(),
  ),

  login: async (
    email: string,
    password: string,
    rememberMe = false,
  ) => {
    const response = await loginUser(
      email,
      password,
      rememberMe,
    );

    localStorage.setItem(
      ACCESS_TOKEN_STORAGE_KEY,
      response.access_token,
    );

    set({
      accessToken: response.access_token,
      user: response.user,
      isAuthenticated: true,
    });
  },

  logout: () => {
    localStorage.removeItem(
      ACCESS_TOKEN_STORAGE_KEY,
    );

    set({
      accessToken: null,
      user: null,
      isAuthenticated: false,
    });
  },

  loadCurrentUser: async () => {
    const token = get().accessToken;

    if (!token) {
      set({
        user: null,
        isAuthenticated: false,
      });

      return;
    }

    try {
      const user = await getCurrentUser(token);

      set({
        user,
        isAuthenticated: true,
      });
    } catch {
      localStorage.removeItem(
        ACCESS_TOKEN_STORAGE_KEY,
      );

      set({
        accessToken: null,
        user: null,
        isAuthenticated: false,
      });
    }
  },
}));
