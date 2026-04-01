import pytest
from playwright.sync_api import expect
from pages.nested_frames_page import NestedFramesPage

@pytest.fixture
def nested_page(page):
    p = NestedFramesPage(page)
    p.navigate()
    return p

def test_parent_frame_text(nested_page):
    """Перевірка наявності тексту в батьківському фреймі"""
    # Очікуємо, що в тілі батьківського фрейму є потрібний текст
    expect(nested_page.parent_text).to_contain_text("Parent frame")

def test_child_frame_text(nested_page):
    """Перевірка наявності тексту у вкладеному (дочірньому) фреймі"""
    # Змінено 'iframe' на 'Iframe'
    expect(nested_page.child_text).to_have_text("Child Iframe")

def test_nested_frames_interaction(nested_page):
    """Комплексна перевірка обох рівнів"""
    p_text = nested_page.parent_text.inner_text()
    c_text = nested_page.child_text.inner_text()
    
    assert "Parent frame" in p_text
    # Змінено 'iframe' на 'Iframe'
    assert c_text == "Child Iframe"