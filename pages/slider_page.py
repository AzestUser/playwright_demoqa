from playwright.sync_api import Page

class SliderPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://demoqa.com/slider"
        
        # Локатор самого повзунка (input)
        self.slider = page.locator(".range-slider")
        # Локатор текстового поля, що відображає поточне значення
        self.slider_value_input = page.locator("#sliderValue")

    def navigate(self):
        # Використовуємо стабільний варіант завантаження
        self.page.goto(self.url, wait_until="load")
        self.remove_ads()
        self.slider.wait_for(state="visible")

    def remove_ads(self):
        self.page.evaluate("""
            const ads = document.querySelectorAll('#fixedban, footer');
            ads.forEach(ad => ad.remove());
        """)

    def set_slider_value(self, value: int):
        """Встановлює значення слайдера через метод fill"""
        # Playwright fill() для input[type=range] працює коректно в більшості випадків
        self.slider.fill(str(value))