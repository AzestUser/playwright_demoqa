from playwright.sync_api import Page

class ModalDialogsPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://demoqa.com/modal-dialogs"
        
        # Кнопки для відкриття
        self.show_small_modal_btn = page.locator("#showSmallModal")
        self.show_large_modal_btn = page.locator("#showLargeModal")
        
        # Елементи модалок (вони з'являються динамічно)
        self.modal_content = page.locator(".modal-content")
        self.modal_title = page.locator(".modal-title")
        self.modal_body = page.locator(".modal-body")
        
        # Кнопки закриття
        self.close_small_modal_btn = page.locator("#closeSmallModal")
        self.close_large_modal_btn = page.locator("#closeLargeModal")

    def navigate(self):
        self.page.goto(self.url)

    def open_small_modal(self):
        self.show_small_modal_btn.click()

    def open_large_modal(self):
        self.show_large_modal_btn.click()