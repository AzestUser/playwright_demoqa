from playwright.sync_api import Page, Locator
import time

class SortablePage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://demoqa.com/sortable"
        self.tab_list = page.locator("#demo-tab-list")
        self.tab_grid = page.locator("#demo-tab-grid")
        self.list_items = page.locator("#demo-tabpane-list .list-group-item")
        self.grid_items = page.locator("#demo-tabpane-grid .list-group-item")

    def navigate(self):
        # 1. Змінюємо на "load" (завантаження основних ресурсів)
        self.page.goto(self.url, wait_until="load")
        
        # 2. Обов'язково чекаємо на появу конкретного елемента, щоб переконатися, що JS відпрацював
        self.tab_list.wait_for(state="visible", timeout=5000)
        
        # 3. Видаляємо сміття, яке може перекривати елементи або гальмувати сторінку
        self.page.evaluate("""
            const ads = document.querySelectorAll('#fixedban, footer, [id^="google_ads"]');
            ads.forEach(el => el.remove());
        """)

    def drag_and_drop_to_top(self, container_selector: str, item_text: str):
        source = self.page.locator(container_selector).get_by_text(item_text, exact=True)
        target = self.page.locator(container_selector).locator(".list-group-item").first

        source_box = source.bounding_box()
        target_box = target.bounding_box()

        if source_box and target_box:
            sx = source_box['x'] + source_box['width'] / 2
            sy = source_box['y'] + source_box['height'] / 2
            tx = target_box['x'] + target_box['width'] / 2
            ty = target_box['y'] + 2

            self.page.mouse.move(sx, sy)
            self.page.mouse.down()
            self.page.wait_for_timeout(100)

            # Поступово рухаємось до цілі через проміжну точку
            mx = (sx + tx) / 2
            my = (sy + ty) / 2
            self.page.mouse.move(mx, my, steps=5)
            self.page.wait_for_timeout(100)
            self.page.mouse.move(tx, ty, steps=5)
            self.page.wait_for_timeout(300)

            self.page.mouse.up()
            self.page.wait_for_timeout(300)

    def get_items_text(self, items_locator: Locator):
        # Переконуємось, що ми отримуємо актуальні дані з DOM
        return items_locator.all_inner_texts()