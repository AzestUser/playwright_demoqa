import pytest
from playwright.sync_api import expect
from pages.buttons_page import ButtonsPage

@pytest.fixture
def buttons_page(page):
    page.set_viewport_size({"width": 1920, "height": 1080})
    bp = ButtonsPage(page)
    bp.navigate()
    return bp

def test_double_click_button(buttons_page):
    buttons_page.double_click()
    expect(buttons_page.double_click_msg).to_be_visible()
    expect(buttons_page.double_click_msg).to_have_text("You have done a double click")

def test_right_click_button(buttons_page):
    buttons_page.right_click()
    expect(buttons_page.right_click_msg).to_be_visible()
    expect(buttons_page.right_click_msg).to_have_text("You have done a right click")

def test_dynamic_click_button(buttons_page):
    buttons_page.click_dynamic()
    expect(buttons_page.dynamic_click_msg).to_be_visible()
    expect(buttons_page.dynamic_click_msg).to_have_text("You have done a dynamic click")