from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_skill():
    skill_name = f"Docker_{uuid4()}"

    response = client.post(
        "/skills",
        json={
            "name": skill_name,
            "category": "DevOps",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == skill_name
    assert data["category"] == "DevOps"
    assert "id" in data


def test_get_skills():
    response = client.get("/skills")

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list,
    )


def test_get_skill():
    skill_name = f"Kubernetes_{uuid4()}"

    create_response = client.post(
        "/skills",
        json={
            "name": skill_name,
            "category": "DevOps",
        },
    )

    assert create_response.status_code == 200

    skill_id = create_response.json()["id"]

    response = client.get(
        f"/skills/{skill_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == skill_id
    assert data["name"] == skill_name
    assert data["category"] == "DevOps"


def test_skill_not_found():
    response = client.get(
        "/skills/999999"
    )

    assert response.status_code == 404


def test_duplicate_skill_name():
    skill_name = f"Terraform_{uuid4()}"

    first_response = client.post(
        "/skills",
        json={
            "name": skill_name,
            "category": "DevOps",
        },
    )

    assert first_response.status_code == 200

    response = client.post(
        "/skills",
        json={
            "name": skill_name,
            "category": "Infrastructure",
        },
    )

    assert response.status_code == 409


def test_update_skill():
    original_name = f"FastApi_{uuid4()}"
    updated_name = f"FastAPI_{uuid4()}"

    create_response = client.post(
        "/skills",
        json={
            "name": original_name,
            "category": "Backend",
        },
    )

    assert create_response.status_code == 200

    skill_id = create_response.json()["id"]

    response = client.put(
        f"/skills/{skill_id}",
        json={
            "name": updated_name,
            "category": "Backend Development",
        },
    )


    assert response.status_code == 200

    data = response.json()

    assert data["id"] == skill_id
    assert data["name"] == updated_name
    assert data["category"] == "Backend Development"


def test_update_skill_not_found():
    response = client.put(
        "/skills/999999",
        json={
            "name": f"UpdatedSkill_{uuid4()}",
            "category": "Updated Category",
        },
    )
    
    response = client.put(
    "/skills/999999",
    json={
        "name": f"UpdatedSkill_{uuid4()}",
        "category": "Updated Category",
    },
    )



    assert response.status_code == 404
    
