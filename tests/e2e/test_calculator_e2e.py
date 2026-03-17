import pytest

BASE_URL = "http://127.0.0.1:8000"


@pytest.mark.e2e
def test_page_load(page, server):
    page.goto(BASE_URL)
    assert page.locator("h2").inner_text() == "FastAPI Calculator"
    assert page.locator("#a").is_visible()
    assert page.locator("#b").is_visible()


@pytest.mark.e2e
def test_add(page, server):
    page.goto(BASE_URL)
    page.fill("#a", "5")
    page.fill("#b", "3")
    page.click('button[value="add"]')
    assert page.locator("#result").inner_text() == "Result: 8.0"


@pytest.mark.e2e
def test_subtract(page, server):
    page.goto(BASE_URL)
    page.fill("#a", "10")
    page.fill("#b", "4")
    page.click('button[value="subtract"]')
    assert page.locator("#result").inner_text() == "Result: 6.0"


@pytest.mark.e2e
def test_multiply(page, server):
    page.goto(BASE_URL)
    page.fill("#a", "6")
    page.fill("#b", "7")
    page.click('button[value="multiply"]')
    assert page.locator("#result").inner_text() == "Result: 42.0"


@pytest.mark.e2e
def test_divide(page, server):
    page.goto(BASE_URL)
    page.fill("#a", "20")
    page.fill("#b", "5")
    page.click('button[value="divide"]')
    assert page.locator("#result").inner_text() == "Result: 4.0"


@pytest.mark.e2e
def test_divide_by_zero(page, server):
    page.goto(BASE_URL)
    page.fill("#a", "10")
    page.fill("#b", "0")
    page.click('button[value="divide"]')
    assert "Cannot divide by zero" in page.locator("#error").inner_text()


@pytest.mark.e2e
def test_swagger_link(page, server):
    page.goto(BASE_URL)
    assert page.locator('a[href="/docs"]').is_visible()