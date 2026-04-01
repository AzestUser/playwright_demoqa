import pytest
from playwright.sync_api import expect
from pages.web_tables_page import WebTablesPage

# Тести перевіряють функціонал пошуку, додавання та редагування
# записів на сторінці DemoQA Web Tables.
@pytest.fixture(autouse=True)
def web_tables(page):
    # Встановлюємо великий екран, щоб елементи не перекривалися
    # і щоб стабільно знаходити кнопки у таблиці.
    page.set_viewport_size({"width": 1920, "height": 1080})
    wt = WebTablesPage(page)
    wt.navigate()
    return wt


def test_search_and_filter_validation(web_tables):
    # 1. Шукаємо Cierra
    search_query = "Cierra"
    web_tables.search_record(search_query)

    # 2. Використовуємо сучасну розмітку таблиці на DemoQA
    table_body = web_tables.table_body

    # 3. Перевіряємо, що в тілі таблиці є потрібний текст
    expect(table_body.get_by_text(search_query, exact=True)).to_be_visible(timeout=10000)
    
    # Перевіряємо інші дані в цьому ж контексті
    expect(table_body).to_contain_text("Vega")
    expect(table_body).to_contain_text("cierra@example.com")

    # 4. Перевірка на відсутність Alden в результаті пошуку
    expect(table_body).not_to_contain_text("Alden")

    # 5. Очищуємо пошук (скидання)
    web_tables.clear_search()
    
    # 6. Перевіряємо, що Alden повернувся
    expect(table_body.get_by_text("Alden", exact=True)).to_be_visible(timeout=5000)


def test_add_and_edit_record(web_tables):
    # Підготувати дані нового запису для додавання
    new_record = {
        "first_name": "Anna",
        "last_name": "Smith",
        "email": "anna.smith@example.com",
        "age": 28,
        "salary": 88000,
        "department": "HR",
    }

    # Додаємо новий запис через форму
    web_tables.add_new_record(
        first_name=new_record["first_name"],
        last_name=new_record["last_name"],
        email=new_record["email"],
        age=new_record["age"],
        salary=new_record["salary"],
        department=new_record["department"],
    )

    # Перевіряємо, що запис з'явився в таблиці
    web_tables.search_record(new_record["email"])
    expect(web_tables.table_body).to_contain_text(new_record["first_name"])
    expect(web_tables.table_body).to_contain_text(new_record["last_name"])
    expect(web_tables.table_body).to_contain_text(new_record["email"])
    expect(web_tables.table_body).to_contain_text(new_record["department"])

    # Очищуємо пошук, щоб повернутися до повного списку
    web_tables.clear_search()

    updated_first_name = "Anya"
    updated_department = "Marketing"
    updated_salary = 98000

    # Редагуємо доданий запис за email
    web_tables.edit_record_by_email(
        new_record["email"],
        first_name=updated_first_name,
        salary=updated_salary,
        department=updated_department,
    )

    # Перевіряємо оновлені значення після редагування
    web_tables.search_record(new_record["email"])
    expect(web_tables.table_body).to_contain_text(updated_first_name)
    expect(web_tables.table_body).to_contain_text(str(updated_salary))
    expect(web_tables.table_body).to_contain_text(updated_department)


def test_delete_record(web_tables):
    # Підготувати новий запис, який будемо видаляти.
    new_record = {
        "first_name": "Olena",
        "last_name": "Kovalenko",
        "email": "olena.kovalenko@example.com",
        "age": 31,
        "salary": 76000,
        "department": "Finance",
    }

    # Додаємо запис, щоб мати стабільний елемент для видалення.
    web_tables.add_new_record(
        first_name=new_record["first_name"],
        last_name=new_record["last_name"],
        email=new_record["email"],
        age=new_record["age"],
        salary=new_record["salary"],
        department=new_record["department"],
    )

    # Переконуємося, що запис видно перед видаленням.
    web_tables.search_record(new_record["email"])
    expect(web_tables.table_body).to_contain_text(new_record["email"])

    # Видаляємо рядок і перевіряємо, що його більше немає в таблиці.
    web_tables.delete_record_by_email(new_record["email"])
    web_tables.clear_search()
    expect(web_tables.table_body).not_to_contain_text(new_record["email"])
