from playwright.sync_api import Page

class NestedFramesPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://demoqa.com/nestedframes"
        
        # 1. Локатор батьківського фрейму (Parent)
        self.parent_frame = page.frame_locator("#frame1")
        
        # 2. Локатор дочірнього фрейму (Child), який шукаємо ВСЕРЕДИНІ батьківського
        # На DemoQA у вкладеного фрейму немає ID, тому шукаємо за тегом 'iframe'
        self.child_frame = self.parent_frame.frame_locator("iframe")
        
        # Локатори тексту
        self.parent_text = self.parent_frame.locator("body")
        self.child_text = self.child_frame.locator("p")

    def navigate(self):
        self.page.goto(self.url)