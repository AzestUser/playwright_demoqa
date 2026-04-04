from playwright.sync_api import Page

class DroppablePage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://demoqa.com/droppable"
        
        # Вкладки
        self.tab_simple = page.locator("#droppableExample-tab-simple")
        self.tab_accept = page.locator("#droppableExample-tab-accept")
        self.tab_prevent = page.locator("#droppableExample-tab-preventPropogation")
        self.tab_revert = page.locator("#droppableExample-tab-revertable")
        
        # --- Елементи вкладки Simple ---
        self.simple_drag = page.locator("#draggable")
        self.simple_drop = page.locator("#simpleDropContainer #droppable")
        
        # --- Елементи вкладки Accept ---
        self.accept_drag = page.locator("#acceptable")
        self.not_accept_drag = page.locator("#acceptDropContainer .drag-box").nth(1)
        self.accept_drop = page.locator("#acceptDropContainer .drop-box")
        
        # --- Елементи вкладки Prevent Propogation ---
        self.prevent_drag = page.locator("#dragBox")
        self.not_greedy_outer = page.locator("#notGreedyDropBox")
        self.not_greedy_inner = page.locator("#notGreedyInnerDropBox")
        self.greedy_outer = page.locator("#greedyDropBox")
        self.greedy_inner = page.locator("#greedyDropBoxInner")
        
        # --- Елементи вкладки Revert Draggable ---
        self.revertable_drag = page.locator("#revertable")
        self.not_revertable_drag = page.locator("#notRevertable")
        self.revert_drop = page.locator("#revertableDropContainer #droppable")

    def navigate(self):
        self.page.goto(self.url, wait_until="load")
        self.page.wait_for_timeout(500)
        self.page.evaluate("document.querySelectorAll('#fixedban, footer').forEach(el => el.remove())")

    def drag_and_drop(self, source, target):
        """Стандартне перетягування через координати"""
        self.drag_by_coordinates(source, target)

    def drag_by_coordinates(self, source, target_locator, offset_x=0, offset_y=0):
        """jQuery UI drag via mouse events"""
        source_box = source.bounding_box()
        target_box = target_locator.bounding_box()
        sx = source_box['x'] + source_box['width'] / 2
        sy = source_box['y'] + source_box['height'] / 2
        tx = target_box['x'] + target_box['width'] / 2 + offset_x
        ty = target_box['y'] + target_box['height'] / 2 + offset_y

        self.page.mouse.move(sx, sy)
        self.page.mouse.down()
        self.page.wait_for_timeout(50)
        steps = 10
        for i in range(1, steps + 1):
            self.page.mouse.move(sx + (tx - sx) * i / steps, sy + (ty - sy) * i / steps)
            self.page.wait_for_timeout(20)
        self.page.mouse.up()
        self.page.wait_for_timeout(300)