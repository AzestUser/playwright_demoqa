from playwright.sync_api import Page, expect

"""
Page Object для сторінки деталей книги DemoQA.

Коли ми клікаємо на книгу в Book Store, відкривається сторінка,
де можна додати книгу до своєї колекції.
"""


class BookDetailsPage:
    def __init__(self, page: Page) -> None:
        self.page = page

        # Кнопка додавання книги до колекції
        self.add_to_collection_button = page.get_by_role("button", name="Add To Your Collection")

    def wait_loaded(self, title: str | None = None) -> None:
        """
        Мінімальна перевірка, що сторінка деталей відкрилась.

        Якщо передати title, додатково перевіримо, що заголовок/посилання з назвою книги видно.
        """
        expect(self.add_to_collection_button).to_be_visible()
        if title:
            expect(self.page.get_by_text(title)).to_be_visible()

    def add_to_collection_accept_dialog(self) -> None:
        """
        Натискає "Add To Your Collection" і підтверджує alert (OK),
        який показує DemoQA після додавання.
        """
        self.page.once("dialog", lambda dialog: dialog.accept())
        self.add_to_collection_button.click()

