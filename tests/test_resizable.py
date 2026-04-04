import pytest
import random
from playwright.sync_api import expect
from pages.resizable_page import ResizablePage


def random_target_in_direction(current, min_value, max_value):
    """
    Випадково обираємо менший або більший розмір відносно поточного.
    Це забезпечує як збільшення, так і зменшення resize-операцій.
    """
    if min_value >= max_value:
        return min_value

    if current <= min_value:
        return random.randint(min_value + 1, max_value)

    if current >= max_value:
        return random.randint(min_value, max_value - 1)

    if random.choice([True, False]):
        return random.randint(min_value, current - 1)

    return random.randint(current + 1, max_value)


@pytest.fixture
def resizable_page(page):
    p = ResizablePage(page)
    p.navigate()
    return p

def test_resize_restricted_box_randomly(resizable_page):
    """Тест обмеженого боксу: min 150x150, max 500x300."""
    
    current_box = resizable_page.restricted_box.bounding_box()
    current_w = current_box['width']
    current_h = current_box['height']

    # Випадково збільшуємо або зменшуємо розмір від поточного стану
    random_w = random_target_in_direction(current_w, 150, 500)
    random_h = random_target_in_direction(current_h, 150, 300)

    resizable_page.resize_element(resizable_page.restricted_handle, random_w, random_h)
    
    final_box = resizable_page.restricted_box.bounding_box()
    
    assert abs(final_box['width'] - random_w) <= 2
    assert abs(final_box['height'] - random_h) <= 2
    print(f"\nRestricted Box resized from {int(current_w)}x{int(current_h)} to: {random_w}x{random_h}")

def test_resize_unrestricted_box_randomly(resizable_page):
    """Тест вільного боксу: випадкове збільшення або зменшення до розмірів 100-600."""
    
    current_box = resizable_page.unrestricted_box.bounding_box()
    current_w = current_box['width']
    current_h = current_box['height']

    random_w = random_target_in_direction(current_w, 100, 600)
    random_h = random_target_in_direction(current_h, 100, 600)
    
    # Прокручуємо до елемента, щоб він був у зоні видимості
    resizable_page.unrestricted_box.scroll_into_view_if_needed()
    
    resizable_page.resize_element(resizable_page.unrestricted_handle, random_w, random_h)
    
    final_box = resizable_page.unrestricted_box.bounding_box()
    
    assert abs(final_box['width'] - random_w) <= 2
    assert abs(final_box['height'] - random_h) <= 2
    print(f"\nUnrestricted Box resized from {int(current_w)}x{int(current_h)} to: {random_w}x{random_h}")
