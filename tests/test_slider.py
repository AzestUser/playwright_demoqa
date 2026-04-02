import pytest
from playwright.sync_api import expect
from pages.slider_page import SliderPage

@pytest.fixture
def slider_page(page):
    p = SliderPage(page)
    p.navigate()
    return p

def test_slider_default_value(slider_page):
    """Перевірка, що значення за замовчуванням дорівнює 25"""
    expect(slider_page.slider).to_have_value("25")
    expect(slider_page.slider_value_input).to_have_value("25")

def test_change_slider_value(slider_page):
    """Перевірка встановлення нового значення (наприклад, 85)"""
    target_value = 85
    slider_page.set_slider_value(target_value)
    
    # Перевіряємо, що повзунок змінив позицію
    expect(slider_page.slider).to_have_value(str(target_value))
    
    # Перевіряємо, що текстове поле оновилося
    expect(slider_page.slider_value_input).to_have_value(str(target_value))

def test_slider_max_min_values(slider_page):
    """Перевірка граничних значень (0 та 100)"""
    # Мінімум
    slider_page.set_slider_value(0)
    expect(slider_page.slider_value_input).to_have_value("0")
    
    # Максимум
    slider_page.set_slider_value(100)
    expect(slider_page.slider_value_input).to_have_value("100")