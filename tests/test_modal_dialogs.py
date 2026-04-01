import pytest
from playwright.sync_api import expect
from pages.modal_dialogs_page import ModalDialogsPage

@pytest.fixture
def modal_page(page):
    p = ModalDialogsPage(page)
    p.navigate()
    return p

def test_small_modal(modal_page):
    """Перевірка вмісту та закриття Small Modal"""
    modal_page.open_small_modal()
    
    # Перевіряємо заголовок та текст
    expect(modal_page.modal_title).to_have_text("Small Modal")
    expect(modal_page.modal_body).to_contain_text("This is a small modal. It has very less content")
    
    # Закриваємо
    modal_page.close_small_modal_btn.click()
    
    # Перевіряємо, що модалка зникла
    expect(modal_page.modal_content).to_be_hidden()

def test_large_modal(modal_page):
    """Перевірка вмісту та закриття Large Modal"""
    modal_page.open_large_modal()
    
    # Перевіряємо заголовок
    expect(modal_page.modal_title).to_have_text("Large Modal")
    
    # Велика модалка містить багато тексту, перевіримо частину
    expect(modal_page.modal_body).to_contain_text("Lorem Ipsum is simply dummy text")
    
    # Закриваємо
    modal_page.close_large_modal_btn.click()
    
    # Перевіряємо, що модалка зникла
    expect(modal_page.modal_content).to_be_hidden()

def test_close_modal_via_escape(modal_page):
    """Перевірка закриття модалки клавішею Escape"""
    modal_page.open_small_modal()
    expect(modal_page.modal_content).to_be_visible()
    
    # Емуляція натискання клавіші Esc
    modal_page.page.keyboard.press("Escape")
    
    expect(modal_page.modal_content).to_be_hidden()