from playwright.sync_api import Page, expect

"""
Page Object для сторінки профілю DemoQA: https://demoqa.com/profile
Виправлений з урахуванням особливостей React-таблиць та діалогових вікон.
"""

class ProfilePage:
    def __init__(self, page: Page) -> None:
        self.page = page

        # Лейбл з логіном користувача
        self.user_name_value = page.locator("#userName-value")

        # Кнопка логауту
        self.logout_button = page.locator("#submit", has_text="Logout")

        # Кнопка переходу в Book Store
        self.go_to_book_store_button = page.get_by_role("button", name="Go To Book Store")

        # Кнопка "Delete All Books"
        # Використовуємо .first, бо на сторінці може бути прихований дублікат цієї кнопки для мобільної версії
        self.delete_all_books_button = page.get_by_role("button", name="Delete All Books").first
        
        # Кнопка підтвердження у модальному вікні, що з'являється ПІСЛЯ натискання Delete All
        self.confirm_modal_button = page.locator("#closeSmallModal-ok")

        # --- ТАБЛИЦЯ З КНИГАМИ ---
        # DemoQA використовує звичайний HTML <table> елемент
        self.books_table = page.locator("table")

        # Рядки таблиці з книгами (tbody tr)
        self.books_rows = page.locator("table tbody tr")

    def goto(self) -> None:
        """Відкриває сторінку профілю."""
        self.page.goto("https://demoqa.com/profile")

    def wait_loaded(self) -> None:
        """Очікує появи таблиці як ознаки завантаження профілю."""
        expect(self.books_table).to_be_visible()

    def expect_user_name(self, username: str) -> None:
        """Перевіряє ім'я користувача."""
        expect(self.user_name_value).to_have_text(username)

    def expect_logout_visible(self) -> None:
        """Перевіряє видимість кнопки виходу."""
        expect(self.logout_button).to_be_visible(timeout=10_000)

    def go_to_book_store(self) -> None:
        """Перехід до магазину книг."""
        self.go_to_book_store_button.click()

    def logout(self) -> None:
        """Вихід з системи."""
        self.logout_button.click()

    def is_book_in_collection(self, title: str) -> bool:
        """Перевіряє наявність конкретної книги за назвою (повертає True/False)."""
        return self.page.get_by_role("link", name=title).is_visible()

    def expect_book_in_collection(self, title: str) -> None:
        """Очікує, що книга з'явиться в колекції."""
        expect(self.page.get_by_role("link", name=title)).to_be_visible(timeout=10_000)

    def delete_all_books_accept_dialog(self) -> None:
        """
        Метод для повного циклу видалення книг:
        1. Клік по кнопці видалення.
        2. Обробка браузерного Alert.
        3. Клік по кнопці в модальному вікні.
        4. Оновлення сторінки для синхронізації стану.
        """
        # Натискаємо червону кнопку видалення
        self.delete_all_books_button.click()
        
        # Готуємо Playwright до того, що зараз вискочить системний Alert ("All books deleted")
        # Ми кажемо йому автоматично натиснути "OK" (accept), коли він з'явиться
        self.page.once("dialog", lambda dialog: dialog.accept())
        
        # Натискаємо "OK" у спливаючому вікні на самій сторінці
        self.confirm_modal_button.click()
        
        # ПОРАДА: DemoQA часто "флакує" (глючить) і не прибирає рядки з екрана миттєво.
        # page.reload() — найнадійніший спосіб переконатися, що ми бачимо актуальний стан бази даних.
        self.page.reload()

    def expect_collection_empty(self) -> None:
        """Перевіряє, що таблиця порожня."""
        # Перевіряємо, що кількість рядків стала 0
        expect(self.books_rows).to_have_count(0)