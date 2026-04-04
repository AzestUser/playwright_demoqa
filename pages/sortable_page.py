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
        """
        Бере елемент за текстом і тягне його на саму першу позицію контейнера.
        """
        source = self.page.locator(container_selector).get_by_text(item_text, exact=True)
        # Ціль — завжди перший елемент у поточному стані списку
        target = self.page.locator(container_selector).locator(".list-group-item").first
        
        # Отримуємо координати
        source_box = source.bounding_box()
        target_box = target.bounding_box()

        if source_box and target_box:
            # 1. Наводимо на центр елемента, який хочемо перетягнути
            self.page.mouse.move(source_box['x'] + source_box['width'] / 2, 
                                 source_box['y'] + source_box['height'] / 2)
            self.page.mouse.down()
            
            # 2. Тягнемо до верхньої частини цільового елемента
            # Додаємо невеликий офсет (-5), щоб бути точно над ним
            self.page.mouse.move(target_box['x'] + target_box['width'] / 2, 
                                 target_box['y'] + 5, steps=10)
            
            # КРИТИЧНО: невелика пауза, щоб SortableJS побачив перекриття
            self.page.wait_for_timeout(300)
            
            self.page.mouse.up()
            # Чекаємо завершення анімації переміщення в DOM
            self.page.wait_for_timeout(200)

    def get_items_text(self, items_locator: Locator):
        # Переконуємось, що ми отримуємо актуальні дані з DOM
        return items_locator.all_inner_texts()