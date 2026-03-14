from playwright.sync_api import Page

from pages.radio_button_page import RadioButtonPage


def test_radio_button_yes(page: Page) -> None:
    """Перевіряємо вибір Yes у Radio Button."""
    radio = RadioButtonPage(page)
    radio.goto()
    radio.wait_loaded()

    radio.select_yes()
    radio.expect_selected("Yes")


def test_radio_button_impressive(page: Page) -> None:
    """Перевіряємо вибір Impressive у Radio Button."""
    radio = RadioButtonPage(page)
    radio.goto()
    radio.wait_loaded()

    radio.select_impressive()
    radio.expect_selected("Impressive")


def test_radio_button_no_disabled(page: Page) -> None:
    """Перевіряємо, що No радіо-кнопка недоступна (disabled)."""
    radio = RadioButtonPage(page)
    radio.goto()
    radio.wait_loaded()

    assert radio.no_radio.is_disabled()
