from playwright.sync_api import Page

"""
Page Object (об'єкт сторінки) для сторінки логіну DemoQA.

Містить:
- локатори для полів логіну та пароля, а також кнопки логіну;
- метод goto() для переходу на сторінку логіну;
- метод login(), який виконує сам процес логіну.
"""


class LoginPage:
    def __init__(self, page: Page) -> None:
        """
        Приймаємо об'єкт Playwright Page і створюємо зручні
        змінні-локатори для елементів форми логіну.
        """
        self.page = page

        # Поле введення логіну (Username)
        self.username_input = page.locator("#userName")

        # Поле введення пароля (Password)
        self.password_input = page.locator("#password")

        # Кнопка "Login" для надсилання форми
        self.login_button = page.locator("#login")

    def goto(self) -> None:
        """
        Відкриває сторінку логіну DemoQA.
        """
        self.page.goto("https://demoqa.com/login")

    def login(self, username: str, password: str) -> None:
        """
        Заповнює форму логіну валідними даними і натискає кнопку входу.
        Чекає на редирект на сторінку профілю.
        """
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
        self.page.wait_for_url("https://demoqa.com/profile")