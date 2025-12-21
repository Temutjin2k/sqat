# Create a test case for login and logout functionality (30pts)

import unittest
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

load_dotenv()


class LoginLogoutTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install())
        )
        self.driver.maximize_window()

    def test_login(self):
        driver = self.driver

        url = os.getenv("ALEM_URL")
        login = os.getenv("ALEM_EMAIL")
        password = os.getenv("ALEM_PASS")

        driver.get(url)

        email_input = driver.find_element(By.CSS_SELECTOR, "input[name='email']")
        email_input.clear()
        email_input.send_keys(login)

        password_input = driver.find_element(By.XPATH, "//input[@name='password']")
        password_input.clear()
        password_input.send_keys(password)

        login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_button.click()


        self.assertIn("alem", driver.current_url)

    def test_logout(self):
        """Test logout functionality on platform alem using CSS and XPath selectors"""
        driver = self.driver

        url = os.getenv("ALEM_URL")
        login = os.getenv("ALEM_EMAIL")
        password = os.getenv("ALEM_PASS")

        driver.get(url)

        email_input = driver.find_element(By.CSS_SELECTOR, "input[name='email']")
        email_input.clear()
        email_input.send_keys(login)

        password_input = driver.find_element(By.XPATH, "//input[@name='password']")
        password_input.clear()
        password_input.send_keys(password)

        login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_button.click()
        time.sleep(1)

        try:
            dropdown_button = driver.find_element(By.CSS_SELECTOR, "button.MuiIconButton-root")
            dropdown_button.click()

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//p[text()='Log out']/ancestor::li"))
            )
            logout_button = driver.find_element(By.XPATH, "//p[text()='Log out']/ancestor::li")
            logout_button.click()

            self.assertTrue(driver.find_element(By.CSS_SELECTOR, "input[name='email']"))
        except Exception as e:
            self.fail(f"Logout button not found or error occurred: {e}")
    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
