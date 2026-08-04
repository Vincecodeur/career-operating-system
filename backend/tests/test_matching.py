from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_matching_endpoint_not_found_for_unknown_profile():
    response = client.get("/matching/999999/1")

    assert response.status_code == 404