from playwright.sync_api import Page

class TabsPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://demoqa.com/tabs"
        
        # Локатори вкладок (кнопки зверху)
        self.tab_what = page.locator("#demo-tab-what")
        self.tab_origin = page.locator("#demo-tab-origin")
        self.tab_use = page.locator("#demo-tab-use")
        self.tab_more = page.locator("#demo-tab-more")
        
        # Локатори контенту (текст під вкладками)
        self.pane_what = page.locator("#demo-tabpane-what")
        self.pane_origin = page.locator("#demo-tabpane-origin")
        self.pane_use = page.locator("#demo-tabpane-use")

    def navigate(self):
        self.page.goto(self.url, wait_until="load")
        # Прибираємо рекламу, щоб не заважала клікам
        self.page.evaluate("""
            document.getElementById('fixedban')?.remove();
            document.querySelector('footer')?.remove();
        """)