import pytest
from playwright.sync_api import expect
from pages.date_picker_page import DatePickerPage

@pytest.fixture
def date_page(page):
    p = DatePickerPage(page)
    p.navigate()
    return p

def test_select_date_simple(date_page):
    """Перевірка вибору звичайної дати"""
    date_page.select_date(day="15", month="July", year="1995")
    
    # Формат у полі після вибору: MM/DD/YYYY
    expect(date_page.date_input).to_have_value("07/15/1995")

def test_date_and_time_selection(date_page):
    """Перевірка вибору дати та конкретного часу"""
    # Обираємо дату та час 14:15
    date_page.select_date_and_time(day="20", month="May", year="2024", time="14:15")
    
    # Очікуваний формат: May 20, 2024 2:15 PM
    # Примітка: формат може залежати від локалі, DemoQA зазвичай використовує такий:
    expect(date_page.date_time_input).to_have_value("May 20, 2024 2:15 PM")

def test_default_values(date_page):
    """Перевірка, що за замовчуванням стоїть поточна дата"""
    import datetime
    now = datetime.datetime.now()
    expected_date = now.strftime("%m/%d/%Y")
    
    expect(date_page.date_input).to_have_value(expected_date)