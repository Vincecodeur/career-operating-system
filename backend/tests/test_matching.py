from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_matching_endpoint_not_found_for_unknown_profile():
    response = client.get(
        "/matching/999999/1"
    )

    assert response.status_code == 404


def test_ranking_endpoint_not_found_for_unknown_profile():
    response = client.get(
        "/profiles/999999/ranked-job-offers"
    )

    assert response.status_code == 404


def test_ranking_endpoint_returns_list():
    response = client.get(
        "/profiles/1/ranked-job-offers"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


def test_ranking_items_have_required_fields():
    response = client.get(
        "/profiles/1/ranked-job-offers"
    )

    assert response.status_code == 200

    data = response.json()

    if len(data) == 0:
        return

    item = data[0]

    assert "job_offer_id" in item
    assert "title" in item
    assert "matching_score" in item
    assert "matching_skills" in item
    assert "missing_skills" in item


def test_ranking_is_sorted_descending():
    response = client.get(
        "/profiles/1/ranked-job-offers"
    )

    assert response.status_code == 200

    data = response.json()

    scores = [
        item["matching_score"]
        for item in data
    ]

    assert scores == sorted(
        scores,
        reverse=True
    )