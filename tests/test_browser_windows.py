import pytest
from playwright.sync_api import expect
from pages.browser_windows_page import BrowserWindowsPage

@pytest.fixture
def windows_page(page):
    # Встановлюємо великий екран
    page.set_viewport_size({"width": 1920, "height": 1080})
    p = BrowserWindowsPage(page)
    p.navigate()
    return p

def test_open_new_tab(windows_page):
    # 1. Відкриваємо нову вкладку
    new_tab = windows_page.click_new_tab()
    
    # 2. Переконуємося, що вона завантажилася
    new_tab.wait_for_load_state()
    
    # 3. Перевіряємо URL та текст на новій вкладці
    expect(new_tab).to_have_url("https://demoqa.com/sample")
    
    # Шукаємо заголовок на новій сторінці, використовуючи локатор з POM, 
    # але прив'язаний до контексту new_tab
    heading = new_tab.locator("#sampleHeading")
    expect(heading).to_be_visible()
    expect(heading).to_have_text("This is a sample page")
    
    # 4. Закриваємо вкладку
    new_tab.close()

def test_open_new_window(windows_page):
    # 1. Відкриваємо нове вікно
    new_window = windows_page.click_new_window()
    
    # 2. Чекаємо завантаження
    new_window.wait_for_load_state()
    
    # 3. Перевірки (логіка така ж, як і для вкладки)
    expect(new_window).to_have_url("https://demoqa.com/sample")
    heading = new_window.locator("#sampleHeading")
    expect(heading).to_be_visible()
    expect(heading).to_have_text("This is a sample page")
    
    # 4. Закриваємо вікно
    new_window.close()

#@pytest.mark.skip(reason="На DemoQA це вікно часто відкривається порожнім або ламається")
def test_open_new_window_message(windows_page):
    # 1. Відкриваємо вікно з повідомленням
    msg_window = windows_page.click_new_window_message()
    
    # 2. Чекаємо завантаження (це вікно специфічне, іноді networkidle допомагає)
    msg_window.wait_for_load_state("networkidle")
    
    # 3. Перевіряємо текст тіла сторінки, бо там немає тегів
    body_text = msg_window.locator("body").text_content()
    assert "Knowledge increases by sharing but not by saving" in body_text
    
    # 4. Закриваємо вікно
    msg_window.close()