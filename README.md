# DemoQA Playwright Automation

## Опис /Description
Цей проєкт — UI-автоматизація на Python, Playwright та pytest для demoqa.com.
This project is UI automation with Python, Playwright, and pytest for demoqa.com.

- `pages/book_store_page.py` — сторінка книги / book store page
- `pages/login_page.py`, `pages/profile_page.py` — логін/профіль / login/profile
- `pages/radio_button_page.py` — радіо-кнопки / radio button page

## Структура / Project structure
- `pages/` — Page Object Model
- `tests/` — pytest тести / pytest tests
- `reports/` — HTML-репорти / HTML reports
- `pytest.ini` — конфігурація pytest / pytest config

## Встановлення / Setup
```bash
python -m venv venv
# Windows PowerShell

cd C:\Users\user\Documents\playwright_demoqa
python -m venv venv
.\\venv\\Scripts\\Activate.ps1
pip install -r requirements.txt


# Unix/Mac
cd ~/path/to/playwright_demoqa
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Запуск тестів локально/ Tests Run Locally
```bash
pytest -q # Windows PowerShell
```

## Запуск теста локально/ Particular test run Locally
```bash
pytest -q tests/test_radio_button.py --html=reports/report_radio_button.html --self-contained-html  # Windows PowerShell
```

## Запуск Тестів на Github/ Tests Run on GitHub
Перейдіть в меню Actions/ Go to Actions Menu
Оберіть пункт Playwright Tests в лівій панелі/ Select Playwright Tests in the left panel
Натисніть Run Workflow/ Hit Run Workflow button 
