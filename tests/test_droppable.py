import pytest
import re
from playwright.sync_api import expect
from pages.droppable_page import DroppablePage

@pytest.fixture
def droppable_page(page):
    p = DroppablePage(page)
    p.navigate()
    return p

# === 1. ТЕСТ ВКЛАДКИ SIMPLE ===
def test_simple_drop(droppable_page):
    droppable_page.tab_simple.click()
    droppable_page.page.wait_for_timeout(300)
    
    droppable_page.drag_by_coordinates(droppable_page.simple_drag, droppable_page.simple_drop)
    
    expect(droppable_page.simple_drop).to_have_text("Dropped!")
    expect(droppable_page.simple_drop).to_have_class(re.compile(r"ui-state-highlight"))


# === 2. ТЕСТ ВКЛАДКИ ACCEPT ===
def test_accept_drop(droppable_page):
    droppable_page.tab_accept.click()
    
    # Спроба перетягнути елемент, який НЕ приймається
    droppable_page.drag_and_drop(droppable_page.not_accept_drag, droppable_page.accept_drop)
    expect(droppable_page.accept_drop).to_have_text("Drop here") # Стан не змінився
    
    # Тягнемо валідний елемент
    droppable_page.drag_and_drop(droppable_page.accept_drag, droppable_page.accept_drop)
    expect(droppable_page.accept_drop).to_have_text("Dropped!")
    expect(droppable_page.accept_drop).to_have_class(re.compile(r"ui-state-highlight"))


# === 3. ТЕСТ ВКЛАДКИ PREVENT PROPOGATION ===
def test_prevent_propogation_greedy(droppable_page):
    droppable_page.tab_prevent.click()
    droppable_page.page.wait_for_timeout(300)
    
    # Тягнемо у внутрішній "Нежадібний" (Not Greedy) бокс
    # Має спрацювати і внутрішній, і зовнішній
    droppable_page.drag_by_coordinates(droppable_page.prevent_drag, droppable_page.not_greedy_inner)
    expect(droppable_page.not_greedy_outer).to_contain_text("Dropped!")
    expect(droppable_page.not_greedy_inner).to_have_text("Dropped!")
    
    # Перезавантажуємо сторінку для чистоти другого тесту на цій вкладці
    droppable_page.page.reload()
    droppable_page.page.wait_for_timeout(500)
    droppable_page.tab_prevent.click()
    droppable_page.page.wait_for_timeout(300)
    
    # Тягнемо у внутрішній "Жадібний" (Greedy) бокс
    # Має спрацювати ТІЛЬКИ внутрішній
    droppable_page.drag_by_coordinates(droppable_page.prevent_drag, droppable_page.greedy_inner)
    expect(droppable_page.greedy_outer.locator("p").first).to_have_text("Outer droppable") # Залишився старим
    expect(droppable_page.greedy_inner).to_have_text("Dropped!")


# === 4. ТЕСТ ВКЛАДКИ REVERT DRAGGABLE ===
def test_revert_draggable(droppable_page):
    droppable_page.tab_revert.click()
    
    # Тягнемо Revertable
    start_box = droppable_page.revertable_drag.bounding_box()
    droppable_page.drag_and_drop(droppable_page.revertable_drag, droppable_page.revert_drop)
    
    # Чекаємо секунду, поки спрацює анімація повернення на базу
    droppable_page.page.wait_for_timeout(1000)
    end_box = droppable_page.revertable_drag.bounding_box()
    
    # Елемент повернувся на своє місце
    assert abs(start_box['x'] - end_box['x']) <= 5
    
    # Тягнемо Not Revertable
    droppable_page.drag_and_drop(droppable_page.not_revertable_drag, droppable_page.revert_drop)
    droppable_page.page.wait_for_timeout(1000)
    
    # Елемент залишився всередині Drop-зони
    final_box = droppable_page.not_revertable_drag.bounding_box()
    assert abs(start_box['x'] - final_box['x']) > 50 # Змістився далеко
    