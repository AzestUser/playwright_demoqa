Playwright DemoQA Automation / Автоматизація DemoQA на Playwright
Опис (Ukrainian)
Цей репозиторій містить приклади автоматизованих тестів на Playwright + pytest для сайту:

https://demoqa.com
Структура:

pages — page object model (Book Store, Login, Profile, Radio Button)
tests — pytest тести
reports — HTML звіти від pytest --html=...
Запуск
python -m venv venv
Activate.ps1 (Windows)
pip install -r requirements.txt
pytest -q test_radio_button.py --html=reports/report_radio_button.html
Команди
pytest -q tests/test_radio_button.py — тільки Radio Button
pytest -q tests/test_login.py — тільки логін
pytest -q — всі тести
Git
git checkout -b feature/radio-button-test
git add .
git commit -m "Add radio button tests"
git push -u origin feature/radio-button-test
