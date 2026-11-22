from fastapi.testclient import TestClient

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


def test_create_treatment():
    response = client.post("/treatments", json={"name": "cupping", "price": 40})
    assert response.status_code == 200
    assert response.json()["name"] == "cupping"
    new_id = response.json()["id"]
    client.delete(f"/treatments/{new_id}")


def test_create_missing_price():
    response = client.post("/treatments", json={"name": "cupping"})
    assert response.status_code == 422


def test_delete_treatments():
    created = client.post("/treatments", json={"name": "test delete", "price": 1})
    new_id = created.json()["id"]

    response = client.delete(f"/treatments/{new_id}")
    assert response.status_code == 200

    response = client.delete(f"/treatments/{new_id}")
    assert response.status_code == 404


def test_missing_treatment_logs_warning(caplog):
    client.get("/treatments/99")
    assert "Treatment not found: 99" in caplog.text


def test_create_and_delete_bookings():
    t = client.post("/treatments", json={"name": "test booking treatment", "price": 1})
    treatment_id = t.json()["id"]

    b = client.post(
        "/bookings",
        json={
            "client_name": "Test",
            "client_phone": "07000000000",
            "treatment_id": treatment_id,
            "starts_at": "2026-12-01T10:00:00Z",
        },
    )
    assert b.status_code == 200
    booking_id = b.json()["id"]

    assert client.delete(f"/bookings/{booking_id}").status_code == 200
    assert client.delete(f"/treatments/{treatment_id}").status_code == 200


def test_booking_unknown_treatment():
    response = client.post(
        "/bookings",
        json={
            "client_name": "Test",
            "client_phone": "07000000000",
            "treatment_id": 999999,
            "starts_at": "2026-12-01T10:00:00Z",
        },
    )
    assert response.status_code == 404


def test_booking_bad_date():
    response = client.post(
        "/bookings",
        json={
            "client_name": "Test",
            "client_phone": "07000000000",
            "treatment_id": 1,
            "starts_at": "next tuesday",
        },
    )
    assert response.status_code == 422


def test_list_bookings():
    response = client.get("/bookings")
    assert response.status_code == 200


def test_double_booking_returns_409():
    t = client.post("/treatments", json={"name": "test double booking", "price": 1})
    treatment_id = t.json()["id"]
    slot = {"client_name": "Test", "client_phone": "07000000000", "treatment_id": treatment_id, "starts_at": "2030-01-01T09:00:00Z"}

    first = client.post("/bookings", json=slot)
    assert first.status_code == 200

    second = client.post("/bookings", json=slot)
    assert second.status_code == 409 

    client.delete(f"/bookings/{first.json()['id']}")
    client.delete(f"/treatments/{treatment_id}")
     