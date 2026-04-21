import pytest
from playwright.sync_api import expect
from pages.tool_tips_page import ToolTipsPage

@pytest.fixture
def tt_page(page):
    p = ToolTipsPage(page)
    p.navigate()
    return p

def test_button_tooltip(tt_page):
    tt_page.hover_and_wait_tooltip(tt_page.button)
    expect(tt_page.tooltip).to_be_visible()
    expect(tt_page.tooltip).to_have_text("You hovered over the Button")

def test_input_tooltip(tt_page):
    tt_page.hover_and_wait_tooltip(tt_page.input_field)
    expect(tt_page.tooltip).to_be_visible()
    expect(tt_page.tooltip).to_have_text("You hovered over the text field")

def test_links_tooltips(tt_page):
    tt_page.hover_and_wait_tooltip(tt_page.contrary_link)
    expect(tt_page.tooltip).to_have_text("You hovered over the Contrary")
    
    tt_page.page.locator("h1").hover()
    expect(tt_page.tooltip).to_be_hidden()
    
    tt_page.hover_and_wait_tooltip(tt_page.section_link)
    expect(tt_page.tooltip).to_have_text("You hovered over the 1.10.32")
    
    tt_page.page.locator("h1").hover()
    expect(tt_page.tooltip).to_be_hidden()

def test_tooltip_disappears(tt_page):
    tt_page.hover_and_wait_tooltip(tt_page.button)
    expect(tt_page.tooltip).to_be_visible()
    
    tt_page.page.locator("h1").hover()
    expect(tt_page.tooltip).to_be_hidden()