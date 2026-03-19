from playwright.sync_api import Page, expect

class ProfilePage:
    def __init__(self, page: Page) -> None:
        self.page = page

        # Локатори
        self.user_name_value = page.locator("#userName-value")
        self.logout_button = page.locator("button#submit").filter(has_text="Logout")
        self.go_to_book_store_button = page.get_by_role("button", name="Go To Book Store")
        
        # Кнопки видалення та модалки
        self.delete_all_books_button = page.get_by_role("button", name="Delete All Books").first
        self.confirm_modal_button = page.locator("#closeSmallModal-ok")
        
        # Контейнери
        self.profile_wrapper = page.locator(".profile-wrapper")

    def goto(self) -> None:
        """Відкриває сторінку профілю."""
        self.page.goto("https://demoqa.com/profile")

    def wait_loaded(self) -> None:
        """Очікує повного завантаження контейнера профілю."""
        self.profile_wrapper.wait_for(state="visible", timeout=10000)

    def go_to_book_store(self) -> None:
        """Натискає кнопку переходу в магазин."""
        self.go_to_book_store_button.click()

    def logout(self) -> None:
        """Вихід із системи."""
        self.logout_button.click()

    def expect_logout_visible(self) -> None:
        """Перевірка авторизації."""
        expect(self.logout_button).to_be_visible(timeout=10000)

    def is_book_in_collection(self, title: str) -> bool:
        """Повертає True, якщо книга є в таблиці (для логічних розгалужень у тесті)."""
        return self.page.get_by_role("link", name=title).is_visible()

    # --- МЕТОДИ ПЕРЕВІРОК (Assertions), ЯКИХ НЕ ВИСТАЧАЛО ---

    def expect_book_in_collection(self, title: str) -> None:
        """Перевіряє, чи книга з таким заголовком з'явилася в таблиці."""
        expect(self.page.get_by_role("link", name=title)).to_be_visible(timeout=10000)

    def expect_collection_empty(self) -> None:
        """Перевіряє, що в таблиці профілю немає жодної книги."""
        # На DemoQA в порожній таблиці немає посилань <a> всередині тіла таблиці
        books_links = self.page.locator(".rt-tbody a")
        expect(books_links).to_have_count(0, timeout=5000)

    def delete_all_books_accept_dialog(self) -> None:
        """Повний цикл видалення всіх книг з обробкою діалогу."""
        self.page.once("dialog", lambda dialog: dialog.accept())
        if self.delete_all_books_button.is_visible():
            self.delete_all_books_button.click()
            self.confirm_modal_button.wait_for(state="visible", timeout=5000)
            self.confirm_modal_button.click(force=True)
            self.page.wait_for_timeout(1000) # Даємо час базі даних оновитися після видалення.