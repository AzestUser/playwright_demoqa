from playwright.sync_api import Page

class DraggablePage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://demoqa.com/dragabble"
        
        # Вкладки
        self.tab_simple = page.locator("#draggableExample-tab-simple")
        self.tab_axis = page.locator("#draggableExample-tab-axisRestriction")
        self.tab_container = page.locator("#draggableExample-tab-containerRestriction")
        self.tab_cursor = page.locator("#draggableExample-tab-cursorStyle")
        
        # --- Елементи Simple ---
        self.simple_drag = page.locator("#dragBox")
        
        # --- Елементи Axis Restricted ---
        self.only_x = page.locator("#restrictedX")
        self.only_y = page.locator("#restrictedY")
        
        # --- Елементи Container Restricted ---
        self.container_box = page.locator("#containmentWrapper")
        self.box_in_container = page.locator("#containmentWrapper .draggable")
        self.text_in_container = page.locator("#containmentWrapper").locator("xpath=..").locator(".draggable").last
        
        # --- Елементи Cursor Style ---
        self.cursor_center = page.locator("#cursorCenter")
        self.cursor_top_left = page.locator("#cursorTopLeft")
        self.cursor_bottom = page.locator("#cursorBottom")

    def navigate(self):
        self.page.goto(self.url, wait_until="load")
        self.page.wait_for_timeout(500)
        self.page.evaluate("document.querySelectorAll('#fixedban, footer').forEach(el => el.remove())")

    def drag_by_offset(self, locator, offset_x: int, offset_y: int):
        """
        Універсальний метод для зміщення елемента на певну кількість пікселів.
        """
        box = locator.bounding_box()
        if not box:
            raise Exception("Елемент не знайдено або він прихований")
            
        # Наводимо на центр елемента
        start_x = box['x'] + box['width'] / 2
        start_y = box['y'] + box['height'] / 2
        
        self.page.mouse.move(start_x, start_y)
        self.page.mouse.down()
        # Рухаємо на вказаний офсет
        self.page.mouse.move(start_x + offset_x, start_y + offset_y, steps=10)
        self.page.mouse.up()
        self.page.wait_for_timeout(200)