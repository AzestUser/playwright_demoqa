from playwright.sync_api import sync_playwright

"""
Цей скрипт ОДИН РАЗ логіниться на DemoQA та зберігає
стан авторизації (cookies, токени тощо) у файл auth_state.json.
Далі цей файл використовується в тестах, щоб не логінитися щоразу.
"""

# URL сторінки логіну DemoQA
DEMOQA_LOGIN_URL = "https://demoqa.com/login"

# URL сторінки профілю, куди потрапляємо після успішного логіну
DEMOQA_PROFILE_URL = "https://demoqa.com/profile"

# Облікові дані користувача, якого ти створив заздалегідь
USERNAME = "Test_User"
PASSWORD = "Test_User123!"

# Ім'я файла, куди запишемо стан авторизації
STATE_FILE = "auth_state.json"


def main() -> None:
    """
    Запускає браузер, виконує логін і зберігає auth state у файл.
    """
    # Основна точка входу в Playwright (sync API)
    with sync_playwright() as p:
        # Запускаємо браузер Chromium (headless=False, щоб бачити, що відбувається)
        browser = p.chromium.launch(headless=False)

        # Створюємо новий ізольований контекст (як окремий профіль браузера)
        context = browser.new_context()

        # Відкриваємо вкладку (Page) у цьому контексті
        page = context.new_page()

        # 1. Відкриваємо сторінку логіну
        page.goto(DEMOQA_LOGIN_URL)

        # 2. Вводимо логін і пароль у відповідні поля
        page.fill("#userName", USERNAME)
        page.fill("#password", PASSWORD)

        # 3. Натискаємо кнопку логіну
        page.click("#login")

        # 4. Чекаємо, поки нас перенаправить на сторінку профілю
        page.wait_for_url(DEMOQA_PROFILE_URL)

        # 5. Зберігаємо весь стан контексту в файл (cookies, localStorage тощо)
        context.storage_state(path=STATE_FILE)

        # 6. Закриваємо браузер
        browser.close()


if __name__ == "__main__":
    # Дозволяє запускати скрипт командою: python auth_setup.py
    main()

