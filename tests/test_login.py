import pytest
from playwright.sync_api import expect
from pages.login_page import LoginPage

"""
Тести, які перевіряють саме процес логіну на DemoQA.
"""


# Використовуємо реальні дані користувача DemoQA, створеного заздалегідь.
@pytest.mark.parametrize("username, password", [("Test_User", "Test_User123!")])
def test_login_success(page, username, password):
    """
    Перевіряємо, що користувач може успішно залогінитися
    і бачить свій профіль з правильною кнопкою Logout та ім'ям.
    """
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