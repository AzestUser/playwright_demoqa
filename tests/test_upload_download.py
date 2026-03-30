import os
import pytest
from playwright.sync_api import expect
from pages.upload_download_page import UploadDownloadPage

@pytest.fixture
def up_down_page(page):
    page.set_viewport_size({"width": 1920, "height": 1080})
    p = UploadDownloadPage(page)
    p.navigate()
    return p

def test_download_file(up_down_page, tmp_path):
    # 1. Трігеримо завантаження
    download = up_down_page.trigger_download()
    
    # 2. Перевіряємо ім'я файлу (воно має бути sampleFile.jpeg на DemoQA)
    assert download.suggested_filename == "sampleFile.jpeg"
    
    # 3. Зберігаємо файл у тимчасову папку pytest (tmp_path)
    download_path = tmp_path / download.suggested_filename
    download.save_as(download_path)
    
    # 4. Перевіряємо, що файл дійсно існує на диску
    assert os.path.exists(download_path)

def test_upload_file(up_down_page, tmp_path):
    # 1. Створюємо фіктивний файл для завантаження
    test_file = tmp_path / "test_upload.txt"
    test_file.write_text("Hello Playwright!")
    
    # 2. Виконуємо завантаження
    file_path_str = str(test_file.absolute())
    up_down_page.upload_file(file_path_str)
    
    # 3. Перевіряємо, що на сторінці з'явився шлях до файлу
    # DemoQA відображає фейковий шлях C:\fakepath\test_upload.txt
    expect(up_down_page.uploaded_path_text).to_be_visible()
    expect(up_down_page.uploaded_path_text).to_contain_text("test_upload.txt")