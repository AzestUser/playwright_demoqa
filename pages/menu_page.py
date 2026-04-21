from playwright.sync_api import Page

class MenuPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://demoqa.com/menu"
        
        # Основні пункти
        self.main_item_1 = page.get_by_role("link", name="Main Item 1")
        self.main_item_2 = page.get_by_role("link", name="Main Item 2")
        self.main_item_3 = page.get_by_role("link", name="Main Item 3")
        
        # Підпункти (з'являються при наведенні на Main Item 2)
        self.sub_sub_list = page.locator("#nav > li:nth-child(2) > ul")
        self.sub_sub_list_link = page.get_by_role("link", name="SUB SUB LIST »")
        
        # Глибокі підпункти (з'являються при наведенні на SUB SUB LIST)
        self.sub_sub_item_1 = page.get_by_role("link", name="Sub Sub Item 1")
        self.sub_sub_item_2 = page.get_by_role("link", name="Sub Sub Item 2")

    def navigate(self):
        self.page.goto(self.url, wait_until="load")
        self.page.evaluate("""
            document.getElementById('fixedban')?.remove();
            document.querySelector('footer')?.remove();
        """)

    def hover_chain(self, *locators):
        """Відкриває підменю через пряме змінення CSS display на вкладених <ul>"""
        for locator in locators:
            locator.evaluate("""
                el => {
                    const ul = el.nextElementSibling;
                    if (ul && ul.tagName === 'UL') ul.style.display = 'block';
                }
            """)
            self.page.wait_for_timeout(200)

    def close_submenu(self):
        """Закриває всі підменю через hover на body (симулює прибирання курсору)"""
        self.page.locator("body").hover()
        self.page.wait_for_timeout(200)