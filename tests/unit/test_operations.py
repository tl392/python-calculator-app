import pytest
from app.operations import add, subtract, multiply, divide


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (0, 0, 0),
        (1, 2, 3),
        (5, 3, 8),
        (100, 200, 300),
        (-1, -2, -3),
        (-5, -3, -8),
        (-5, 3, -2),
        (5, -3, 2),
        (10, 0, 10),
        (0, 10, 10),
    ],
)
def test_add(a, b, expected):
    assert add(a, b) == expected


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (0, 0, 0),
        (5, 3, 2),
        (10, 4, 6),
        (100, 50, 50),
        (-5, -3, -2),
        (-10, -4, -6),
        (-5, 3, -8),
        (5, -3, 8),
        (10, 0, 10),
        (0, 10, -10),
    ],
)
def test_subtract(a, b, expected):
    assert subtract(a, b) == expected


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (0, 0, 0),
        (1, 2, 2),
        (5, 3, 15),
        (10, 10, 100),
        (-1, -2, 2),
        (-5, -3, 15),
        (-5, 3, -15),
        (5, -3, -15),
        (100, 0, 0),
        (0, 100, 0),
    ],
)
def test_multiply(a, b, expected):
    assert multiply(a, b) == expected


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (1, 1, 1),
        (20, 5, 4),
        (100, 10, 10),
        (-20, -5, 4),
        (-20, 5, -4),
        (20, -5, -4),
        (7, 2, 3.5),
        (9, 1, 9),
        (0, 5, 0),
        (5, 2, 2.5),
    ],
)
def test_divide(a, b, expected):
    assert divide(a, b) == expected


@pytest.mark.parametrize(
    "a,b",
    [
        (10, 0),
        (0, 0),
        (-5, 0),
        (100, 0),
    ],
)
def test_divide_by_zero(a, b):
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(a, b)