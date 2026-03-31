from playwright.sync_api import Page

class FramesPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://demoqa.com/frames"
        
        # Локатори для самих фреймів (за ID)
        self.frame1_selector = "#frame1"
        self.frame2_selector = "#frame2"
        
        # Локатор елемента ВСЕРЕДИНІ фрейму
        self.frame_heading = "#sampleHeading"

    def navigate(self):
        self.page.goto(self.url)

    def get_frame_heading_text(self, frame_id: str) -> str:
        """Повертає текст заголовка всередині вказаного фрейму"""
        # frame_locator() створює контекст усередині iframe
        return self.page.frame_locator(frame_id).locator(self.frame_heading).inner_text()