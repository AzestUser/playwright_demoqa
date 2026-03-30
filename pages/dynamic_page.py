from playwright.sync_api import Page

class DynamicPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://demoqa.com/dynamic-properties"
        
        # Елемент з рандомним ID (шукаємо по тексту, бо ID змінюється кожного разу)
        self.random_id_text = page.get_by_text("This text has random Id")
        
        # Кнопка, що активується через 5 секунд
        self.enable_after_btn = page.locator("#enableAfter")
        
        # Кнопка, що змінює колір тексту
        self.color_change_btn = page.locator("#colorChange")
        
        # Кнопка, що з'являється через 5 секунд
        self.visible_after_btn = page.locator("#visibleAfter")

    def navigate(self):
        self.page.goto(self.url)
        # Очищуємо рекламу, щоб не заважала таймерам
        self.page.evaluate("document.querySelectorAll('[id^=\"google_ads\"]').forEach(el => el.remove())")