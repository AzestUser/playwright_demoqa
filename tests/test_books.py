import pytest
from playwright.sync_api import Page

"""
Тести для роботи з книгами в DemoQA Book Store.

Кожен тест логінується самостійно перед тим, як почати роботу.
"""

# Page Objects
from pages.login_page import LoginPage
from pages.profile_page import ProfilePage
from pages.book_store_page import BookStorePage
from pages.book_details_page import BookDetailsPage

# Назва книги, з якою працюватимемо у сценаріях
BOOK_TITLE = "Git Pocket Guide"
USERNAME = "Test_User"
PASSWORD = "Test_User123!"


def login_helper(page: Page) -> None:
    """Допоміжна функція для логіну перед кожним тестом."""
    login_page = LoginPage(page)
    login_page.goto()
    login_page.login(USERNAME, PASSWORD)


def test_books_list_visible(page: Page) -> None:
    """
    Перевіряємо, що на сторінці профілю відображається таблиця з книгами.
    Це базова перевірка, що ми успішно потрапили в особистий кабінет.
    """
    login_helper(page)
    
    profile = ProfilePage(page)
    profile.goto()
    profile.wait_loaded()


def test_add_book_to_collection(page: Page) -> None:
    """
    Сценарій: перейти в Book Store, відкрити книгу за назвою
    і додати її в свою колекцію. Потім перевірити, що книга
    з'явилась у списку на сторінці профілю.
    """
    login_helper(page)
    
    profile = ProfilePage(page)
    store = BookStorePage(page)
    details = BookDetailsPage(page)

    # 1. Йдемо в профіль і переходимо в Book Store
    profile.goto()
    profile.wait_loaded()
    profile.go_to_book_store()

    # 2. Відкриваємо книгу і додаємо її в колекцію
    store.wait_loaded()
    store.open_book_details(BOOK_TITLE)
    details.wait_loaded(BOOK_TITLE)
    details.add_to_collection_accept_dialog()

    # 3. Повертаємося на профіль і перевіряємо, що книга є в колекції
    profile.goto()
    profile.expect_book_in_collection(BOOK_TITLE)


def test_delete_all_books(page: Page) -> None:
    """
    Сценарій: видалити всі книги з колекції користувача
    та переконатися, що таблиця стала порожньою.
    """
    login_helper(page)
    
    profile = ProfilePage(page)
    store = BookStorePage(page)
    details = BookDetailsPage(page)

    # Робимо тест незалежним: якщо книги ще немає — додамо її.
    profile.goto()
    profile.wait_loaded()
    if not profile.is_book_in_collection(BOOK_TITLE):
        profile.go_to_book_store()
        store.wait_loaded()
        store.open_book_details(BOOK_TITLE)
        details.wait_loaded(BOOK_TITLE)
        details.add_to_collection_accept_dialog()
        profile.goto()
        profile.wait_loaded()

    # Тепер видаляємо всі книги і перевіряємо, що колекція порожня
    profile.delete_all_books_accept_dialog()
    profile.expect_collection_empty()


