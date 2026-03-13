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

        # Поле пошуку книг (стабільний елемент на сторінці Book Store)
        self.search_box = page.locator("#searchBox")

    def goto(self) -> None:
        """Відкриває сторінку Book Store."""
        self.page.goto("https://demoqa.com/books")

    def wait_loaded(self) -> None:
        """
        Мінімальна перевірка завантаження сторінки Book Store:
        чекаємо, доки з'явиться поле пошуку книг.
        """
        expect(self.search_box).to_be_visible()

    def open_book_details(self, title: str) -> None:
        """
        Відкриває деталі книги, клікаючи по її назві в списку.
        """
        self.page.get_by_role("link", name=title).click()


