from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_saved_searches():
    response = client.get(
        "/settings/saved-searches"
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list,
    )


def test_create_saved_search():
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
    )

    assert response.status_code == 200

    data = response.json()

    assert (
        data["name"]
        == "Test Search"
    )


def test_delete_saved_search():
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
    )

    saved_search_id = (
        create_response.json()["id"]
    )

    delete_response = client.delete(
        f"/settings/saved-searches/{saved_search_id}"
    )

    assert (
        delete_response.status_code
        == 200
    )