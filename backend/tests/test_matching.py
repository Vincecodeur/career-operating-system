from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_matching_endpoint_not_found_for_unknown_profile(authenticated_headers):
    response = client.get(
        "/matching/999999/1",
        headers=authenticated_headers,
    )

    assert response.status_code == 404


def test_ranking_endpoint_not_found_for_unknown_profile(authenticated_headers):
    response = client.get(
        "/profiles/999999/ranked-job-offers",
        headers=authenticated_headers,
    )

    assert response.status_code == 404


def test_ranking_endpoint_returns_list(authenticated_headers):
    response = client.get(
        "/profiles/1/ranked-job-offers",
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


def test_ranking_items_have_required_fields(authenticated_headers):
    response = client.get(
        "/profiles/1/ranked-job-offers",
        headers=authenticated_headers,
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


def test_matching_endpoint_returns_v2_fields(authenticated_headers):
    ranking_response = client.get(
        "/profiles/1/ranked-job-offers",
        headers=authenticated_headers,
    )

    assert ranking_response.status_code == 200

    ranked_job_offers = ranking_response.json()

    if len(ranked_job_offers) == 0:
        return

    job_offer_id = ranked_job_offers[0]["job_offer_id"]

    response = client.get(
        f"/matching/1/{job_offer_id}",
        headers=authenticated_headers,
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


def test_matching_v2_scores_are_numeric(authenticated_headers):
    ranking_response = client.get(
        "/profiles/1/ranked-job-offers",
        headers=authenticated_headers,
    )

    assert ranking_response.status_code == 200

    ranked_job_offers = ranking_response.json()

    if len(ranked_job_offers) == 0:
        return

    job_offer_id = ranked_job_offers[0]["job_offer_id"]

    response = client.get(
        f"/matching/1/{job_offer_id}",
        headers=authenticated_headers,
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


def test_matching_v2_scores_are_between_zero_and_one_hundred(authenticated_headers):
    ranking_response = client.get(
        "/profiles/1/ranked-job-offers",
        headers=authenticated_headers,
    )

    assert ranking_response.status_code == 200

    ranked_job_offers = ranking_response.json()

    if len(ranked_job_offers) == 0:
        return

    job_offer_id = ranked_job_offers[0]["job_offer_id"]

    response = client.get(
        f"/matching/1/{job_offer_id}",
        headers=authenticated_headers,
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


def test_matching_v2_strengths_and_weaknesses_are_lists(authenticated_headers):
    ranking_response = client.get(
        "/profiles/1/ranked-job-offers",
        headers=authenticated_headers,
    )

    assert ranking_response.status_code == 200

    ranked_job_offers = ranking_response.json()

    if len(ranked_job_offers) == 0:
        return

    job_offer_id = ranked_job_offers[0]["job_offer_id"]

    response = client.get(
        f"/matching/1/{job_offer_id}",
        headers=authenticated_headers,
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


def test_ranking_is_sorted_descending(authenticated_headers):
    response = client.get(
        "/profiles/1/ranked-job-offers",
        headers=authenticated_headers,
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

def test_matching_v2_explanations_are_present(authenticated_headers):
    ranking_response = client.get(
        "/profiles/1/ranked-job-offers",
        headers=authenticated_headers,
    )

    assert ranking_response.status_code == 200

    ranked_job_offers = ranking_response.json()

    if len(ranked_job_offers) == 0:
        return

    job_offer_id = ranked_job_offers[0]["job_offer_id"]

    response = client.get(
        f"/matching/1/{job_offer_id}",
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert "explanations" in data

    explanations = data["explanations"]

    assert isinstance(explanations, list)

    criteria = {
        item["criterion"]
        for item in explanations
    }

    assert "skills" in criteria
    assert "experience" in criteria
    assert "work_mode" in criteria
    assert "location" in criteria

    for item in explanations:
        assert "criterion" in item
        assert "score" in item
        assert "message" in item

def test_opportunity_analysis_is_present(authenticated_headers):
    ranking_response = client.get(
        "/profiles/1/ranked-job-offers",
        headers=authenticated_headers,
    )

    assert ranking_response.status_code == 200

    ranked_job_offers = ranking_response.json()

    if len(ranked_job_offers) == 0:
        return

    job_offer_id = ranked_job_offers[0]["job_offer_id"]

    response = client.get(
        f"/matching/1/{job_offer_id}",
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert "opportunity_analysis" in data

    analysis = data["opportunity_analysis"]

    assert "verdict" in analysis
    assert "recommendation" in analysis
    assert "summary" in analysis

def test_profile_scores_endpoint_not_found_for_unknown_job_offer(authenticated_headers):
    response = client.get(
        "/matching/job-offers/999999/profiles",
        headers=authenticated_headers,
    )

    assert response.status_code == 404


def test_profile_scores_endpoint_returns_list(authenticated_headers):
    response = client.get(
        "/matching/job-offers/1/profiles",
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

def test_profile_scores_items_have_required_fields(authenticated_headers):
    response = client.get(
        "/matching/job-offers/1/profiles",
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    data = response.json()

    if len(data) == 0:
        return

    item = data[0]

    assert "profile_id" in item
    assert "profile_name" in item
    assert "matching_score" in item
    assert "skills_score" in item
    assert "experience_score" in item
    assert "work_mode_score" in item
    assert "location_score" in item
    assert "is_best_match" in item


def test_profile_scores_only_one_best_match(authenticated_headers):
    response = client.get(
        "/matching/job-offers/1/profiles",
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    data = response.json()

    best_match_count = sum(
        1
        for item in data
        if item["is_best_match"]
    )

    assert best_match_count <= 1


def test_profile_scores_sorted_descending(authenticated_headers):
    response = client.get(
        "/matching/job-offers/1/profiles",
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    data = response.json()

    scores = [
        item["matching_score"]
        for item in data
    ]

    assert scores == sorted(
        scores,
        reverse=True,
    )
