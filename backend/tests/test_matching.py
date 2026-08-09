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
    assert "skills_score" in item
    assert "experience_score" in item
    assert "work_mode_score" in item
    assert "location_score" in item
    assert "matching_skills" in item
    assert "missing_skills" in item


def test_matching_endpoint_returns_v2_fields():
    ranking_response = client.get(
        "/profiles/1/ranked-job-offers"
    )

    assert ranking_response.status_code == 200

    ranked_job_offers = ranking_response.json()

    if len(ranked_job_offers) == 0:
        return

    job_offer_id = ranked_job_offers[0]["job_offer_id"]

    response = client.get(
        f"/matching/1/{job_offer_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert "profile_id" in data
    assert "job_offer_id" in data
    assert "matching_score" in data
    assert "skills_score" in data
    assert "experience_score" in data
    assert "work_mode_score" in data
    assert "location_score" in data
    assert "matching_skills" in data
    assert "missing_skills" in data
    assert "strengths" in data
    assert "weaknesses" in data


def test_matching_v2_scores_are_numeric():
    ranking_response = client.get(
        "/profiles/1/ranked-job-offers"
    )

    assert ranking_response.status_code == 200

    ranked_job_offers = ranking_response.json()

    if len(ranked_job_offers) == 0:
        return

    job_offer_id = ranked_job_offers[0]["job_offer_id"]

    response = client.get(
        f"/matching/1/{job_offer_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(
        data["matching_score"],
        int | float
    )
    assert isinstance(
        data["skills_score"],
        int | float
    )
    assert isinstance(
        data["experience_score"],
        int | float
    )
    assert isinstance(
        data["work_mode_score"],
        int | float
    )
    assert isinstance(
        data["location_score"],
        int | float
    )


def test_matching_v2_scores_are_between_zero_and_one_hundred():
    ranking_response = client.get(
        "/profiles/1/ranked-job-offers"
    )

    assert ranking_response.status_code == 200

    ranked_job_offers = ranking_response.json()

    if len(ranked_job_offers) == 0:
        return

    job_offer_id = ranked_job_offers[0]["job_offer_id"]

    response = client.get(
        f"/matching/1/{job_offer_id}"
    )

    assert response.status_code == 200

    data = response.json()

    score_fields = [
        "matching_score",
        "skills_score",
        "experience_score",
        "work_mode_score",
        "location_score",
    ]

    for field in score_fields:
        assert data[field] >= 0
        assert data[field] <= 100


def test_matching_v2_strengths_and_weaknesses_are_lists():
    ranking_response = client.get(
        "/profiles/1/ranked-job-offers"
    )

    assert ranking_response.status_code == 200

    ranked_job_offers = ranking_response.json()

    if len(ranked_job_offers) == 0:
        return

    job_offer_id = ranked_job_offers[0]["job_offer_id"]

    response = client.get(
        f"/matching/1/{job_offer_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(
        data["strengths"],
        list
    )
    assert isinstance(
        data["weaknesses"],
        list
    )


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