import pytest
from playwright.sync_api import expect
from pages.tool_tips_page import ToolTipsPage

@pytest.fixture
def tt_page(page):
    p = ToolTipsPage(page)
    p.navigate()
    return p

def test_button_tooltip(tt_page):
    """Перевірка підказки при наведенні на кнопку"""
    tt_page.button.hover()
    
    # Перевіряємо, що підказка стала видимою і має правильний текст
    expect(tt_page.tooltip).to_be_visible()
    expect(tt_page.tooltip).to_have_text("You hovered over the Button")

def test_input_tooltip(tt_page):
    """Перевірка підказки при наведенні на текстове поле"""
    tt_page.input_field.hover()
    
    expect(tt_page.tooltip).to_be_visible()
    expect(tt_page.tooltip).to_have_text("You hovered over the text field")

def test_links_tooltips(tt_page):
    """Перевірка підказок для посилань у тексті"""
    
    # 1. Перевірка для "Contrary"
    tt_page.contrary_link.hover()
    expect(tt_page.tooltip).to_have_text("You hovered over the Contrary")
    
    # --- СКИДАННЯ СТАНУ ---
    # Наводимо на заголовок, де немає підказок
    tt_page.page.locator("h1").hover()
    # ЧЕКАЄМО, поки стара підказка зникне з DOM
    expect(tt_page.tooltip).to_be_hidden()
    
    # 2. Тепер наводимо на "1.10.32"
    tt_page.section_link.hover()
    # Тепер помилки "resolved to 2 elements" не буде
    expect(tt_page.tooltip).to_have_text("You hovered over the 1.10.32")

    # Ще раз скидаємо для порядку
    tt_page.page.locator("h1").hover()
    expect(tt_page.tooltip).to_be_hidden()

def test_tooltip_disappears(tt_page):
    """Перевірка, що підказка зникає, якщо прибрати курсор"""
    tt_page.button.hover()
    expect(tt_page.tooltip).to_be_visible()
    
    # Наводимо на порожнє місце або заголовок
    tt_page.page.locator("h1").hover()
    
    # Підказка має зникнути з DOM або стати прихованою
    expect(tt_page.tooltip).to_be_hidden()