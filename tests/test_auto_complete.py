import pytest
from playwright.sync_api import expect
from pages.auto_complete_page import AutoCompletePage

@pytest.fixture
def auto_page(page):
    p = AutoCompletePage(page)
    p.navigate()
    return p

def test_fill_multiple_colors(auto_page):
    """Перевірка додавання декількох кольорів у поле Multiple"""
    colors = ["Red", "Blue", "Green"]
    
    for color in colors:
        # Вводимо перші літери та вибираємо повну назву
        auto_page.fill_and_select(auto_page.multiple_input, color[:2], color)
    
    # Перевіряємо, чи всі кольори відображаються як теги
    expect(auto_page.multiple_values).to_have_count(3)
    expect(auto_page.multiple_values).to_have_text(colors)

def test_remove_color_from_multiple(auto_page):
    """Перевірка видалення одного кольору з вибраних"""
    auto_page.fill_and_select(auto_page.multiple_input, "Re", "Red")
    auto_page.fill_and_select(auto_page.multiple_input, "Bl", "Blue")
    
    # Видаляємо перший колір (Red)
    auto_page.remove_value_btn.first.click()
    
    # Перевіряємо, що залишився тільки Blue
    expect(auto_page.multiple_values).to_have_count(1)
    expect(auto_page.multiple_values).to_have_text(["Blue"])

def test_fill_single_color(auto_page):
    """Перевірка заповнення поля з одним значенням"""
    color = "Yellow"
    auto_page.fill_and_select(auto_page.single_input, "Ye", color)
    
    # Перевіряємо результат
    expect(auto_page.single_value).to_have_text(color)
    
    # Спробуємо змінити на інший колір
    auto_page.fill_and_select(auto_page.single_input, "Pur", "Purple")
    expect(auto_page.single_value).to_have_text("Purple")