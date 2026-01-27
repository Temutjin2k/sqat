
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from excel import ExcelReader

# Import the Page Objects
try:
    from assignment4.pages import AviasalesSearchPage, AviasalesResultsPage, BookingPage
except ModuleNotFoundError:
    from pages import AviasalesSearchPage, AviasalesResultsPage, BookingPage

from selenium.webdriver.chrome.options import Options as ChromeOptions

# === КОНФИГУРАЦИЯ BROWSERSTACK ===
BS_USER = "emutjin_ns7Vrz"
BS_KEY = "BKmb5ftVhJfAqh3qD4gG"
HUB_URL = f"https://{BS_USER}:{BS_KEY}@hub-cloud.browserstack.com/wd/hub"

class AviasalesOpenTest(unittest.TestCase):
    def setUp(self):
        options = ChromeOptions()
        
        # Настройки BrowserStack
        bstack_options = {
            "os": "Windows",
            "osVersion": "11",
            "projectName": "Aviasales Booking Project",
            "buildName": "Python POM Build",
            "sessionName": "Booking Test",
            "seleniumVersion": "4.0.0",
            "userName": BS_USER,
            "accessKey": BS_KEY,
            "consoleLogs": "errors"
        }
        options.set_capability('bstack:options', bstack_options)
        
        # Инициализация Remote WebDriver
        self.driver = webdriver.Remote(command_executor=HUB_URL, options=options)
        self.driver.maximize_window()
        # Initialize pages
        self.search_page = AviasalesSearchPage(self.driver)
        self.results_page = AviasalesResultsPage(self.driver)
        self.booking_page = BookingPage(self.driver)

    def test_open_aviasales(self):
        # 1. Читаем данные из Excel (строка 2, так как 1-я — заголовки)
        test_data = ExcelReader.get_data("assignment6/data.xlsx", 2)
        if test_data['name'] is None or test_data['lastname'] is None:
            print("Error: No test data found")
            return

        print(f"Запуск теста для: {test_data['name']} {test_data['lastname']}")
        
        # 2. Open main page
        self.search_page.open()
        self.search_page.disable_booking_checkbox()

        # 3. Используем данные из Excel для поиска
        self.search_page.fill_search_form(
            origin=test_data['origin'], 
            destination=test_data['destination']
        )
        self.search_page.select_date()
        self.search_page.click_search()

        # Результаты
        self.results_page.wait_for_results()
        self.results_page.select_first_ticket()
        original_window = self.driver.current_window_handle
        self.results_page.click_buy_button()

        # Переход на страницу бронирования
        self.booking_page.switch_to_new_window(original_window)

        # 4. Заполнение данными из Excel
        self.booking_page.fill_contact_info(
            email=test_data['email'],
            phone=test_data['phone']
        )
        
        self.booking_page.fill_passenger_info(
            name=test_data['name'],
            lastname=test_data['lastname'],
            birth_day=2, birth_month=12, birth_year=2005 # Можно тоже в Excel
        )

        self.booking_page.fill_passport_info(
            number=test_data['passport'],
            day=15, month=3, year=2032
        )

        self.booking_page.select_nationality(test_data['nationality'])
        self.booking_page.select_comfort_package()

        time.sleep(5)
        print("finished")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
