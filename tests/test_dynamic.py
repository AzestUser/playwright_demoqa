import pytest
import re  
from playwright.sync_api import expect
from pages.dynamic_page import DynamicPage

@pytest.fixture
def dynamic_page(page):
    page.set_viewport_size({"width": 1920, "height": 1080})
    dp = DynamicPage(page)
    dp.navigate()
    return dp

def test_button_enables_after_five_seconds(dynamic_page):
    # Перевіряємо, що спочатку кнопка заблокована (опціонально)
    expect(dynamic_page.enable_after_btn).to_be_disabled(timeout=0)
    
    # Чекаємо, поки вона стане активною. 
    # Ставимо 6000мс, бо DemoQA іноді трохи пригальмовує
    expect(dynamic_page.enable_after_btn).to_be_enabled(timeout=6500)

def test_button_changes_color(dynamic_page):
    # На DemoQA колір змінюється на червоний (клас text-danger)
    # Ми можемо перевірити наявність класу або конкретний колір CSS
    
    # Чекаємо, поки у кнопки з'явиться клас 'text-danger'
    expect(dynamic_page.color_change_btn).to_have_class(
        re.compile(r"text-danger"), 
        timeout=6500
    )

def test_button_appears_after_five_seconds(dynamic_page):
    # Цей елемент взагалі відсутній в DOM перші 5 секунд
    expect(dynamic_page.visible_after_btn).to_be_visible(timeout=6500)

def test_random_id_text_is_present(dynamic_page):
    # Перевіряємо, що текст з рандомним ID просто є на сторінці
    expect(dynamic_page.random_id_text).to_be_visible()