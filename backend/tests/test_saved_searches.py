from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_get_saved_searches(authenticated_headers):
    response = client.get(
        "/settings/saved-searches",
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list,
    )


def test_create_saved_search(authenticated_headers):
    response = client.post(
        "/settings/saved-searches",
        json={
            "name": "Test Search",
            "keyword": "python",
            "application_status": "ALL",
            "source": "ALL",
            "location": "ALL",
            "sort_by": "BEST_MATCH_FIRST",
        },
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert (
        data["name"]
        == "Test Search"
    )


def test_delete_saved_search(authenticated_headers):
    create_response = client.post(
        "/settings/saved-searches",
        json={
            "name": "Delete Search",
            "keyword": "",
            "application_status": "ALL",
            "source": "ALL",
            "location": "ALL",
            "sort_by": "BEST_MATCH_FIRST",
        },
        headers=authenticated_headers,
    )

    saved_search_id = (
        create_response.json()["id"]
    )

    delete_response = client.delete(
        f"/settings/saved-searches/{saved_search_id}",
        headers=authenticated_headers,
    )

    assert (
        delete_response.status_code
        == 200
    )


def test_delete_saved_search_not_found(authenticated_headers):
    response = client.delete(
        "/settings/saved-searches/999999",
        headers=authenticated_headers,
    )

    assert response.status_code == 404


def test_saved_search_is_isolated_between_users(
    authenticated_headers,
):
    from app.auth.models import User
    from app.auth.service import hash_password
    from app.core.database import SessionLocal
    from uuid import uuid4

    create_response = client.post(
        "/settings/saved-searches",
        json={
            "name": "Isolation Test Search",
            "keyword": "python",
            "application_status": "ALL",
            "source": "ALL",
            "location": "ALL",
            "sort_by": "BEST_MATCH_FIRST",
        },
        headers=authenticated_headers,
    )

    assert create_response.status_code == 200

    saved_search_id = create_response.json()["id"]

    email = f"isolation-saved-search-{uuid4()}@career-os.local"
    password = "IsolationTestPassword123!"

    db = SessionLocal()

    try:
        second_user = User(
            email=email,
            hashed_password=hash_password(password),
            is_active=True,
        )

        db.add(second_user)
        db.commit()
    finally:
        db.close()

    login_response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    assert login_response.status_code == 200

    access_token = login_response.json()["access_token"]

    other_headers = {
        "Authorization": f"Bearer {access_token}",
    }

    list_response = client.get(
        "/settings/saved-searches",
        headers=other_headers,
    )

    assert list_response.status_code == 200

    other_user_search_ids = [
        item["id"] for item in list_response.json()
    ]

    assert saved_search_id not in other_user_search_ids

    delete_response = client.delete(
        f"/settings/saved-searches/{saved_search_id}",
        headers=other_headers,
    )

    assert delete_response.status_code == 404
