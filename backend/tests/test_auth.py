from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_register_is_disabled():
    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "Password123!",
        },
    )

    assert response.status_code == 403

    data = response.json()

    assert (
        data["detail"]
        == "Public registration is disabled."
    )


def test_login_with_unknown_user():
    response = client.post(
        "/auth/login",
        json={
            "email": "unknown@example.com",
            "password": "Password123!",
        },
    )

    assert response.status_code == 401

    data = response.json()

    assert (
        data["detail"]
        == "Invalid email or password."
    )


def test_me_without_token():
    response = client.get(
        "/auth/me",
    )

    assert response.status_code == 401