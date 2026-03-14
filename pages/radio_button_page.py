from playwright.sync_api import Page, expect

"""
Page Object для сторінки Radio Button DemoQA: https://demoqa.com/radio-button

Містить логіку роботи з радіо-кнопками "Yes", "Impressive" і "No" і перевірку результату.
"""


class RadioButtonPage:
    def __init__(self, page: Page) -> None:
        self.page = page

        # Радіо-кнопки
        self.yes_radio = page.locator("#yesRadio")
        self.impressive_radio = page.locator("#impressiveRadio")
        self.no_radio = page.locator("#noRadio")

        # Текст результату після вибору (повинен бути .text-success)
        self.selected_result = page.locator(".text-success")

    def goto(self) -> None:
        """Відкриває сторінку Radio Button."""
        self.page.goto("https://demoqa.com/radio-button")

    def wait_loaded(self) -> None:
        """Чекає появи робочого елемента на сторінці."""
        expect(self.yes_radio).to_be_visible()

    def select_yes(self) -> None:
        """Вибирає варіант Yes."""
        self.yes_radio.click()

    def select_impressive(self) -> None:
        """Вибирає варіант Impressive."""
        self.impressive_radio.click()

    def select_no(self) -> None:
        """Переважно для перевірки стану No (заблокований стан)."""
        self.no_radio.click()

    def select(self, option: str) -> None:
        """Обирає радіо-кнопку за назвоюопції: Yes / Impressive / No."""
        label = option.strip().lower()
        if label == "yes":
            self.select_yes()
        elif label == "impressive":
            self.select_impressive()
        elif label == "no":
            self.select_no()
        else:
            raise ValueError(f"Невідома опція радіо-кнопки: {option}")

    def get_selected_text(self) -> str:
        """Повертає text-success (значення вибраної кнопки)."""
        return self.selected_result.text_content().strip()

    def expect_selected(self, value: str) -> None:
        """Перевіряє, що в результаті видно обране значення."""
        expect(self.selected_result).to_have_text(value)
