from datetime import datetime
from pathlib import Path
import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session", autouse=True)
def setup_reports_dir():
    """Створює папку для звітів, якщо її немає."""
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    yield


def pytest_configure(config):
    """Додає дату/час до імені HTML звіту."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_file = f"reports/report_{timestamp}.html"
    config.option.htmlpath = report_file


@pytest.fixture(scope="session")
def browser():
    """Запускає браузер з Playwright."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture
def page(browser):
    """Створює нову сторінку для кожного тесту."""
    context = browser.new_context()
    page = context.new_page()
    yield page
    page.close()
    context.close()