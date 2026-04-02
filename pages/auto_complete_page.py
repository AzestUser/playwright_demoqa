from playwright.sync_api import Page

class AutoCompletePage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://demoqa.com/auto-complete"
        
        # Локатори полів вводу
        self.multiple_input = page.locator("#autoCompleteMultipleInput")
        self.single_input = page.locator("#autoCompleteSingleInput")
        
        # Локатор для меню підказок (з'являється динамічно)
        self.suggestion_menu = page.locator(".auto-complete__menu")
        self.suggestion_option = page.locator(".auto-complete__option")
        
        # Локатори вибраних значень
        self.multiple_values = page.locator(".auto-complete__multi-value__label")
        self.single_value = page.locator(".auto-complete__single-value")
        
        # Кнопки видалення (хрестики)
        self.remove_value_btn = page.locator(".auto-complete__multi-value__remove")

    def navigate(self):
        self.page.goto(self.url)
        self.remove_ads()

    def remove_ads(self):
        self.page.evaluate("""
            const ads = document.querySelectorAll('#fixedban, footer');
            ads.forEach(ad => ad.style.display = 'none');
        """)

    def fill_and_select(self, input_locator, text: str, color_to_select: str):
        """Вводить текст і вибирає конкретний колір із запропонованих"""
        input_locator.fill(text)
        # Чекаємо на появу меню та клікаємо по потрібному кольору
        self.suggestion_option.filter(has_text=color_to_select).click()