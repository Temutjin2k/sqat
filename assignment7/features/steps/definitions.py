from behave import given, when, then
import time

# --- SEARCH STEPS ---

@given('I open the Aviasales website')
def step_open_site(context):
    context.search_page.open()
    context.search_page.disable_booking_checkbox()

@when('I search for a ticket from "{origin}" to "{destination}"')
def step_search_flight(context, origin, destination):
    # Code snippet from your item #3
    context.search_page.fill_search_form(origin, destination)
    context.search_page.select_date()
    context.search_page.click_search()

@then('I see a list of results')
def step_see_results(context):
    context.results_page.wait_for_results()

# --- BOOKING STEPS

@given('I have already found tickets from "{origin}" to "{destination}"')
def step_precondition_search(context, origin, destination):
    # It does open -> search -> wait, so we are ready to select a ticket
    context.search_page.open()
    context.search_page.disable_booking_checkbox()
    context.search_page.fill_search_form(origin, destination)
    context.search_page.select_date()
    context.search_page.click_search()
    context.results_page.wait_for_results()

@when('I select the first ticket and click buy')
def step_select_and_buy(context):
    # Save the window ID
    context.original_window = context.driver.current_window_handle
    context.results_page.select_first_ticket()
    context.results_page.click_buy_button()

@then('the booking tab opens')
def step_verify_tab(context):
    context.booking_page.switch_to_new_window(context.original_window)

@given('I am on the booking page (flight {origin}-{dest})')
def step_precondition_full_flow(context, origin, dest):
    # SUPER-STEP: Executes EVERYTHING before the booking page
    # 1. Search
    context.search_page.open()
    context.search_page.disable_booking_checkbox()
    context.search_page.fill_search_form(origin, dest)
    context.search_page.select_date()
    context.search_page.click_search()
    # 2. Select
    context.results_page.wait_for_results()
    context.results_page.select_first_ticket()
    context.original_window = context.driver.current_window_handle
    context.results_page.click_buy_button()
    # 3. Switch
    context.booking_page.switch_to_new_window(context.original_window)

@when('I fill in contact details: "{email}", "{phone}"')
def step_fill_contacts(context, email, phone):
    context.booking_page.fill_contact_info(email, phone)

@when('I fill in passenger details: "{name}", "{lastname}"')
def step_fill_passenger(context, name, lastname):
    # Birth date is hardcoded as in your code
    context.booking_page.fill_passenger_info(name, lastname, 2, 12, 2005)

@when('I fill in passport details: "{passport}", nationality "{nationality}"')
def step_fill_docs(context, passport, nationality):
    context.booking_page.fill_passport_info(passport, 15, 3, 2032)
    context.booking_page.select_nationality(nationality)

@then('I successfully select the Comfort package')
def step_finish(context):
    context.booking_page.select_comfort_package()
    time.sleep(5)

# --- STEPS USING EXCEL ---
from excel import ExcelReader

@given('I load test data from Excel "{filename}" (row {row})')
def step_load_data(context, filename, row):
    context.test_data = ExcelReader.get_data(filename, int(row))
    print(f"Data loaded for passenger: {context.test_data['name']}")

@when('I search for a ticket using data from Excel')
def step_search_flight_excel(context):
    origin = context.test_data['origin']
    destination = context.test_data['destination']
    context.search_page.fill_search_form(origin, destination)
    context.search_page.select_date()
    context.search_page.click_search()

@given('I have reached the booking page with data from Excel')
def step_precondition_full_flow_excel(context):
    origin = context.test_data['origin']
    dest = context.test_data['destination']
    
    # 1. Search
    context.search_page.open()
    context.search_page.disable_booking_checkbox()
    context.search_page.fill_search_form(origin, dest)
    context.search_page.select_date()
    context.search_page.click_search()
    
    # 2. Select
    context.results_page.wait_for_results()
    context.results_page.select_first_ticket()
    context.original_window = context.driver.current_window_handle
    context.results_page.click_buy_button()
    
    # 3. Switch
    context.booking_page.switch_to_new_window(context.original_window)

@when('I fill in contact details from Excel')
def step_fill_contacts_excel(context):
    email = context.test_data['email']
    phone = context.test_data['phone']
    context.booking_page.fill_contact_info(email, phone)

@when('I fill in passenger details from Excel')
def step_fill_passenger_excel(context):
    name = context.test_data['name']
    lastname = context.test_data['lastname']
    context.booking_page.fill_passenger_info(name, lastname, 2, 12, 2005)

@when('I fill in passport details from Excel')
def step_fill_docs_excel(context):
    passport = context.test_data['passport']
    nationality = context.test_data['nationality']
    context.booking_page.fill_passport_info(passport, 15, 3, 2032)
    context.booking_page.select_nationality(nationality)