import os
from pathlib import Path

import pytest
from playwright.sync_api import expect
from api.bookstore_client import BookStoreAPI
from pages.login_page import LoginPage

"""
Тести, які перевіряють саме процес логіну на DemoQA.
"""


def load_env_file(env_path: Path | str = ".env") -> None:
    env_path = Path(env_path)
    if not env_path.is_file():
        return

    with env_path.open(encoding="utf-8") as env_file:
        for raw_line in env_file:
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value


@pytest.fixture(scope="session")
def demoqa_credentials():
    workspace_root = Path(__file__).resolve().parents[1]
    load_env_file(workspace_root / ".env")

    username = os.getenv("API_USERNAME")
    password = os.getenv("API_PASSWORD")
    if not username or not password:
        pytest.fail("Креденшали не знайдені в змінних оточення або в .env")
    return username, password


@pytest.fixture(scope="session")
def auth_api(demoqa_credentials):
    from playwright.sync_api import sync_playwright
    p_cm = sync_playwright()
    p = p_cm.__enter__()
    request_context = p.request.new_context()
    client = BookStoreAPI(request_context)
    username, password = demoqa_credentials
    client.username = username
    client.password = password
    yield client
    request_context.dispose()
    p_cm.__exit__(None, None, None)

def test_generate_token_success(auth_api, demoqa_credentials):
    username, password = demoqa_credentials

    token = auth_api.generate_token()
    assert token is not None
    assert len(token) > 10


def test_login_success(page, demoqa_credentials):
    """
    Перевіряємо, що користувач може успішно залогінитися
    і бачить свій профіль з правильною кнопкою Logout та ім'ям.
    """
    username, password = demoqa_credentials

    # Створюємо об'єкт сторінки логіну (Page Object)
    login_page = LoginPage(page)

    # 1. Переходимо на сторінку логіну DemoQA
    login_page.goto()

    # 2. Виконуємо логін із переданими у параметрах логіном та паролем
    login_page.login(username, password)

    # 3. Перевіряємо, що на сторінці з'явилася кнопка Logout
    #    (id="submit" + текст "Logout") – це ознака успішної авторизації.
    logout_button = page.locator("#submit", has_text="Logout")
    expect(logout_button).to_be_visible(timeout=10000)

    # 4. Додаткова перевірка: елемент з id="userName-value"
    #    має містити логін користувача, з яким ми заходили.
    user_label = page.locator("#userName-value")
    expect(user_label).to_have_text(username)