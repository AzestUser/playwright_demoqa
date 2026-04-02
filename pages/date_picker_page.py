from playwright.sync_api import Page

class DatePickerPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://demoqa.com/date-picker"
        
        # Локатори для "Select Date"
        self.date_input = page.locator("#datePickerMonthYearInput")
        self.month_select = page.locator(".react-datepicker__month-select")
        self.year_select = page.locator(".react-datepicker__year-select")
        
        # Локатори для "Date And Time"
        self.date_time_input = page.locator("#dateAndTimePickerInput")
        self.dt_month_view = page.locator(".react-datepicker__month-read-view")
        self.dt_year_view = page.locator(".react-datepicker__year-read-view")
        self.time_list = page.locator(".react-datepicker__time-list-item")

    def navigate(self):
        # 1. Використовуємо "load" замість "networkidle"
        # "load" чекає лише завантаження основних ресурсів (HTML, JS, CSS)
        self.page.goto(self.url, wait_until="load")
        
        # 2. Чекаємо на появу конкретного елемента, щоб переконатися, що сторінка готова
        self.date_input.wait_for(state="visible")
        
        # 3. Видаляємо рекламу (безпечно)
        self.page.evaluate("""
            const banner = document.getElementById('fixedban');
            if (banner) banner.remove();
            const footer = document.querySelector('footer');
            if (footer) footer.remove();
        """)

    def select_date(self, day: str, month: str, year: str):
        """Вибір дати у першому віджеті (Select Date)"""
        self.date_input.click()
        self.month_select.select_option(label=month)
        self.year_select.select_option(value=year)
        
        # Форматуємо день (напр. "5" -> "005"), уникаємо днів поза межами місяця
        day_class = f".react-datepicker__day--{day.zfill(3)}:not(.react-datepicker__day--outside-month)"
        self.page.locator(day_class).click()

    def select_date_and_time(self, day: str, month: str, year: str, time: str):
        """Вибір дати та часу (Date and Time)"""
        self.date_time_input.click()
        
        # Вибір місяця (тут кастомний дропдаун, не <select>)
        self.dt_month_view.click()
        self.page.get_by_text(month, exact=True).click()
        
        # Вибір року
        self.dt_year_view.click()
        # Знаходимо потрібний рік у списку (може знадобитися скрол)
        year_item = self.page.locator(".react-datepicker__year-option", has_text=year)
        year_item.scroll_into_view_if_needed()
        year_item.click()
        
        # Вибір дня
        day_class = f".react-datepicker__day--{day.zfill(3)}:not(.react-datepicker__day--outside-month)"
        self.page.locator(day_class).click()
        
        # Вибір часу
        self.time_list.filter(has_text=time).click()