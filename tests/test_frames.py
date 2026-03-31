import pytest
from playwright.sync_api import expect
from pages.frames_page import FramesPage

@pytest.fixture
def frames_page(page):
    p = FramesPage(page)
    p.navigate()
    return p

def test_frame1_content(frames_page):
    """Перевірка тексту у великому фреймі (Frame 1)"""
    text = frames_page.get_frame_heading_text(frames_page.frame1_selector)
    assert text == "This is a sample page"

def test_frame2_content(frames_page):
    """Перевірка тексту у маленькому фреймі (Frame 2)"""
    text = frames_page.get_frame_heading_text(frames_page.frame2_selector)
    assert text == "This is a sample page"

def test_frames_have_different_sizes(frames_page):
    """Перевірка, що фрейми мають різні розміри (візуальна відмінність)"""
    f1 = frames_page.page.locator(frames_page.frame1_selector)
    f2 = frames_page.page.locator(frames_page.frame2_selector)
    
    box1 = f1.bounding_box()
    box2 = f2.bounding_box()
    
    assert box1['width'] > box2['width']
    assert box1['height'] > box2['height']