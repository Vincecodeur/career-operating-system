import { createBrowserRouter, Navigate } from "react-router-dom";

import { AppLayout } from "../layouts/AppLayout";
import { AccountPage } from "../pages/AccountPage";
import { DashboardPage } from "../pages/DashboardPage";
import { ForgotPasswordPage } from "../pages/ForgotPasswordPage";
import { LoginPage } from "../pages/LoginPage";
import { ResetPasswordPage } from "../pages/ResetPasswordPage";
import { ConfirmEmailChangePage } from "../pages/ConfirmEmailChangePage";
import { SignUpPage } from "../pages/SignUpPage";
import { ProtectedRoute } from "./ProtectedRoute";
import { ApplicationsPage } from "../pages/ApplicationsPage";
import { OpportunitiesPage } from "../pages/OpportunitiesPage";
import { ProfilesPage } from "../pages/ProfilesPage";
import { SettingsPage } from "../pages/SettingsPage";

export const router = createBrowserRouter([
  {
    path: "/login",
    element: <LoginPage />,
  },
  {
    path: "/signup",
    element: <SignUpPage />,
  },
  {
    path: "/forgot-password",
    element: <ForgotPasswordPage />,
  },
  {
    path: "/reset-password",
    element: <ResetPasswordPage />,
  },
  {
    path: "/confirm-email-change",
    element: <ConfirmEmailChangePage />,
  },
  {
    element: (
      <ProtectedRoute>
        <AppLayout />
      </ProtectedRoute>
    ),
    children: [
      {
        path: "/",
        element: <Navigate to="/dashboard" replace />,
      },
      {
        path: "/dashboard",
        element: <DashboardPage />,
      },
      {
        path: "/account",
        element: <AccountPage />,
      },
      {
        path: "/applications",
        element: <ApplicationsPage />,
      },
      {
        path: "/opportunities",
        element: <OpportunitiesPage />,
      },
      {
        path: "/profiles",
        element: <ProfilesPage />,
      },
      {
        path: "/settings",
        element: <SettingsPage />,
      },
    ],
  },
  {
    path: "*",
    element: <Navigate to="/dashboard" replace />,
  },
]);
