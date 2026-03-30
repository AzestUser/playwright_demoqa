from playwright.sync_api import Page, expect

class BrokenPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://demoqa.com/broken"
        
        # Локатори зображень
        # Використовуємо комбінацію тегу та src, щоб точно знайти потрібні картинки
        self.valid_image = page.locator('img[src="/images/Toolsqa.jpg"]')
        self.broken_image = page.locator('img[src="/images/Toolsqa_1.jpg"]')
        
        # Локатори посилань по тексту
        self.valid_link = page.get_by_role("link", name="Click Here for Valid Link")
        self.broken_link = page.get_by_role("link", name="Click Here for Broken Link")

    def navigate(self):
        self.page.goto(self.url)
        # Традиційне видалення реклами
        self.page.evaluate("""
            const ads = document.querySelectorAll('#adplus-anchor, #close-fixedban, footer, [id^="google_ads"]');
            ads.forEach(el => el.remove());
        """)

    def is_image_broken(self, image_locator):
        # Чекаємо, поки картинка з'явиться в DOM
        image_locator.wait_for(state="visible", timeout=5000)
        
        # Перевіряємо через JS, чи вона завантажена
        return image_locator.evaluate("""
            element => !element.complete || 
            typeof element.naturalWidth === 'undefined' || 
            element.naturalWidth === 0
        """)