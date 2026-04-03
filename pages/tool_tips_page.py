from playwright.sync_api import Page

class ToolTipsPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://demoqa.com/tool-tips"
        
        # Елементи-тригери
        self.button = page.locator("#toolTipButton")
        self.input_field = page.locator("#toolTipTextField")
        self.contrary_link = page.get_by_text("Contrary", exact=False)
        self.section_link = page.get_by_text("1.10.32", exact=False)
        
        # Сама підказка (з'являється динамічно)
        self.tooltip = page.locator(".tooltip-inner >> visible=true")

    def navigate(self):
        self.page.goto(self.url, wait_until="load")
        # Видаляємо рекламу, щоб вона не перекривала елементи при наведенні
        self.page.evaluate("""
            document.getElementById('fixedban')?.remove();
            document.querySelector('footer')?.remove();
        """)