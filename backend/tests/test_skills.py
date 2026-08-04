from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_skills():
    response = client.get("/skills")

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list
    )