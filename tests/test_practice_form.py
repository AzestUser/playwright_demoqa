import os
import pytest
from playwright.sync_api import expect
from pages.practice_form_page import PracticeFormPage

@pytest.fixture
def form_page(page):
    # Встановлюємо великий екран, щоб елементи не наповзали один на одного
    page.set_viewport_size({"width": 1920, "height": 1080})
    p = PracticeFormPage(page)
    p.navigate()
    return p

def test_submit_full_practice_form(form_page, tmp_path):
    # 1. Створюємо фейкову картинку для завантаження
    fake_img = tmp_path / "avatar.png"
    fake_img.write_text("fake image content")
    
    # 2. Заповнюємо базові дані
    form_page.first_name.fill("Ostap")
    form_page.last_name.fill("Bender")
    form_page.email.fill("ostap@bender.com")
    form_page.select_gender("Male")
    form_page.mobile.fill("1234567890")
    
    # 3. Працюємо з календарем
    form_page.fill_date_of_birth(day="15", month="July", year="1995")
    
    # 4. Спеціальні поля
    form_page.fill_subjects(["English", "Maths"])
    form_page.select_hobby("Sports")
    form_page.select_hobby("Music")
    
    # 5. Завантаження файлу та адреса
    form_page.upload_picture(str(fake_img.absolute()))
    form_page.current_address.fill("Vinnytsia, Ukraine")
    
    # 6. Випадаючі списки штату та міста
    form_page.select_state_and_city("NCR", "Delhi")
    
    # 7. Надсилаємо форму
    form_page.submit_form()
    
    # 8. Перевірки в модальному вікні
    expect(form_page.modal_title).to_be_visible()
    expect(form_page.modal_title).to_have_text("Thanks for submitting the form")
    
    # Перевіряємо вміст таблиці
    expect(form_page.modal_table).to_contain_text("Ostap Bender")
    expect(form_page.modal_table).to_contain_text("ostap@bender.com")
    expect(form_page.modal_table).to_contain_text("Male")
    expect(form_page.modal_table).to_contain_text("1234567890")
    expect(form_page.modal_table).to_contain_text("15 July,1995")
    expect(form_page.modal_table).to_contain_text("English, Maths")
    expect(form_page.modal_table).to_contain_text("Sports, Music")
    expect(form_page.modal_table).to_contain_text("avatar.png")
    expect(form_page.modal_table).to_contain_text("Vinnytsia, Ukraine")
    expect(form_page.modal_table).to_contain_text("NCR Delhi")
    
    # Закриваємо модалку
    #form_page.close_modal_btn.click()
    #expect(form_page.modal_title).to_be_hidden()
    # Замість form_page.close_modal_btn.click()
    form_page.page.keyboard.press("Escape")
    expect(form_page.modal_title).to_be_hidden()