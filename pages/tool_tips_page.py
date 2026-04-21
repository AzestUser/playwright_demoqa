from playwright.sync_api import Page

class ToolTipsPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://demoqa.com/tool-tips"
        
        # Елементи-тригери
        self.button = page.locator("#toolTipButton")
        self.input_field = page.locator("#toolTipTextField")
        self.contrary_link = page.locator("#texToolTopContainer a").filter(has_text="Contrary")
        self.section_link = page.locator("#texToolTopContainer a").filter(has_text="1.10.32")
        
        # Сама підказка (з'являється динамічно)
        self.tooltip = page.locator(".tooltip-inner")

    def hover_and_wait_tooltip(self, locator):
        box = locator.bounding_box()
        self.page.mouse.move(
            box['x'] + box['width'] / 2,
            box['y'] + box['height'] / 2
        )
        self.page.wait_for_selector(".tooltip-inner", state="visible", timeout=8000)

    def navigate(self):
        self.page.goto(self.url, wait_until="load")
        # Видаляємо рекламу, щоб вона не перекривала елементи при наведенні
        self.page.evaluate("""
            document.getElementById('fixedban')?.remove();
            document.querySelector('footer')?.remove();
        """)