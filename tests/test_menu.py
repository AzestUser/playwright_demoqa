import pytest
from playwright.sync_api import expect
from pages.menu_page import MenuPage

@pytest.fixture
def menu_page(page):
    p = MenuPage(page)
    p.navigate()
    return p

def test_main_menu_items_visible(menu_page):
    """Перевірка, що основні пункти меню видимі"""
    expect(menu_page.main_item_1).to_be_visible()
    expect(menu_page.main_item_2).to_be_visible()
    expect(menu_page.main_item_3).to_be_visible()

def test_nested_menu_navigation(menu_page):
    """Перевірка відкриття підпунктів (Hover Chain)"""
    
    # 1. Наводимо на Main Item 2
    menu_page.main_item_2.hover()
    
    # Перевіряємо, що з'явився список підпунктів
    expect(menu_page.sub_sub_list).to_be_visible()
    
    # 2. Наводимо на Sub Sub List всередині другого пункту
    menu_page.sub_sub_list.hover()
    
    # Перевіряємо елементи найглибшого рівня
    expect(menu_page.sub_sub_item_1).to_be_visible()
    expect(menu_page.sub_sub_item_1).to_have_text("Sub Sub Item 1")
    
    expect(menu_page.sub_sub_item_2).to_be_visible()

def test_menu_closes_on_leave(menu_page):
    """Перевірка, що меню ховається, якщо прибрати курсор"""
    # Відкриваємо
    menu_page.main_item_2.hover()
    expect(menu_page.sub_sub_list).to_be_visible()
    
    # Відводимо мишу на Main Item 1 (де немає вкладеності)
    menu_page.main_item_1.hover()
    
    # Підменю має зникнути
    expect(menu_page.sub_sub_list).to_be_hidden()