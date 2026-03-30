import os
from playwright.sync_api import Page

class UploadDownloadPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://demoqa.com/upload-download"
        
        # Локатори
        self.download_button = page.locator("#downloadButton")
        self.upload_input = page.locator("#uploadFile")
        self.uploaded_path_text = page.locator("#uploadedFilePath")

    def navigate(self):
        self.page.goto(self.url)
        # Видаляємо рекламу, щоб не перекривала кнопки
        self.page.evaluate("document.querySelectorAll('[id^=\"google_ads\"]').forEach(el => el.remove())")

    def trigger_download(self):
        """Запускає процес завантаження та повертає об'єкт завантаження"""
        with self.page.expect_download() as download_info:
            self.download_button.click()
        return download_info.value

    def upload_file(self, file_path: str):
        """Завантажує файл у вказаний input"""
        self.upload_input.set_input_files(file_path)