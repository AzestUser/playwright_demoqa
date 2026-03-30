from playwright.sync_api import Page, expect

class ButtonsPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://demoqa.com/buttons"
        
        # Локатори для кнопок
        self.double_click_btn = page.locator("#doubleClickBtn")
        self.right_click_btn = page.locator("#rightClickBtn")
        # Остання кнопка не має постійного ID, тому шукаємо по тексту з точним збігом
        self.dynamic_click_btn = page.get_by_role("button", name="Click Me", exact=True)
        
        # Локатори для повідомлень про успіх
        self.double_click_msg = page.locator("#doubleClickMessage")
        self.right_click_msg = page.locator("#rightClickMessage")
        self.dynamic_click_msg = page.locator("#dynamicClickMessage")

    def navigate(self):
        self.page.goto(self.url)
        # Прибираємо рекламу, щоб вона не перехоплювала кліки
        self.page.evaluate("""
            const ads = document.querySelectorAll('#adplus-anchor, #close-fixedban, footer, [id^="google_ads"]');
            ads.forEach(el => el.remove());
        """)

    def double_click(self):
        self.double_click_btn.dblclick()

    def right_click(self):
        self.right_click_btn.click(button="right")

    def click_dynamic(self):
        self.dynamic_click_btn.click()