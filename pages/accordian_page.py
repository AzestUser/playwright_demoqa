from playwright.sync_api import Page

class AccordianPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://demoqa.com/accordian"
        self.root_accordion = page.locator("div.accordion").nth(1)

        # Локатори заголовків
        self.section1_heading = self.root_accordion.locator(".accordion-button").nth(0)
        self.section2_heading = self.root_accordion.locator(".accordion-button").nth(1)
        self.section3_heading = self.root_accordion.locator(".accordion-button").nth(2)

        # Локатори контенту (тіла секцій)
        self.section1_content = self.root_accordion.locator(".accordion-collapse").nth(0)
        self.section2_content = self.root_accordion.locator(".accordion-collapse").nth(1)
        self.section3_content = self.root_accordion.locator(".accordion-collapse").nth(2)

    def navigate(self):
        self.page.goto(self.url)
        self.page.wait_for_selector("div.accordion")

    def expand_section(self, section_number: int):
        """Натискає на заголовок секції за номером (1, 2 або 3)"""
        headings = {
            1: self.section1_heading,
            2: self.section2_heading,
            3: self.section3_heading
        }
        headings[section_number].click()