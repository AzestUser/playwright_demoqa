from playwright.sync_api import Page, expect

class BrowserWindowsPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://demoqa.com/browser-windows"
        
        # Кнопки
        self.new_tab_btn = page.locator("#tabButton")
        self.new_window_btn = page.locator("#windowButton")
        self.new_window_message_btn = page.locator("#messageWindowButton")
        
        # Заголовок на нових сторінках/вкладках
        self.sample_heading = page.locator("#sampleHeading")

    def navigate(self):
        self.page.goto(self.url)
        # Видаляємо рекламу для стабільності
        self.page.evaluate("""
            const ads = document.querySelectorAll('#adplus-anchor, #close-fixedban, footer, [id^="google_ads"]');
            ads.forEach(el => el.remove());
        """)

    def click_new_tab(self):
        """Клікає по кнопці New Tab та повертає об'єкт нової вкладки"""
        with self.page.expect_popup() as popup_info:
            self.new_tab_btn.click()
        return popup_info.value

    def click_new_window(self):
        """Клікає по кнопці New Window та повертає об'єкт нового вікна"""
        with self.page.expect_popup() as popup_info:
            self.new_window_btn.click()
        return popup_info.value

    def click_new_window_message(self):
        """
        Клікає по кнопці New Window Message та повертає об'єкт вікна.
        Увага: На DemoQA це вікно часто відкривається без тексту або з затримкою.
        """
        with self.page.expect_popup() as popup_info:
            self.new_window_message_btn.click()
        return popup_info.value