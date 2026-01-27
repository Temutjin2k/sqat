from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def find_element(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))
    
    def find_clickable_element(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def click(self, locator):
        element = self.find_clickable_element(locator)
        element.click()

    def input_text(self, locator, text):
        element = self.find_clickable_element(locator)
        element.clear()
        element.send_keys(text)
    
    def js_click(self, element):
        self.driver.execute_script("arguments[0].click();", element)

    def js_scroll_into_view(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)


class AviasalesSearchPage(BasePage):
    URL = "https://www.aviasales.kz"
    
    # Locators
    BOOKING_LABEL = (By.XPATH, "//label[contains(., 'Booking.com')]")
    BOOKING_CHECKBOX = (By.TAG_NAME, "input")
    ORIGIN_INPUT = (By.XPATH, '//*[@id="avia_form_origin-input"]')
    DESTINATION_INPUT = (By.XPATH, '//*[@id="avia_form_destination-input"]')
    DATE_PICKER_BTN = (By.XPATH, '/html/body/div[1]/div/div[1]/div[2]/div[2]/div[2]/div/form/div[1]/div[3]/div[1]/div[1]/button[1]')
    TARGET_DATE = (By.XPATH, '/html/body/div[1]/div/div[1]/div[2]/div/div[2]/div/form/div[1]/div[3]/div[1]/div[2]/div[1]/div/div/div/div/div[2]/div/div/div/div[3]/table/tbody/tr[5]/td[4]/div/button/div[2]')
    CONFIRM_DATE_BTN = (By.XPATH, "//button[contains(., 'Выбрать')] | //button[contains(., 'Готово')] | /html/body/div[1]/div/div[1]/div[2]/div[2]/div[2]/div/form/div[1]/div[3]/div[1]/div[2]/div[1]/div/div/div/div/button")
    SEARCH_BTN = (By.CSS_SELECTOR, 'button[data-test-id="form-submit"]')

    def open(self):
        self.driver.get(self.URL)

    def disable_booking_checkbox(self):
        print("Handling booking checkbox...")
        try:
            booking_label = self.find_element(self.BOOKING_LABEL)
            checkbox_input = booking_label.find_element(*self.BOOKING_CHECKBOX)
            
            if checkbox_input.is_selected():
                self.js_click(booking_label)
                print("checkbox was active – disabled.")
            else:
                self.js_click(booking_label)
                print("Clicked checkbox (inactive mode).")
        except Exception as e:
            print(f"Failed to handle checkbox: {e}")

    def fill_search_form(self, origin, destination):
        print("Filling search form...")
        self.input_text(self.ORIGIN_INPUT, origin)
        self.input_text(self.DESTINATION_INPUT, destination)

    def select_date(self):
        # Open calendar
        self.click(self.DATE_PICKER_BTN)
        # Select date
        self.click(self.TARGET_DATE)
        print("Date selected: 28.02.2025")
        
        # Confirm date
        try:
            self.click(self.CONFIRM_DATE_BTN)
            print("Confirm button clicked")
        except Exception:
            print("No new tab or confirm button issues, staying on current page.")

    def click_search(self):
        print("Looking for search button...")
        try:
            search_button = self.find_clickable_element(self.SEARCH_BTN)
            self.js_scroll_into_view(search_button)
            
            time.sleep(1)

            self.js_click(search_button)
            print("Search button clicked via JS!")
        except Exception as e:
            print(f"Failed to click search button: {e}")
            print("Trying Plan B: Pressing ENTER in destination field...")
            to_input = self.driver.find_element(*self.DESTINATION_INPUT)
            to_input.send_keys(Keys.ENTER)


class AviasalesResultsPage(BasePage):
    TICKET_PRICE = (By.CSS_SELECTOR, 'div[data-test-id="price"]')
    BUY_OPTIONS_XPATH = '/html/body/div[2]/div/div/div/div/div[2]/div/div[2]/div[3]/div[2]'
    BUY_BUTTON_XPATH = '/html/body/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[11]'
    # NOTE: The xpath for the buy button seems very brittle/absolute in the original code. 
    # I kept it as is, but dynamic xpaths are better.

    BUT_OPTIONS = (By.XPATH, BUY_OPTIONS_XPATH)
    BUY_BUTTON = (By.XPATH, BUY_BUTTON_XPATH)

    def wait_for_results(self):
        print("Waiting for redirect to search results page...")
        try:
            WebDriverWait(self.driver, 15).until(EC.url_contains("/search/"))
            print(f"Redirected! Current URL: {self.driver.current_url}")
            print("Searching for flights...")
        except Exception as e:
            print(f"Error waiting for redirect: {e}")
            raise

    def select_first_ticket(self):
        try:
            ticket_price = WebDriverWait(self.driver, 45).until(
                EC.visibility_of_element_located(self.TICKET_PRICE)
            )
            self.js_scroll_into_view(ticket_price)
            time.sleep(1)
            self.js_click(ticket_price)
            print("Successfully clicked on the first ticket price")
        except Exception as e:
            print(f"Error selecting ticket: {e}")
            raise

    def click_buy_button(self):
        # first it should call this to open 
        buy_options_btn = self.find_clickable_element(self.BUT_OPTIONS)
        buy_options_btn.click()

        wait = WebDriverWait(self.driver, 10) 
        # User explicitly requested to find div with text 'Wingie'
        buy_btn = wait.until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Wingie')]"))
        )
        self.js_click(buy_btn)
        print("Clicked element containing 'Wingie'")


class BookingPage(BasePage):
    EMAIL_INPUT = (By.XPATH, '//*[@id="contact_email"]')
    PHONE_INPUT = (By.XPATH, '//*[@id="contact_cellphone"]')
    NAME_INPUT = (By.XPATH, '//*[@id="firstName_0"]')
    LASTNAME_INPUT = (By.XPATH, '//*[@id="lastName_0"]')
    MALE_LABEL = (By.XPATH, '//*[@id="gender_M_0"]')
    
    PASSPORT_INPUT = (By.XPATH, '//*[@id="passportNoAll_0"]')
    
    # Dropdowns (Select)
    BIRTH_DAY = (By.XPATH, '//*[@id="birthDateDay_0"]')
    BIRTH_MONTH = (By.XPATH, '//*[@id="birthDateMonth_0"]')
    BIRTH_YEAR = (By.XPATH, '//*[@id="birthDateYear_0"]')
    
    PASSPORT_DAY = (By.XPATH, '//*[@id="passportDay_0"]')
    PASSPORT_MONTH = (By.XPATH, '//*[@id="passportMonth_0"]')
    PASSPORT_YEAR = (By.XPATH, '//*[@id="passportYear_0"]')

    # Searchable select
    NATIONALITY_DROPDOWN = (By.CSS_SELECTOR, '.searchable-select__selection')
    NATIONALITY_SEARCH = (By.CSS_SELECTOR, '.searchable-select__search')
    
    COMFORT_PACKAGE = (By.XPATH, "//div[contains(@class, 'provider-package__select') and .//p[text()='Comfort']]")

    def switch_to_new_window(self, original_window):
        WebDriverWait(self.driver, 10).until(EC.number_of_windows_to_be(2))
        for window_handle in self.driver.window_handles:
            if window_handle != original_window:
                self.driver.switch_to.window(window_handle)
                break
        print(f"New page title: {self.driver.title}")

    def fill_contact_info(self, email, phone):
        self.input_text(self.EMAIL_INPUT, email)
        self.input_text(self.PHONE_INPUT, phone)

    def fill_passenger_info(self, name, lastname, birth_day, birth_month, birth_year):
        self.input_text(self.NAME_INPUT, name)
        self.input_text(self.LASTNAME_INPUT, lastname)
        
        # Gender Selection with overlay handling
        male_elem = self.driver.find_element(*self.MALE_LABEL)
        if not male_elem.is_selected():
            try:
                close_overlay = self.driver.find_elements(By.CSS_SELECTOR, '.membership-container [data-testid="closeIcon"]')
                if close_overlay:
                    close_overlay[0].click()
                    WebDriverWait(self.driver, 5).until(EC.invisibility_of_element_located((By.ID, 'membershipContainer')))
                male_elem.click()
            except Exception:
                self.js_click(male_elem)

        # Date of Birth
        Select(self.driver.find_element(*self.BIRTH_DAY)).select_by_value(f"{birth_day:02d}")
        Select(self.driver.find_element(*self.BIRTH_MONTH)).select_by_value(f"{birth_month:02d}")
        Select(self.driver.find_element(*self.BIRTH_YEAR)).select_by_value(str(birth_year))

    def fill_passport_info(self, number, day, month, year):
        self.input_text(self.PASSPORT_INPUT, number)
        Select(self.driver.find_element(*self.PASSPORT_DAY)).select_by_value(f"{day:02d}")
        Select(self.driver.find_element(*self.PASSPORT_MONTH)).select_by_value(f"{month:02d}")
        Select(self.driver.find_element(*self.PASSPORT_YEAR)).select_by_value(str(year))

    def select_nationality(self, nationality):
        self.click(self.NATIONALITY_DROPDOWN)
        search = self.find_clickable_element(self.NATIONALITY_SEARCH)
        search.clear()
        search.send_keys(nationality)
        
        option_xpath = (By.XPATH, f"//div[contains(@class, 'searchable-select__option') and text()='{nationality}']")
        option = self.find_clickable_element(option_xpath)
        option.click()
        print(f"Selected nationality: {nationality}")

    def select_comfort_package(self):
        try:
            self.click(self.COMFORT_PACKAGE)
            print("Selected 'Comfort' flight package")
        except Exception as e:
            print(f"Could not select Comfort package: {e}")
