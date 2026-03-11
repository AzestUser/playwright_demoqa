import sys
from pathlib import Path

import pytest

"""
Загальні налаштування для всіх тестів.

1) Додаємо корінь проєкту в sys.path, щоб можна було імпортувати `pages.login_page` тощо.
2) Опційно підключаємо файл auth_state.json тільки для тестів,
   які явно помічені маркером @pytest.mark.auth.
"""


# Шукаємо корінь проєкту: .../playwright_demoqa
ROOT_DIR = Path(__file__).resolve().parents[1]

# Якщо корінь ще не в sys.path – додаємо.
# Завдяки цьому Python бачить наш пакет `pages` та інші модулі з кореня.
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


@pytest.fixture
def browser_context_args(request):
    """
    Базова фікстура Playwright для налаштування контексту браузера.

    - Для звичайних тестів (без маркера @pytest.mark.auth) повертаємо порожні налаштування
      => кожен тест стартує "з нуля" (без попередньої авторизації).
    - Для тестів із маркером @pytest.mark.auth додаємо storage_state з auth_state.json
      => такі тести стартують уже залогіненими.
    """
    state_path = ROOT_DIR / "auth_state.json"

    # Якщо тест помічений як такий, що потребує попередньо збережений auth-стан
    if request.node.get_closest_marker("auth"):
        return {"storage_state": str(state_path)}

    # Для всіх інших тестів – "чистий" контекст без збереженого стану
    return {}


