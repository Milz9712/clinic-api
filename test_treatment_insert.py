from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

import main


@pytest.mark.parametrize(
    ("row", "status_code", "expected"),
    [
        ((7, "cupping", 40), 200, {"id": 7, "name": "cupping", "price": 40}),
        (None, 500, {"detail": "Failed to create treatment"}),
    ],
)
def test_insert_result(monkeypatch, row, status_code, expected):
    connection = MagicMock()
    connection.__enter__.return_value = connection
    connection.execute.return_value.fetchone.return_value = row
    connect = MagicMock(return_value=connection)
    monkeypatch.setattr(main.psycopg, "connect", connect)

    response = TestClient(main.app).post(
        "/treatments", json={"name": "cupping", "price": 40}
    )

    assert response.status_code == status_code
    assert response.json() == expected
    connection.execute.assert_called_once_with(
        "INSERT INTO treatments (name, price) VALUES (%s, %s) RETURNING id, name, price",
        ("cupping", 40),
    )
    # A missing result raises inside the transaction so it is rolled back.
    assert connection.__exit__.call_args.args[0] == (
        main.HTTPException if row is None else None
    )
