from playwright.sync_api import Page, expect

# Об'єкт сторінки для роботи зі сторінкою Web Tables на DemoQA.
class WebTablesPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://demoqa.com/webtables"
        
        # Селектори для керування таблицею
        self.add_button = page.locator("#addNewRecordButton")
        self.search_input = page.locator("#searchBox")
        self.table_body = page.locator("table tbody")
        self.table_rows = page.locator("table tbody tr")
        
        # Поля форми для додавання / редагування запису
        self.first_name_input = page.locator("#firstName")
        self.last_name_input = page.locator("#lastName")
        self.email_input = page.locator("#userEmail")
        self.age_input = page.locator("#age")
        self.salary_input = page.locator("#salary")
        self.department_input = page.locator("#department")
        self.submit_button = page.locator("#submit")

    def navigate(self):
        # Відкриваємо сторінку Web Tables і чекаємо появи таблиці.
        self.page.goto(self.url)
        # Прибираємо рекламу та зайві елементи, щоб вони не перекривали елементи сторінки.
        self.page.evaluate("""
            const selectors = ['#adplus-anchor', '#close-fixedban', 'footer', '[id^="google_ads"]'];
            selectors.forEach(sel => {
                const el = document.querySelector(sel);
                if (el) el.remove();
            });
        """)
        expect(self.table_body).to_be_visible(timeout=10000)

    def add_new_record(self, first_name, last_name, email, age, salary, department):
        # Відкриваємо форму додавання запису та заповнюємо поля.
        self.add_button.click()
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.email_input.fill(email)
        self.age_input.fill(str(age))
        self.salary_input.fill(str(salary))
        self.department_input.fill(department)
        self.submit_button.click()
        # Чекаємо, поки вікно форми закриється, і перевіряємо, що запис додано.
        expect(self.page.locator(".modal-content")).to_be_hidden(timeout=10000)
        expect(self.get_row_by_email(email)).to_be_visible(timeout=10000)

    def delete_record_by_email(self, email: str):
        # Знаходимо рядок за email і натискаємо кнопку видалення.
        row = self.get_row_by_email(email)
        delete_button = row.locator('span[title="Delete"]')
        delete_button.click()
        expect(row).to_be_hidden(timeout=10000)
        expect(self.table_body).not_to_contain_text(email, timeout=10000)

    def edit_record_by_email(
        self,
        email: str,
        first_name: str | None = None,
        last_name: str | None = None,
        age: int | None = None,
        salary: int | None = None,
        department: str | None = None,
    ):
        # Знаходимо рядок за email та відкриваємо форму редагування.
        row = self.get_row_by_email(email)
        edit_button = row.locator('span[title="Edit"]')
        edit_button.click()

        # Заповнюємо тільки передані поля, залишаємо інші без змін.
        if first_name is not None:
            self.first_name_input.fill(first_name)
        if last_name is not None:
            self.last_name_input.fill(last_name)
        if age is not None:
            self.age_input.fill(str(age))
        if salary is not None:
            self.salary_input.fill(str(salary))
        if department is not None:
            self.department_input.fill(department)

        self.submit_button.click()
        expect(self.page.locator(".modal-content")).to_be_hidden(timeout=10000)
        expect(self.get_row_by_email(email)).to_be_visible(timeout=10000)

    def clear_search(self):
        # Очищення пошукового поля, щоб повернутися до повного списку записів.
        self.search_input.wait_for(state="visible")
        self.search_input.fill("")
        expect(self.search_input).to_have_value("")
        self.page.wait_for_timeout(500)

    def search_record(self, text: str):
        # Виконуємо пошук по тексту і чекаємо, поки поле оновиться.
        self.search_input.wait_for(state="visible")
        self.search_input.fill(text)
        expect(self.search_input).to_have_value(text, timeout=5000)
        self.page.wait_for_timeout(500)

    def get_row_by_email(self, email: str):
        # Повертаємо рядок таблиці, який містить цей email.
        return self.page.get_by_text(email, exact=True).locator("xpath=ancestor::tr")