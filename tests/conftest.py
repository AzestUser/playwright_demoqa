from datetime import datetime
from pathlib import Path
import pytest

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
