import pytest
from playwright.sync_api import Page
# ОСЬ ЦЕЙ ІМПОРТ МАЄ БУТИ ОБОВ'ЯЗКОВО:
from pages.check_box_page import CheckBoxPage


def test_select_single_checkbox(page):
    check_box_page = CheckBoxPage(page)
    check_box_page.navigate()

    # Послідовно розгортаємо шлях до Notes
    check_box_page.expand_node("Home")
    check_box_page.expand_node("Desktop")
    
    # Тепер вибираємо чекбокс
    check_box_page.select_checkbox("Notes")
    
    # Валідуємо результат
    check_box_page.expect_result_to_contain("notes")

def test_complex_selection(page: Page):
    cb = CheckBoxPage(page)
    cb.navigate()

    # Розгортаємо дерево до файлу Excel
    cb.expand_node("Home")
    cb.expand_node("Downloads")
    
    # Вибираємо файл (використовуємо точне ім'я з aria-label)
    cb.select_checkbox("Excel File.doc")
    
    # Перевіряємо результат (в DOM це excelFile)
    cb.expect_selected("excelFile")