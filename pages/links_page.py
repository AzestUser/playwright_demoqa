from playwright.sync_api import Page, expect

class LinksPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://demoqa.com/links"
        
        # Посилання, що відкриваються в новій вкладці
        self.home_link = page.locator("#simpleLink")
        self.dynamic_home_link = page.locator("#dynamicLink")
        
        # Посилання для API-запитів
        self.created_link = page.locator("#created")
        self.no_content_link = page.locator("#no-content")
        self.moved_link = page.locator("#moved")
        self.bad_request_link = page.locator("#bad-request")
        self.unauthorized_link = page.locator("#unauthorized")
        self.forbidden_link = page.locator("#forbidden")
        self.not_found_link = page.locator("#invalid-url")
        
        # Поле з відповіддю
        self.response_text = page.locator("#linkResponse")

    def navigate(self):
        self.page.goto(self.url)
        # Традиційне "прибирання" реклами
        self.page.evaluate("""
            const ads = document.querySelectorAll('#adplus-anchor, #close-fixedban, footer, [id^="google_ads"]');
            ads.forEach(el => el.remove());
        """)

    def click_api_link(self, link_locator):
        """Клікає по лінці та чекає, поки текст відповіді оновиться"""
        link_locator.click()
        # Чекаємо, поки в елементі з'явиться хоч якийсь текст (статус)
        expect(self.response_text).to_be_visible()