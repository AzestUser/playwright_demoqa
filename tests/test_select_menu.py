import pytest
from playwright.sync_api import expect
from pages.select_menu_page import SelectMenuPage

@pytest.fixture
def select_page(page):
    p = SelectMenuPage(page)
    p.navigate()
    return p

def test_standard_html_select(select_page):
    """Тест 1: Робота з класичним HTML <select> (цей у вас працював)"""
    select_page.standard_select.select_option(label="Aqua")
    expect(select_page.standard_select).to_have_value("10")

def test_custom_react_select(select_page):
    """Тест 2: Робота з кастомним React-Select (Grouped)"""
    select_page.value_dropdown.click()
    
    # Вводимо текст і тиснемо Enter. Це найнадійніший спосіб для React-Select!
    select_page.page.keyboard.type("Another root option")
    select_page.page.keyboard.press("Enter")
    
    expect(select_page.value_dropdown).to_contain_text("Another root option")

def test_custom_select_one(select_page):
    """Тест 3: Робота з кастомним React-Select (Titles)"""
    select_page.title_dropdown.click()
    
    select_page.page.keyboard.type("Dr.")
    select_page.page.keyboard.press("Enter")
    
    expect(select_page.title_dropdown).to_contain_text("Dr.")

def test_multi_select_dropdown(select_page):
    select_page.multi_select_input.click()
    select_page.page.keyboard.type("Green")
    select_page.page.keyboard.press("Enter")
    
    select_page.page.keyboard.type("Black")
    select_page.page.keyboard.press("Enter")
    
    expect(select_page.multi_container).to_contain_text("Green")
    expect(select_page.multi_container).to_contain_text("Black")