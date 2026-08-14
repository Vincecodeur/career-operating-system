from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_countries():
    response = client.get(
        "/reference-data/countries"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 10

    country_codes = {
        country["code"]
        for country in data
    }

    assert "FR" in country_codes
    assert "GB" in country_codes
    assert "US" in country_codes


def test_get_work_modes():
    response = client.get(
        "/reference-data/work-modes"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 3

    work_mode_codes = {
        work_mode["code"]
        for work_mode in data
    }

    assert "REMOTE" in work_mode_codes
    assert "HYBRID" in work_mode_codes
    assert "ONSITE" in work_mode_codes


def test_get_contract_types():
    response = client.get(
        "/reference-data/contract-types"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 6

    contract_type_codes = {
        contract_type["code"]
        for contract_type in data
    }

    assert "PERMANENT" in contract_type_codes
    assert "FIXED_TERM" in contract_type_codes
    assert "FREELANCE" in contract_type_codes
    assert "CONTRACTOR" in contract_type_codes
    assert "INTERNSHIP" in contract_type_codes
    assert "APPRENTICESHIP" in contract_type_codes


def test_countries_are_sorted():
    response = client.get(
        "/reference-data/countries"
    )

    assert response.status_code == 200

    data = response.json()

    names = [
        country["name"]
        for country in data
    ]

    assert names == sorted(names)


def test_work_modes_are_sorted():
    response = client.get(
        "/reference-data/work-modes"
    )

    assert response.status_code == 200

    data = response.json()

    names = [
        work_mode["name"]
        for work_mode in data
    ]

    assert names == sorted(names)


def test_contract_types_are_sorted():
    response = client.get(
        "/reference-data/contract-types"
    )

    assert response.status_code == 200

    data = response.json()

    names = [
        contract_type["name"]
        for contract_type in data
    ]

    assert names == sorted(names)