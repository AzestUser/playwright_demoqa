import pytest
from pages.draggable_page import DraggablePage

@pytest.fixture
def draggable_page(page):
    p = DraggablePage(page)
    p.navigate()
    return p

# === 1. ТЕСТ ВКЛАДКИ SIMPLE ===
def test_simple_draggable(draggable_page):
    draggable_page.tab_simple.click()
    draggable_page.page.wait_for_timeout(300)
    
    start_box = draggable_page.simple_drag.bounding_box()
    
    # Тягнемо по діагоналі на 100 пікселів вправо і вниз
    draggable_page.drag_by_offset(draggable_page.simple_drag, 100, 100)
    
    end_box = draggable_page.simple_drag.bounding_box()
    
    # Перевіряємо, що елемент дійсно перемістився
    assert abs((end_box['x'] - start_box['x']) - 100) <= 5
    assert abs((end_box['y'] - start_box['y']) - 100) <= 5


# === 2. ТЕСТ ВКЛАДКИ AXIS RESTRICTED ===
def test_axis_restricted_draggable(draggable_page):
    draggable_page.tab_axis.click()
    draggable_page.page.wait_for_timeout(300)
    
    # Тест осі X (має рухатися ТІЛЬКИ вправо/вліво)
    start_x_box = draggable_page.only_x.bounding_box()
    draggable_page.drag_by_offset(draggable_page.only_x, 100, 100)
    end_x_box = draggable_page.only_x.bounding_box()
    
    assert abs((end_x_box['x'] - start_x_box['x']) - 100) <= 25
    assert abs(end_x_box['y'] - start_x_box['y']) <= 5 # Y не змінився
    
    # Тест осі Y (має рухатися ТІЛЬКИ вгору/вниз)
    start_y_box = draggable_page.only_y.bounding_box()
    draggable_page.drag_by_offset(draggable_page.only_y, 100, 100)
    end_y_box = draggable_page.only_y.bounding_box()
    
    assert abs(end_y_box['x'] - start_y_box['x']) <= 5 # X не змінився
    assert abs((end_y_box['y'] - start_y_box['y']) - 100) <= 25


# === 3. ТЕСТ ВКЛАДКИ CONTAINER RESTRICTED ===
def test_container_restricted_draggable(draggable_page):
    draggable_page.tab_container.click()
    draggable_page.page.wait_for_timeout(300)
    
    container_box = draggable_page.container_box.bounding_box()
    
    # Спробуємо викинути блок ДАЛЕКО за межі контейнера (на 1000 пікселів)
    draggable_page.drag_by_offset(draggable_page.box_in_container, 1000, 1000)
    
    element_box = draggable_page.box_in_container.bounding_box()
    
    # Перевіряємо, що правий і нижній краї блоку не вилізли за рамки контейнера
    element_right_edge = element_box['x'] + element_box['width']
    element_bottom_edge = element_box['y'] + element_box['height']
    
    container_right_edge = container_box['x'] + container_box['width']
    container_bottom_edge = container_box['y'] + container_box['height']
    
    assert element_right_edge <= container_right_edge + 5
    assert element_bottom_edge <= container_bottom_edge + 5


# === 4. ТЕСТ ВКЛАДКИ CURSOR STYLE ===
def test_cursor_style_draggable(draggable_page):
    draggable_page.tab_cursor.click()
    draggable_page.page.wait_for_timeout(300)
    
    # Для цієї вкладки ми просто перевіримо, що елементи взагалі можна перемістити, 
    # оскільки зміна стилів курсору — це суто візуальний CSS-ефект (cursor: move)
    start_box = draggable_page.cursor_center.bounding_box()
    
    draggable_page.drag_by_offset(draggable_page.cursor_center, 50, 50)
    
    end_box = draggable_page.cursor_center.bounding_box()
    
    # Переконуємося, що хоча б один із них зсунувся
    assert abs((end_box['x'] - start_box['x']) - 50) <= 10