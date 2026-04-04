import random
from playwright.sync_api import Page

class SelectablePage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://demoqa.com/selectable"
        
        # Вкладки
        self.tab_list = page.get_by_role("tab", name="List")
        self.tab_grid = page.get_by_role("tab", name="Grid")
        
        # Елементи (локатори для кожної вкладки)
        self.list_items = page.locator("#verticalListContainer .list-group-item")
        self.grid_items = page.locator("#gridContainer .list-group-item")

    def navigate(self):
        self.page.goto(self.url, wait_until="load")
        self.page.evaluate("document.querySelectorAll('#fixedban, footer').forEach(el => el.remove())")

    def select_random_from(self, locator):
        """
        Універсальний метод для вибору рандомної кількості елементів 
        з будь-якого переданого локатора.
        """
        total_count = locator.count()
        k = random.randint(1, total_count)
        indices = random.sample(range(total_count), k)
        
        selected_texts = []
        for index in indices:
            item = locator.nth(index)
            selected_texts.append(item.inner_text())
            item.click()
            
        return selected_texts, k