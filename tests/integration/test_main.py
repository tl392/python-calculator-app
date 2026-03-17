import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.parametrize(
    "endpoint,a,b,expected",
    [
        ("/add", 5, 3, 8),
        ("/add", -5, 3, -2),
        ("/subtract", 10, 4, 6),
        ("/subtract", 5, 10, -5),
        ("/multiply", 6, 7, 42),
        ("/multiply", -6, 7, -42),
        ("/divide", 20, 5, 4),
        ("/divide", 7, 2, 3.5),
    ],
)
def test_calculator_endpoints(endpoint, a, b, expected):
    response = client.get(endpoint, params={"a": a, "b": b})

    assert response.status_code == 200
    assert response.json()["result"] == expected


@pytest.mark.parametrize(
    "a,b",
    [
        (10, 0),
        (0, 0),
        (-5, 0),
    ],
)
def test_divide_by_zero(a, b):
    response = client.get("/divide", params={"a": a, "b": b})

    assert response.status_code == 400
    assert response.json()["detail"] == "Cannot divide by zero"


@pytest.mark.parametrize(
    "a,b,operation,expected",
    [
        (5, 3, "add", "Result: 8.0"),
        (10, 4, "subtract", "Result: 6.0"),
        (6, 7, "multiply", "Result: 42.0"),
        (20, 5, "divide", "Result: 4.0"),
    ],
)
def test_calculate_form(a, b, operation, expected):
    response = client.post(
        "/calculate",
        data={
            "a": a,
            "b": b,
            "operation": operation,
        },
    )

    assert response.status_code == 200
    assert expected in response.text


def test_calculate_divide_by_zero_form():
    response = client.post(
        "/calculate",
        data={
            "a": 10,
            "b": 0,
            "operation": "divide",
        },
    )

    assert response.status_code == 400
    assert "Cannot divide by zero" in response.text