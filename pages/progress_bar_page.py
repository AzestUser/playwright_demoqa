from playwright.sync_api import Page

class ProgressBarPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://demoqa.com/progress-bar"
        
        # Локатори
        self.start_stop_button = page.locator("#startStopButton")
        self.progress_bar = page.locator("div[role='progressbar']")
        self.reset_button = page.locator("#resetButton")

    def navigate(self):
        self.page.goto(self.url, wait_until="load")
        # Безпечне видалення реклами
        self.page.evaluate("""
            document.getElementById('fixedban')?.remove();
            document.querySelector('footer')?.remove();
        """)

    def get_progress_value(self) -> int:
        """Отримує числове значення прогресу"""
        value = self.progress_bar.get_attribute("aria-valuenow")
        return int(value) if value else 0