import os
from playwright.sync_api import Page, expect

class PracticeFormPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://demoqa.com/automation-practice-form"
        
        # Основні поля
        self.first_name = page.locator("#firstName")
        self.last_name = page.locator("#lastName")
        self.email = page.locator("#userEmail")
        self.mobile = page.locator("#userNumber")
        self.current_address = page.locator("#currentAddress")
        
        # Календар
        self.date_of_birth_input = page.locator("#dateOfBirthInput")
        self.month_select = page.locator(".react-datepicker__month-select")
        self.year_select = page.locator(".react-datepicker__year-select")
        
        # Спеціальні випадаючі списки (React-Select)
        self.subjects_input = page.locator("#subjectsInput")
        self.state_dropdown = page.locator("#state")
        self.city_dropdown = page.locator("#city")
        
        # Інші елементи
        self.file_upload = page.locator("#uploadPicture")
        self.submit_button = page.locator("#submit")
        
        # Модалка підтвердження
        self.modal_title = page.locator("#example-modal-sizes-title-lg")
        self.modal_table = page.locator(".table-responsive")
        self.close_modal_btn = page.locator("#closeLargeModal")

    def navigate(self):
        self.page.goto(self.url)
        self.page.evaluate("""
            document.querySelectorAll('#adplus-anchor, #close-fixedban, footer, #fixedban, [id^="google_ads"]').forEach(el => el.remove());
        """)

    def select_gender(self, gender: str):
        self.page.locator("#genterWrapper").get_by_text(gender, exact=True).click()

    def select_hobby(self, hobby: str):
        self.page.locator("#hobbiesWrapper").get_by_text(hobby, exact=True).click()

    def fill_date_of_birth(self, day: str, month: str, year: str):
        self.date_of_birth_input.click()
        self.month_select.select_option(label=month)
        self.year_select.select_option(value=year)
        formatted_day = day.zfill(3)
        selector = f".react-datepicker__day--{formatted_day}:not(.react-datepicker__day--outside-month)"
        self.page.locator(selector).click()

    def fill_subjects(self, subjects: list):
        for subject in subjects:
            self.subjects_input.fill(subject)
            option = self.page.locator("[class*='option']")
            option.first.wait_for(state="visible")
            option.first.click()

    def select_state_and_city(self, state: str, city: str):
        # React-Select на DemoQA не є стандартним селектом, тому взаємодіємо через клік + текст
        self.state_dropdown.click()
        self.page.get_by_text(state, exact=True).click()
        
        self.city_dropdown.click()
        self.page.get_by_text(city, exact=True).click()

    def upload_picture(self, file_path: str):
        self.file_upload.set_input_files(file_path)

    def submit_form(self):
        # Іноді кнопка перекривається футером, тому використовуємо scroll
        self.submit_button.scroll_into_view_if_needed()
        self.submit_button.click()