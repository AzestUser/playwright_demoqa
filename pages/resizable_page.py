from playwright.sync_api import Page

class ResizablePage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://demoqa.com/resizable"
        self.restricted_box = page.locator("#resizableBoxWithRestriction")
        self.restricted_handle = page.locator("#resizableBoxWithRestriction .react-resizable-handle")
        self.unrestricted_box = page.locator("#resizable")
        self.unrestricted_handle = page.locator("#resizable .react-resizable-handle")

    def navigate(self):
        self.page.goto(self.url, wait_until="load")
        self.page.evaluate("document.querySelectorAll('#fixedban, footer').forEach(el => el.remove())")

    def resize_element(self, handle_locator, target_width, target_height):
        """
        Виконуємо перетягування ручки зміни розміру.
        Обчислюємо цільову позицію всередині батьківського елемента
        і використовуємо drag_to для стабільного результату.
        """
        parent = handle_locator.locator("xpath=..")

        # Переконуємося, що і батьківський елемент, і ручка видимі у вікні
        parent.scroll_into_view_if_needed()
        handle_locator.scroll_into_view_if_needed()

        parent_box = parent.bounding_box()
        if not parent_box:
            raise RuntimeError("Не вдалося отримати розміри батьківського елемента для перетягування")

        handle_box = handle_locator.bounding_box()
        if not handle_box:
            raise RuntimeError("Не вдалося отримати розміри маніпулятора")

        # Розраховуємо позицію, куди треба перемістити ручку всередині контейнера
        target_x = target_width - handle_box["width"] / 2
        target_y = target_height - handle_box["height"] / 2

        handle_locator.drag_to(
            parent,
            target_position={"x": target_x, "y": target_y},
            force=True
        )

        # Коротка пауза для завершення обробки розміру
        self.page.wait_for_timeout(500)
