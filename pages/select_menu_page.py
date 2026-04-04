from playwright.sync_api import Page

class SelectMenuPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://demoqa.com/select-menu"
        # У конструкторі __init__ вашого SelectMenuPage додайте цей локатор:
        self.multi_container = page.locator("#react-select-4-input").locator("xpath=ancestor::div[contains(@class,'container')][1]")
        
        # 1. Custom "Select Value" (React)
        self.value_dropdown = page.locator("#withOptGroup")
        
        # 2. Custom "Select One" (React)
        self.title_dropdown = page.locator("#selectOne")
        
        # 3. Standard HTML Select
        self.standard_select = page.locator("#oldSelectMenu")
        
        # 4. Multi Select Dropdown
        self.multi_select_input = page.locator("#react-select-4-input")

    def navigate(self):
        self.page.goto(self.url, wait_until="load")
        self.page.evaluate("""
            document.getElementById('fixedban')?.remove();
            document.querySelector('footer')?.remove();
        """)