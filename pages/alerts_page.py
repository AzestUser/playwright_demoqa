from playwright.sync_api import Page

class AlertsPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://demoqa.com/alerts"
        
        # Локатори кнопок
        self.alert_btn = page.locator("#alertButton")
        self.timer_alert_btn = page.locator("#timerAlertButton")
        self.confirm_btn = page.locator("#confirmButton")
        self.prompt_btn = page.locator("#promtButton")
        
        # Локатори результатів
        self.confirm_result = page.locator("#confirmResult")
        self.prompt_result = page.locator("#promptResult")

    def navigate(self):
        self.page.goto(self.url)

    def handle_dialog(self, action="accept", prompt_text=None):
        """
        Універсальний обробник для діалогів.
        action: "accept" або "dismiss"
        """
        def on_dialog(dialog):
            if prompt_text:
                dialog.accept(prompt_text)
            elif action == "accept":
                dialog.accept()
            else:
                dialog.dismiss()

        # Підписуємося на подію діалогу один раз
        self.page.once("dialog", on_dialog)