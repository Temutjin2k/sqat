from behave import given, when, then
import time

# --- ШАГИ ДЛЯ ПОИСКА ---

@given('я открываю сайт Aviasales')
def step_open_site(context):
    context.search_page.open()
    context.search_page.disable_booking_checkbox()

@when('я ищу билет из "{origin}" в "{destination}"')
def step_search_flight(context, origin, destination):
    # Кусок кода из твоего пункта #3
    context.search_page.fill_search_form(origin, destination)
    context.search_page.select_date()
    context.search_page.click_search()

@then('я вижу список результатов')
def step_see_results(context):
    context.results_page.wait_for_results()

# --- ШАГИ ДЛЯ БРОНИРОВАНИЯ (САМОЕ ВАЖНОЕ) ---

@given('я уже нашел билеты из "{origin}" в "{destination}"')
def step_precondition_search(context, origin, destination):
    # ЭТОТ ШАГ ВОССТАНАВЛИВАЕТ ПОСЛЕДОВАТЕЛЬНОСТЬ!
    # Он делает open -> search -> wait, чтобы мы были готовы выбирать билет
    context.search_page.open()
    context.search_page.disable_booking_checkbox()
    context.search_page.fill_search_form(origin, destination)
    context.search_page.select_date()
    context.search_page.click_search()
    context.results_page.wait_for_results()

@when('я выбираю первый билет и жму купить')
def step_select_and_buy(context):
    # Сохраняем ID окна
    context.original_window = context.driver.current_window_handle
    context.results_page.select_first_ticket()
    context.results_page.click_buy_button()

@then('открывается вкладка бронирования')
def step_verify_tab(context):
    context.booking_page.switch_to_new_window(context.original_window)

@given('я нахожусь на странице оформления бронирования (рейс {origin}-{dest})')
def step_precondition_full_flow(context, origin, dest):
    # СУПЕР-ШАГ: Выполняет ВСЁ, что было до страницы бронирования
    # 1. Поиск
    context.search_page.open()
    context.search_page.disable_booking_checkbox()
    context.search_page.fill_search_form(origin, dest)
    context.search_page.select_date()
    context.search_page.click_search()
    # 2. Выбор
    context.results_page.wait_for_results()
    context.results_page.select_first_ticket()
    context.original_window = context.driver.current_window_handle
    context.results_page.click_buy_button()
    # 3. Переход
    context.booking_page.switch_to_new_window(context.original_window)

@when('я заполняю контакты: "{email}", "{phone}"')
def step_fill_contacts(context, email, phone):
    context.booking_page.fill_contact_info(email, phone)

@when('я заполняю пассажира: "{name}", "{lastname}"')
def step_fill_passenger(context, name, lastname):
    # Данные рождения берем хардкодом, как у тебя было в коде
    context.booking_page.fill_passenger_info(name, lastname, 2, 12, 2005)

@when('я заполняю паспорт: "{passport}", гражданство "{nationality}"')
def step_fill_docs(context, passport, nationality):
    context.booking_page.fill_passport_info(passport, 15, 3, 2032)
    context.booking_page.select_nationality(nationality)

@then('я успешно выбираю тариф Comfort')
def step_finish(context):
    context.booking_page.select_comfort_package()
    time.sleep(5) # Чтобы препод успел увидеть результат

# --- ШАГИ С ИСПОЛЬЗОВАНИЕМ EXCEL ---
from excel import ExcelReader

@given('я загружаю тестовые данные из Excel "{filename}" (строка {row})')
def step_load_data(context, filename, row):
    context.test_data = ExcelReader.get_data(filename, int(row))
    print(f"Данные загружены для пассажира: {context.test_data['name']}")

@when('я ищу билет используя данные из Excel')
def step_search_flight_excel(context):
    origin = context.test_data['origin']
    destination = context.test_data['destination']
    context.search_page.fill_search_form(origin, destination)
    context.search_page.select_date()
    context.search_page.click_search()

@given('я дошел до страницы бронирования с данными из Excel')
def step_precondition_full_flow_excel(context):
    origin = context.test_data['origin']
    dest = context.test_data['destination']
    
    # 1. Поиск
    context.search_page.open()
    context.search_page.disable_booking_checkbox()
    context.search_page.fill_search_form(origin, dest)
    context.search_page.select_date()
    context.search_page.click_search()
    
    # 2. Выбор
    context.results_page.wait_for_results()
    context.results_page.select_first_ticket()
    context.original_window = context.driver.current_window_handle
    context.results_page.click_buy_button()
    
    # 3. Переход
    context.booking_page.switch_to_new_window(context.original_window)

@when('я заполняю контактные данные из Excel')
def step_fill_contacts_excel(context):
    email = context.test_data['email']
    phone = context.test_data['phone']
    context.booking_page.fill_contact_info(email, phone)

@when('я заполняю данные пассажира из Excel')
def step_fill_passenger_excel(context):
    name = context.test_data['name']
    lastname = context.test_data['lastname']
    context.booking_page.fill_passenger_info(name, lastname, 2, 12, 2005)

@when('я заполняю паспортные данные из Excel')
def step_fill_docs_excel(context):
    passport = context.test_data['passport']
    nationality = context.test_data['nationality']
    context.booking_page.fill_passport_info(passport, 15, 3, 2032)
    context.booking_page.select_nationality(nationality)