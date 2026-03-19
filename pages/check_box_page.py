from playwright.sync_api import Page, expect

class CheckBoxPage:
    def __init__(self, page: Page):
        self.page = page
        self.result_text = page.locator("#result")

    def navigate(self):
        """Відкрити сторінку та чекати на дерево."""
        self.page.goto("https://demoqa.com/checkbox")
        self.page.wait_for_selector(".rc-tree", timeout=15000)

    def expand_node(self, node_name: str):
        """
        Знаходить treeitem за назвою і розгортає його, якщо він закритий.
        Використовує aria-expanded, що є найнадійнішим способом для rc-tree.
        """
        # Шукаємо конкретний treeitem за його назвою (атрибут title або текст)
        node = self.page.locator("div[role='treeitem']").filter(has_text=node_name).first
        
        # Перевіряємо стан через aria-expanded
        if node.get_attribute("aria-expanded") == "false":
            # Клікаємо по світчеру (стрілочці). 
            # Навіть якщо клас rc-tree-switcher_close, ми просто беремо базовий клас.
            node.locator(".rc-tree-switcher").click()
            # Маленька пауза, щоб React встиг відрендерити вкладені елементи
            self.page.wait_for_timeout(300)

    def select_checkbox(self, item_name: str):
        """
        Клікає по чекбоксу елемента.
        Використовує aria-label, який є у твоєму коді: aria-label='Select [Name]'
        """
        # Це найбільш точний шлях, бо aria-label містить назву елемента
        checkbox = self.page.get_by_role("checkbox", name=f"Select {item_name}")
        checkbox.click()

    def expect_result_to_contain(self, text: str):
        """
        Перевіряє, чи з'явився текст у блоці результатів.
        Параметр 'text' — це очікувана назва (наприклад, 'notes').
        """
        # Чекаємо, поки блок з результатами стане видимим
        self.result_text.wait_for(state="visible", timeout=5000)
        # Перевіряємо наявність тексту
        expect(self.result_text).to_contain_text(text)

    def expect_selected(self, item_id: str):
        """
        Перевіряє, чи з'явився текст у блоці результатів.
        Зверни увагу: в результатах назви часто пишуться з маленької літери (notes, excelFile).
        """
        expect(self.result_text).to_contain_text(item_id)