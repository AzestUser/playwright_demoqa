import pytest
import re
from playwright.sync_api import expect
from pages.broken_page import BrokenPage

@pytest.fixture
def broken_page(page):
    page.set_viewport_size({"width": 1920, "height": 1080})
    bp = BrokenPage(page)
    bp.navigate()
    return bp

# --- Блок тестів зображень ---

def test_valid_image_displays_correctly(broken_page):
    # Даємо картинкам трохи часу "прогрузитися" (на випадок гальмівного сервера)
    broken_page.page.wait_for_load_state("networkidle")
    
    is_broken = broken_page.is_image_broken(broken_page.valid_image)
    assert is_broken is False, "Валідне зображення не завантажилося (naturalWidth == 0)"

def test_broken_image_does_not_display(broken_page):
    """Перевіряємо, що зламане зображення дійсно зламане (naturalWidth == 0)"""
    is_broken = broken_page.is_image_broken(broken_page.broken_image)
    assert is_broken is True, "Зламане зображення завантажилося успішно (naturalWidth > 0)"

# --- Блок тестів посилань ---


def test_valid_link_works(broken_page):
    broken_page.valid_link.click()
    # Чекаємо переходу
    broken_page.page.wait_for_load_state("networkidle")
    
    # Використовуємо скомпілований регулярний вираз. 
    # \. екранує крапку, щоб вона не означала "будь-який символ"
    # /? дозволяє посиланню закінчуватися на слеш або ні
       
    expect(broken_page.page).to_have_url(re.compile(r"https?://demoqa\.com/?"), timeout=10000)

def test_broken_link_returns_500_status(broken_page):
    """
    Це найцікавіший тест. Ми не просто клікаємо, а перехоплюємо відповідь сервера.
    Натискання на broken link має повернути статус 500.
    """
    # Створюємо контекстний менеджер для очікування відповіді від конкретного URL
    target_url = "http://the-internet.herokuapp.com/status_codes/500"
    
    with broken_page.page.expect_response(target_url) as response_info:
        broken_page.broken_link.click()
    
    response = response_info.value
    
    # Перевіряємо, що статус код дорівнює 500
    assert response.status == 500, f"Очікували статус 500, отримали {response.status}"
    # Додатково можна перевірити статус текст, якщо він є
    # assert response.status_text == "Internal Server Error"