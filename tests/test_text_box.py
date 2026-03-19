import pytest
from pages.text_box_page import TextBoxPage

def test_fill_text_box_form_success(page):
    # Дані для тесту
    name = "Ivan Ivanov"
    email = "ivan@example.com"
    current_addr = "Kyiv, Ukraine"
    permanent_addr = "Lviv, Ukraine"

    text_box_page = TextBoxPage(page)

    # Відкриваємо сторінку
    text_box_page.navigate()

    # Заповнюємо форму та відправляємо
    text_box_page.fill_form(name, email, current_addr, permanent_addr)
    text_box_page.submit()

    # Перевіряємо результат у блоці Output
    text_box_page.check_output_data(name, email, current_addr, permanent_addr)

def test_email_validation_error(page):
    """Перевірка валідації некоректного email (поле має підсвітитися червоним)"""
    text_box_page = TextBoxPage(page)
    text_box_page.navigate()

    # Вводимо невалідний email
    text_box_page.email_input.fill("invalid-email")
    text_box_page.submit()

    # Перевіряємо наявність класу помилки (field-error)
    # В DemoQA при помилці додається клас 'field-error'
    from playwright.sync_api import expect
    expect(text_box_page.email_input).to_have_class(r"mr-sm-2 field-error form-control")