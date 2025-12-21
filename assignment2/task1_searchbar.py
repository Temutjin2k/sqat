import unittest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

load_dotenv()

class SearchTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install())
        )

    def test_search_youtube(self):
        driver = self.driver
        driver.get("https://www.youtube.com/")

        time.sleep(2) 

        search_input = driver.find_element(By.NAME, "search_query")

        searchtext = "Astana IT University"

        search_input.send_keys(searchtext)
        search_input.submit()

        time.sleep(2) 

        self.assertIn(searchtext, driver.page_source)

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
