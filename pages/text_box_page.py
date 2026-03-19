from playwright.sync_api import Page, expect

class TextBoxPage:
    def __init__(self, page: Page):
        self.page = page
        # Локатори елементів
        self.full_name_input = page.get_by_placeholder("Full Name")
        self.email_input = page.get_by_placeholder("name@example.com")
        self.current_address_input = page.get_by_placeholder("Current Address")
        self.permanent_address_textarea = page.locator("#permanentAddress")
        self.submit_button = page.locator("#submit")
        
        # Локатори результатів (output block)
        self.output_name = page.locator("#name")
        self.output_email = page.locator("#email")
        self.output_current_address = page.locator("p#currentAddress")
        self.output_permanent_address = page.locator("p#permanentAddress")

    def navigate(self):
        """Відкрити сторінку Text Box"""
        self.page.goto("https://demoqa.com/text-box")

    def fill_form(self, name: str, email: str, current_addr: str, permanent_addr: str):
        """Заповнити всі поля форми"""
        self.full_name_input.fill(name)
        self.email_input.fill(email)
        self.current_address_input.fill(current_addr)
        self.permanent_address_textarea.fill(permanent_addr)

    def submit(self):
        """Натиснути кнопку Submit"""
        self.submit_button.click()

    def check_output_data(self, name: str, email: str, current_addr: str, permanent_addr: str):
        """Перевірити, чи відображаються коректні дані після сабміту"""
        expect(self.output_name).to_contain_text(f"Name:{name}")
        expect(self.output_email).to_contain_text(f"Email:{email}")
        expect(self.output_current_address).to_contain_text(f"Current Address :{current_addr}")
        expect(self.output_permanent_address).to_contain_text(f"Permananet Address :{permanent_addr}")