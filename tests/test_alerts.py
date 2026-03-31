import pytest
from playwright.sync_api import expect
from pages.alerts_page import AlertsPage

@pytest.fixture
def alerts_page(page):
    page_obj = AlertsPage(page)
    page_obj.navigate()
    return page_obj

def test_simple_alert(alerts_page):
    """Перевірка звичайного alert (тільки кнопка OK)"""
    alerts_page.handle_dialog(action="accept")
    alerts_page.alert_btn.click()
    # Якщо тест не впав — alert було успішно оброблено

def test_timer_alert(alerts_page):
    """Перевірка alert, що з'являється через 5 секунд"""
    alerts_page.handle_dialog(action="accept")
    alerts_page.timer_alert_btn.click()
    
    # Playwright чекатиме появи діалогу автоматично протягом тайм-ауту
    alerts_page.page.wait_for_timeout(6000) # Даємо час таймеру спрацювати

def test_confirm_box_accept(alerts_page):
    """Перевірка Confirm Box — натискання OK"""
    alerts_page.handle_dialog(action="accept")
    alerts_page.confirm_btn.click()
    
    expect(alerts_page.confirm_result).to_have_text("You selected Ok")

def test_confirm_box_dismiss(alerts_page):
    """Перевірка Confirm Box — натискання Cancel"""
    alerts_page.handle_dialog(action="dismiss")
    alerts_page.confirm_btn.click()
    
    expect(alerts_page.confirm_result).to_have_text("You selected Cancel")

def test_prompt_box(alerts_page):
    """Перевірка Prompt Box — введення тексту"""
    user_name = "Gemini AI"
    alerts_page.handle_dialog(prompt_text=user_name)
    alerts_page.prompt_btn.click()
    
    expect(alerts_page.prompt_result).to_contain_text(f"You entered {user_name}")