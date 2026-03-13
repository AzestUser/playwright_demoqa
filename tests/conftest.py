import sys
from pathlib import Path

import pytest

"""
Загальні налаштування для всіх тестів.

Додаємо корінь проєкту в sys.path, щоб можна було імпортувати `pages.login_page` тощо.
"""


# Шукаємо корінь проєкту: .../playwright_demoqa
ROOT_DIR = Path(__file__).resolve().parents[1]

# Якщо корінь ще не в sys.path – додаємо.
# Завдяки цьому Python бачить наш пакет `pages` та інші модулі з кореня.
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


