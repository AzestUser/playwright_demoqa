from playwright.sync_api import Page, expect

"""
Page Object для сторінки Book Store DemoQA: https://demoqa.com/books

Тут є список книг. Ми в тестах зазвичай:
- відкриваємо Book Store;
- клікаємо по назві книги, щоб перейти на сторінку деталей.
"""


class BookStorePage:
    def __init__(self, page: Page) -> None:
        self.page = page

        # На сторінці є таблиця зі списком книг
        self.books_table = page.locator(".rt-table")

    def goto(self) -> None:
        """Відкриває сторінку Book Store."""
        self.page.goto("https://demoqa.com/books")

    def wait_loaded(self) -> None:
        """Мінімальна перевірка завантаження сторінки Book Store."""
        expect(self.books_table).to_be_visible()

    def open_book_details(self, title: str) -> None:
        """
        Відкриває деталі книги, клікаючи по її назві в списку.
        """
        self.page.get_by_role("link", name=title).click()

