import pytest
from pages.sortable_page import SortablePage

@pytest.fixture
def sort_page(page):
    p = SortablePage(page)
    p.navigate()
    return p

def test_sort_list_descending(sort_page):
    sort_page.tab_list.click()
    
    # Послідовність елементів, які ми будемо "кидати наверх" один за одним
    to_move_up = ["Two", "Three", "Four", "Five", "Six"]
    expected_order = ["Six", "Five", "Four", "Three", "Two", "One"]
    
    for item in to_move_up:
        sort_page.drag_and_drop_to_top("#demo-tabpane-list", item)
    
    actual_order = sort_page.get_items_text(sort_page.list_items)
    assert actual_order == expected_order, f"Помилка! Отримали: {actual_order}"

def test_sort_grid_descending(sort_page):
    sort_page.tab_grid.click()
    
    to_move_up = ["Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"]
    expected_order = ["Nine", "Eight", "Seven", "Six", "Five", "Four", "Three", "Two", "One"]
    
    for item in to_move_up:
        sort_page.drag_and_drop_to_top("#demo-tabpane-grid", item)
    
    actual_order = sort_page.get_items_text(sort_page.grid_items)
    assert actual_order == expected_order, f"Помилка! Отримали: {actual_order}"