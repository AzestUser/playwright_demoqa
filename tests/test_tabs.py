import pytest
import re  # Обов'язково додаємо імпорт регулярних виразів
from playwright.sync_api import expect
from pages.tabs_page import TabsPage

@pytest.fixture
def tabs_page(page):
    p = TabsPage(page)
    p.navigate()
    return p

def test_initial_tab_is_active(tabs_page):
    """Перевірка, що вкладка 'What' активна за замовчуванням"""
    # ВИПРАВЛЕНО: використовуємо re.compile замість lambda
    expect(tabs_page.tab_what).to_have_class(re.compile(r"active"))
    expect(tabs_page.pane_what).to_be_visible()
    expect(tabs_page.pane_what).to_contain_text("Lorem Ipsum")

def test_switch_to_origin_tab(tabs_page):
    """Перевірка перемикання на вкладку 'Origin'"""
    tabs_page.tab_origin.click()
    
    # ВИПРАВЛЕНО: використовуємо re.compile
    expect(tabs_page.tab_origin).to_have_class(re.compile(r"active"))
    expect(tabs_page.pane_origin).to_be_visible()
    expect(tabs_page.pane_origin).to_contain_text("Contrary to popular belief")
    
    expect(tabs_page.pane_what).to_be_hidden()

def test_switch_to_use_tab(tabs_page):
    """Перевірка перемикання на вкладку 'Use'"""
    tabs_page.tab_use.click()
    
    # ВИПРАВЛЕНО: використовуємо re.compile
    expect(tabs_page.tab_use).to_have_class(re.compile(r"active"))
    expect(tabs_page.pane_use).to_be_visible()
    expect(tabs_page.pane_use).to_contain_text("It is a long established fact")

def test_more_tab_is_disabled(tabs_page):
    """Перевірка, що вкладка 'More' недоступна для кліку"""
    # ВИПРАВЛЕНО: перевіряємо наявність класу 'disabled' через Regex
    expect(tabs_page.tab_more).to_have_class(re.compile(r"disabled"))
    
    # Спроба кліку (force=True дозволяє клікнути навіть якщо CSS каже "ні")
    tabs_page.tab_more.click(force=True)
    
    # Перевіряємо, що вкладка НЕ стала активною
    expect(tabs_page.tab_more).not_to_have_class(re.compile(r"active"))