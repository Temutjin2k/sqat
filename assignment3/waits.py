import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver import Keys, ActionChains
import time


class WebWaitTests(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def test_spotify_implicit_wait(self):
        print("test_spotify_implicit_wait")
        d = self.driver

        # 1. IMPLICIT WAIT
        d.implicitly_wait(10)
        d.get("https://www.spotify.com/")

        try:
            logo = d.find_element(By.TAG_NAME, "svg")
            print("Spotify test: Logo found using Implicit Wait.")
            self.assertTrue(logo.is_displayed())
        except NoSuchElementException:
            self.fail("Элемент не был найден в течение времени неявного ожидания")
        
        print("test_spotify_implicit_wait finished")
        time.sleep(2)

    def test_github_explicit_wait(self):
        print("test_github_explicit_wait")

        self.driver.get("https://github.com/Temutjin2k")

        wait = WebDriverWait(self.driver, 15)

        # Explicit Wait
        repos_tab = wait.until(
            EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Repositories"))
        )
        
        repos_tab.click()
        
        wait.until(EC.url_contains("tab=repositories"))
        print("test_github_explicit_wait finished")
        time.sleep(2)

    def test_3_dynamic_fluent(self):
        self.driver.get("https://the-internet.herokuapp.com/dynamic_loading/1")

        # Находим кнопку Start и кликаем через ActionChains
        start_button = self.driver.find_element(By.CSS_SELECTOR, "#start button")
        ActionChains(self.driver).click(start_button).perform()

        fluent_wait = WebDriverWait(
            self.driver, 
            timeout=20, 
            poll_frequency=1, 
            ignored_exceptions=[NoSuchElementException, ElementNotInteractableException]
        )

        # Ждем появления финального текста
        finish_text_element = fluent_wait.until(
            EC.visibility_of_element_located((By.ID, "finish"))
        )

        ActionChains(self.driver).send_keys("Finished!").perform()

        self.assertEqual(finish_text_element.text, "Hello World!")
        print(f"Test 3: Fluent Wait OK. Result: {finish_text_element.text}")

        time.sleep(2)
    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()