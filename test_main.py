from fastapi.testclient import TestClient

TestClient
from main import app

client = TestClient(app)


def test_list_treatments():
    response = client.get("/treatments")
    assert response.status_code == 200


def test_treatment_not_found():
    response = client.get("/treatments/99")
    assert response.status_code == 404


def test_invalid_id():
    response = client.get("/treatments/abc")
    assert response.status_code == 422
