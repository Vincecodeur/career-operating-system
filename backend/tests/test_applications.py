from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)

APPLICATION_TEST_PROFILE_PAYLOAD = {
    "profile_name": "Inactive Application Test Profile",
    "full_name": "Application Test User",
    "current_title": "Technical Partnerships Manager",
    "location": "France",
    "years_of_experience": 10,
    "target_role_short_term": "Solution Architect",
    "target_role_long_term": "Enterprise Architect",
    "remote_preference": "Hybrid",
    "preferred_countries": "France,UK",
}


def create_application_test_profile(authenticated_headers):
    response = client.post(
        "/profiles",
        json=APPLICATION_TEST_PROFILE_PAYLOAD,
        headers=authenticated_headers,
    )

    assert response.status_code == 200

    return response.json()


def archive_application_test_profile(
    profile_id: int,
    authenticated_headers,
):
    response = client.delete(
        f"/profiles/{profile_id}",
        headers=authenticated_headers,
    )

    assert response.status_code == 200
    assert response.json()["is_active"] is False

    return response.json()

def test_list_applications():
    response = client.get(
        "/applications"
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list
    )


def test_get_application_not_found():
    response = client.get(
        "/applications/999999"
    )

    assert response.status_code == 404


def test_create_application():
    response = client.post(
        "/applications",
        json={
            "profile_id": 1,
            "job_offer_id": 1,
            "status": "Applied"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["profile_id"] == 1
    assert data["job_offer_id"] == 1
    assert data["status"] == "Applied"


def test_get_application():
    create_response = client.post(
        "/applications",
        json={
            "profile_id": 1,
            "job_offer_id": 1,
            "status": "Interview"
        }
    )

    application_id = create_response.json()["id"]

    response = client.get(
        f"/applications/{application_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == application_id
    assert data["status"] == "Interview"
    

def test_update_application():
    create_response = client.post(
        "/applications",
        json={
            "profile_id": 1,
            "job_offer_id": 1,
            "status": "Applied"
        }
    )

    application_id = create_response.json()["id"]

    response = client.put(
        f"/applications/{application_id}",
        json={
            "profile_id": 1,
            "status": "Interview",
            "notes": "Entretien RH réalisé",
            "source_type": "REFERRAL",
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "Interview"
    assert data["notes"] == "Entretien RH réalisé"
    assert data["source_type"] == "REFERRAL"


def test_transition_application_status():
    create_response = client.post(
        "/applications",
        json={
            "profile_id": 1,
            "job_offer_id": 1,
            "status": "Applied"
        }
    )

    application_id = create_response.json()["id"]

    response = client.post(
        f"/applications/{application_id}/status",
        json={
            "status": "Phone Screen"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "Phone Screen"


def test_invalid_status_transition():
    create_response = client.post(
        "/applications",
        json={
            "profile_id": 1,
            "job_offer_id": 1,
            "status": "Interview"
        }
    )

    application_id = create_response.json()["id"]

    response = client.post(
        f"/applications/{application_id}/status",
        json={
            "status": "Applied"
        }
    )

    assert response.status_code == 400

    assert response.json()["detail"] == (
        "Invalid status transition."
    )


def test_transition_application_not_found():
    response = client.post(
        "/applications/999999/status",
        json={
            "status": "Phone Screen"
        }
    )

    assert response.status_code == 404


def test_get_application_timeline():
    create_response = client.post(
        "/applications",
        json={
            "profile_id": 1,
            "job_offer_id": 1,
            "status": "Interview"
        }
    )

    application_id = create_response.json()["id"]

    transition_response = client.post(
        f"/applications/{application_id}/status",
        json={
            "status": "Offer"
        }
    )

    assert transition_response.status_code == 200

    response = client.get(
        f"/applications/{application_id}/timeline"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) >= 1

    assert data[0]["event_type"] == "STATUS_CHANGED"
    assert data[0]["old_value"] == "Interview"
    assert data[0]["new_value"] == "Offer"


def test_timeline_application_not_found():
    response = client.get(
        "/applications/999999/timeline"
    )

    assert response.status_code == 404
    
    
def test_create_application_rejects_unknown_profile():
    response = client.post(
        "/applications",
        json={
            "profile_id": 999999,
            "job_offer_id": 1,
            "status": "Applied",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == (
        "Profile not found."
    )


def test_create_application_rejects_unknown_job_offer():
    response = client.post(
        "/applications",
        json={
            "profile_id": 1,
            "job_offer_id": 999999,
            "status": "Applied",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == (
        "Job offer not found."
    )


def test_update_application_changes_profile():
    create_response = client.post(
        "/applications",
        json={
            "profile_id": 1,
            "job_offer_id": 1,
            "status": "Applied",
        },
    )

    assert create_response.status_code == 200

    application_id = create_response.json()["id"]

    response = client.put(
        f"/applications/{application_id}",
        json={
            "profile_id": 2,
            "status": "Applied",
            "notes": None,
            "source_type": "OPPORTUNITY",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["profile_id"] == 2
    assert data["job_offer_id"] == 1
    assert data["status"] == "Applied"
    assert data["source_type"] == "OPPORTUNITY"


def test_update_application_creates_profile_changed_event():
    create_response = client.post(
        "/applications",
        json={
            "profile_id": 1,
            "job_offer_id": 1,
            "status": "Applied",
        },
    )

    assert create_response.status_code == 200

    application_id = create_response.json()["id"]

    update_response = client.put(
        f"/applications/{application_id}",
        json={
            "profile_id": 2,
            "status": "Applied",
            "notes": None,
            "source_type": "OPPORTUNITY",
        },
    )

    assert update_response.status_code == 200

    timeline_response = client.get(
        f"/applications/{application_id}/timeline"
    )

    assert timeline_response.status_code == 200

    events = timeline_response.json()

    profile_events = [
        event
        for event in events
        if event["event_type"] == "PROFILE_CHANGED"
    ]

    assert len(profile_events) == 1
    assert profile_events[0]["old_value"] == "1"
    assert profile_events[0]["new_value"] == "2"


def test_update_application_does_not_create_profile_event_when_unchanged():
    create_response = client.post(
        "/applications",
        json={
            "profile_id": 1,
            "job_offer_id": 1,
            "status": "Applied",
        },
    )

    assert create_response.status_code == 200

    application_id = create_response.json()["id"]

    update_response = client.put(
        f"/applications/{application_id}",
        json={
            "profile_id": 1,
            "status": "Applied",
            "notes": "No profile change.",
            "source_type": "MANUAL",
        },
    )

    assert update_response.status_code == 200

    timeline_response = client.get(
        f"/applications/{application_id}/timeline"
    )

    assert timeline_response.status_code == 200

    profile_events = [
        event
        for event in timeline_response.json()
        if event["event_type"] == "PROFILE_CHANGED"
    ]

    assert profile_events == []


def test_update_application_rejects_unknown_profile():
    create_response = client.post(
        "/applications",
        json={
            "profile_id": 1,
            "job_offer_id": 1,
            "status": "Applied",
        },
    )

    assert create_response.status_code == 200

    application_id = create_response.json()["id"]

    response = client.put(
        f"/applications/{application_id}",
        json={
            "profile_id": 999999,
            "status": "Applied",
            "notes": None,
            "source_type": "MANUAL",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == (
        "Profile not found."
    )

    get_response = client.get(
        f"/applications/{application_id}"
    )

    assert get_response.status_code == 200
    assert get_response.json()["profile_id"] == 1
    
    
    
def test_create_application_rejects_inactive_profile(authenticated_headers):
    profile = create_application_test_profile(authenticated_headers)

    archived_profile = archive_application_test_profile(
        profile["id"],
        authenticated_headers,
    )

    response = client.post(
        "/applications",
        json={
            "profile_id": archived_profile["id"],
            "job_offer_id": 1,
            "status": "Applied",
            "notes": None,
            "source_type": "OPPORTUNITY",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "The selected profile is not available."
    )
    
def test_update_application_rejects_inactive_profile(authenticated_headers):
    inactive_profile = create_application_test_profile(authenticated_headers)

    archived_profile = archive_application_test_profile(
        inactive_profile["id"],
        authenticated_headers,
    )

    create_response = client.post(
        "/applications",
        json={
            "profile_id": 1,
            "job_offer_id": 1,
            "status": "Applied",
            "notes": None,
            "source_type": "OPPORTUNITY",
        },
    )

    assert create_response.status_code == 200

    application_id = create_response.json()["id"]
    original_profile_id = create_response.json()["profile_id"]

    update_response = client.put(
        f"/applications/{application_id}",
        json={
            "profile_id": archived_profile["id"],
            "status": "Applied",
            "notes": None,
            "source_type": "OPPORTUNITY",
        },
    )

    assert update_response.status_code == 400
    assert update_response.json()["detail"] == (
        "The selected profile is not available."
    )

    get_response = client.get(
        f"/applications/{application_id}"
    )

    assert get_response.status_code == 200
    assert get_response.json()["profile_id"] == original_profile_id

    timeline_response = client.get(
        f"/applications/{application_id}/timeline"
    )

    assert timeline_response.status_code == 200

    profile_events = [
        event
        for event in timeline_response.json()
        if event["event_type"] == "PROFILE_CHANGED"
    ]

    assert profile_events == []