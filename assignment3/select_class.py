import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SelectClassTests(unittest.TestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)

    def test_facebook_signup_dropdowns(self):
        # TASK 3: Select Class
     
        self.driver.get("https://www.facebook.com/r.php")
        
        wait = WebDriverWait(self.driver, 10)
        print("\nTesting Dropdowns on Facebook Sign Up Page...")

        # MONTH SELECT (by Visible Text)
        month_elem = wait.until(EC.presence_of_element_located((By.ID, "month")))
        month_select = Select(month_elem)
        
        target_month = "Feb"
        month_select.select_by_visible_text(target_month)
        
        selected_month = month_select.first_selected_option.text
        self.assertEqual(selected_month, target_month)
        print(f"Selected month by visible text: {selected_month}")
        time.sleep(1)

        # DAY SELECT (by Value) 
        day_elem = self.driver.find_element(By.ID, "day")
        day_select = Select(day_elem)
        
        target_day_value = "28"
        day_select.select_by_value(target_day_value)
        
        selected_day = day_select.first_selected_option.text
        self.assertEqual(day_select.first_selected_option.get_attribute("value"), target_day_value)
        print(f"Selected day by value: {selected_day}")
        time.sleep(1)

        year_elem = self.driver.find_element(By.ID, "year")
        year_select = Select(year_elem)
        
        year_select.select_by_value("2006")
        
        selected_year = year_select.first_selected_option.text
        self.assertEqual(selected_year, "2006")
        print(f"Selected year: {selected_year}")
        time.sleep(1)

        print("Select Class Test - PASSED!")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
