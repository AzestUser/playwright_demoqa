import pytest
import re
from playwright.sync_api import expect
from pages.selectable_page import SelectablePage

@pytest.fixture
def selectable_page(page):
    p = SelectablePage(page)
    p.navigate()
    return p

def test_random_list_selection(selectable_page):
    """Тест для вкладки LIST"""
    selectable_page.tab_list.click()
    
    # Вибираємо рандомні елементи зі списку
    selected_texts, expected_count = selectable_page.select_random_from(selectable_page.list_items)
    
    # 1. Перевіряємо загальну кількість активних елементів у списку
    active_items = selectable_page.page.locator("#verticalListContainer .list-group-item.active")
    expect(active_items).to_have_count(expected_count)
    
    # 2. Перевіряємо, що саме ті елементи, на які ми клікнули, стали активними
    for text in selected_texts:
        target = selectable_page.list_items.filter(has_text=text)
        # ВИПРАВЛЕННЯ: використовуємо регулярний вираз замість лямбди
        expect(target).to_have_class(re.compile(r"active"))

def test_random_grid_selection(selectable_page):
    """Тест для вкладки GRID"""
    selectable_page.tab_grid.click()
    
    # Вибираємо рандомні елементи з сітки
    selected_texts, expected_count = selectable_page.select_random_from(selectable_page.grid_items)
    
    # 1. Перевіряємо загальну кількість активних елементів у сітці
    active_items = selectable_page.page.locator("#gridContainer .list-group-item.active")
    expect(active_items).to_have_count(expected_count)
    
    # 2. Перевіряємо кожну обрану плитку
    for text in selected_texts:
        target = selectable_page.grid_items.filter(has_text=text)
        expect(target).to_have_class(re.compile(r"active"))