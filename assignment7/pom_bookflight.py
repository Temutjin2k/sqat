
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from excel import ExcelReader

# Import the Page Objects
from pages import AviasalesSearchPage, AviasalesResultsPage, BookingPage

class AviasalesOpenTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install())
        )
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
