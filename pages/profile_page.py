from playwright.sync_api import Page, expect

"""
Page Object для сторінки профілю DemoQA: https://demoqa.com/profile

Ця сторінка показує:
- ім'я залогіненого користувача;
- таблицю з книгами в колекції;
- кнопки Logout / Go To Book Store / Delete All Books тощо.
"""


class ProfilePage:
    def __init__(self, page: Page) -> None:
        """
        Приймаємо Playwright Page і ініціалізуємо локатори,
        які найчастіше використовуються в тестах.
        """
        self.page = page

        # Лейбл з логіном користувача (після логіну там буде, наприклад, Test_User)
        self.user_name_value = page.locator("#userName-value")

        # Кнопка логауту. На DemoQA вона теж має id="submit"
        self.logout_button = page.locator("#submit", has_text="Logout")

        # Кнопка переходу в Book Store зі сторінки профілю
        self.go_to_book_store_button = page.get_by_role("button", name="Go To Book Store")

        # Кнопка "Delete All Books" (також id="submit", тому шукаємо за текстом)
        self.delete_all_books_button = page.locator("#submit", has_text="Delete All Books")

        # Таблиця книг у профілі (колекція користувача)
        self.books_table = page.locator("table")
        self.books_rows = page.locator("table tbody tr")

    def goto(self) -> None:
        """Відкриває сторінку профілю."""
        self.page.goto("https://demoqa.com/profile")

    def wait_loaded(self) -> None:
        """
        Мінімальна перевірка, що сторінка профілю завантажилась:
        таблиця книг має бути видима.
        """
        expect(self.books_table).to_be_visible()

    def expect_user_name(self, username: str) -> None:
        """Перевіряє, що відображається правильний логін користувача."""
        expect(self.user_name_value).to_have_text(username)

    def expect_logout_visible(self) -> None:
        """Перевіряє, що кнопка Logout видима."""
        expect(self.logout_button).to_be_visible(timeout=10_000)

    def go_to_book_store(self) -> None:
        """Натискає кнопку переходу до Book Store."""
        self.go_to_book_store_button.click()

    def logout(self) -> None:
        """Вихід з акаунта зі сторінки профілю."""
        self.logout_button.click()

    def is_book_in_collection(self, title: str) -> bool:
        """
        Перевіряє, чи є книга з такою назвою у таблиці колекції.
        Повертає True/False без падіння тесту.
        """
        return self.page.get_by_role("link", name=title).is_visible()

    def expect_book_in_collection(self, title: str) -> None:
        """Очікує, що книга з такою назвою є в колекції (видиме посилання)."""
        expect(self.page.get_by_role("link", name=title)).to_be_visible()

    def delete_all_books_accept_dialog(self) -> None:
        """
        Натискає Delete All Books і автоматично підтверджує alert (OK).
        """
        self.page.once("dialog", lambda dialog: dialog.accept())
        self.delete_all_books_button.click()

    def expect_collection_empty(self) -> None:
        """Перевіряє, що таблиця колекції порожня (0 рядків у tbody)."""
        expect(self.books_rows).to_have_count(0)

