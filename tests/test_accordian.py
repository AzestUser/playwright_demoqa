import pytest
from playwright.sync_api import expect
from pages.accordian_page import AccordianPage

@pytest.fixture
def accordian_page(page):
    p = AccordianPage(page)
    p.navigate()
    return p

def test_initial_state(accordian_page):
    """Перевірка початкового стану: перша секція відкрита, інші закриті"""
    # Перша секція має бути видимою за замовчуванням
    expect(accordian_page.section1_content).to_be_visible()
    expect(accordian_page.section1_content).to_contain_text("Lorem Ipsum is simply dummy text")
    
    # Інші мають бути приховані
    expect(accordian_page.section2_content).to_be_hidden()
    expect(accordian_page.section3_content).to_be_hidden()

def test_expand_second_section(accordian_page):
    """Перевірка розкриття другої секції та автоматичного закриття першої"""
    accordian_page.expand_section(2)
    
    # Тепер друга секція видима
    expect(accordian_page.section2_content).to_be_visible()
    expect(accordian_page.section2_content).to_contain_text("Hampden-Sydney College in Virginia")
    
    # Перша повинна автоматично згорнутися
    expect(accordian_page.section1_content).to_be_hidden()

def test_expand_third_section(accordian_page):
    """Перевірка розкриття третьої секції"""
    accordian_page.expand_section(3)
    
    expect(accordian_page.section3_content).to_be_visible()
    expect(accordian_page.section3_content).to_contain_text("It is a long established fact that a reader")
    
    # Перевіряємо, що інші згорнуті
    expect(accordian_page.section1_content).to_be_hidden()
    expect(accordian_page.section2_content).to_be_hidden()

def test_toggle_same_section(accordian_page):
    """Перевірка згортання вже відкритої секції (натискаємо ще раз на першу)"""
    # Спочатку вона відкрита
    expect(accordian_page.section1_content).to_be_visible()
    
    # Натискаємо, щоб закрити
    accordian_page.expand_section(1)
    
    # Тепер вона має бути прихована
    expect(accordian_page.section1_content).to_be_hidden()