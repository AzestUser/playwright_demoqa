import pytest
import re
from playwright.sync_api import expect
from pages.progress_bar_page import ProgressBarPage

@pytest.fixture
def progress_page(page):
    p = ProgressBarPage(page)
    p.navigate()
    return p

def test_progress_reaches_100_percent(progress_page):
    progress_page.start_stop_button.click()
    
    # Чекаємо 100%
    expect(progress_page.progress_bar).to_have_text("100%", timeout=20000)
    
    # ВИПРАВЛЕНО: використовуємо регулярний вираз замість лямбди
    expect(progress_page.progress_bar).to_have_class(re.compile(r"bg-success"))

def test_stop_at_specific_value(progress_page):
    """Тест: Зупинка прогресу на позначці 50% (+/- 2%)"""
    target = 50
    progress_page.start_stop_button.click()
    
    # Чекаємо в циклі або через функцію, поки значення не стане >= 50
    progress_page.page.wait_for_function(
        f"document.querySelector('div[role=\"progressbar\"]').getAttribute('aria-valuenow') >= {target}"
    )
    
    # Зупиняємо
    progress_page.start_stop_button.click()
    
    current_value = progress_page.get_progress_value()
    print(f"Stopped at: {current_value}%")
    
    # Допускаємо невелику похибку через швидкість виконання скрипта
    assert target <= current_value <= target + 5

def test_reset_functionality(progress_page):
    """Тест: Скидання прогресу після завершення"""
    # 1. Починаємо прогрес
    progress_page.start_stop_button.click()
    
    # 2. Чекаємо, поки текст стане "100%"
    expect(progress_page.progress_bar).to_have_text("100%", timeout=20000)
    
    # 3. Скидаємо — після reset прогрес автоматично стартує знову
    progress_page.reset_button.click()
    
    # 4. Одразу зупиняємо
    progress_page.start_stop_button.click()
    
    # 5. Перевіряємо, що значення скинулось (менше 10%)
    assert progress_page.get_progress_value() < 10