import pytest
from playwright.sync_api import expect
from pages.login_page import LoginPage
from pages.profile_page import ProfilePage

"""
Окремі тести для перевірки логауту (виходу з акаунта) на DemoQA.
"""


@pytest.mark.parametrize("username, password", [("Test_User", "Test_User123!")])
def test_logout_success(page, username, password):
    """
    Перевіряємо повний сценарій: логін + логаут "з нуля".
    Після виходу користувач має знову опинитися на сторінці логіну.
    """
    login_page = LoginPage(page)

    # 1. Заходимо на сторінку логіну
    login_page.goto()

    # 2. Логінимося
    login_page.login(username, password)

    # 3. Переходимо на ProfilePage і перевіряємо, що ми залогінені
    profile = ProfilePage(page)
    profile.expect_logout_visible()

    # 4. Тиснемо Logout через Page Object
    profile.logout()

    # 5. Перевіряємо, що нас повернуло на сторінку логіну
    expect(page).to_have_url("https://demoqa.com/login")

