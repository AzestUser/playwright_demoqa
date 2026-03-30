import pytest
from playwright.sync_api import expect
from pages.links_page import LinksPage

@pytest.fixture
def links_page(page):
    page.set_viewport_size({"width": 1920, "height": 1080})
    lp = LinksPage(page)
    lp.navigate()
    return lp

def test_simple_link_opens_new_tab(links_page):
    # Використовуємо expect_popup, щоб перехопити нову вкладку
    with links_page.page.expect_popup() as popup_info:
        links_page.home_link.click()
    
    new_page = popup_info.value
    new_page.wait_for_load_state()
    
    # Перевіряємо URL нової сторінки
    expect(new_page).to_have_url("https://demoqa.com/")
    # Важливо закрити нову вкладку, щоб не засмічувати пам'ять
    new_page.close()

@pytest.mark.parametrize("link_name, expected_status, expected_text", [
    ("created", "201", "Created"),
    ("no_content", "204", "No Content"),
    ("moved", "301", "Moved Permanently"),
    ("bad_request", "400", "Bad Request"),
    ("unauthorized", "401", "Unauthorized"),
    ("forbidden", "403", "Forbidden"),
    ("not_found", "404", "Not Found"),
])
def test_api_links_status_codes(links_page, link_name, expected_status, expected_text):
    # Динамічно отримуємо локатор з об'єкта сторінки
    locator = getattr(links_page, f"{link_name}_link")
    
    links_page.click_api_link(locator)
    
    # Перевіряємо, що текст відповіді містить правильний код і опис
    expect(links_page.response_text).to_contain_text(expected_status)
    expect(links_page.response_text).to_contain_text(expected_text)