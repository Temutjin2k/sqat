
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Import the Page Objects
# Import the Page Objects
try:
    from assignment4.pages import AviasalesSearchPage, AviasalesResultsPage, BookingPage
except ModuleNotFoundError:
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
        # Open main page
        self.search_page.open()

        # Disable booking checkbox if present
        self.search_page.disable_booking_checkbox()

        # Fill search form
        self.search_page.fill_search_form(origin="Астана", destination="Уральск")

        # Select date (28.02.2025 hardcoded in page object logic as per original)
        self.search_page.select_date()

        # Search
        self.search_page.click_search()

        # Wait for results and select first ticket
        self.results_page.wait_for_results()
        self.results_page.select_first_ticket()

        # Click 'Buy'
        # Save original window handle before clicking
        original_window = self.driver.current_window_handle
        self.results_page.click_buy_button()

        # Switch to new window
        self.booking_page.switch_to_new_window(original_window)

        # Fill booking info
        self.booking_page.fill_contact_info(
            email="231504@astanait.edu.kz",
            phone="7777777777"
        )
        
        self.booking_page.fill_passenger_info(
            name="Temutjin",
            lastname="Koszhanov",
            birth_day=2,
            birth_month=12,
            birth_year=2005
        )

        self.booking_page.fill_passport_info(
            number="123456798",
            day=15,
            month=3,
            year=2032
        )

        self.booking_page.select_nationality("Россия")
        
        self.booking_page.select_comfort_package()

        time.sleep(7)
        print("finished")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
