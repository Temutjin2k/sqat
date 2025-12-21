
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


class AviasalesOpenTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install())
        )
        self.driver.maximize_window()

    def test_open_aviasales(self):
        driver = self.driver
        url = "https://www.aviasales.kz/search/NQZ2502URA1?marker=186703.google_ppc_kz_nqz_sr_bd_a-all_exp-phrase-match&utm_campaign_id=23287122653&utm_adgroup_id=191536919920&utm_content_id=647308259442&utm_extension_id=&term_match_type=e&utm_term=aviasales&utm_term_id=kwd-42393665022&network=g&placement=&position=&device=c.&geo=.1009806&gad_source=1&gad_campaignid=23287122653&gclid=Cj0KCQiA0p7KBhCkARIsAE6XlalUDLKsiOiwtfdintfRQBcyTd9AhOQjTTrM-VrTcJSNlUlafM1lAtIaAhseEALw_wcB"
        driver.get(url)
        print("Opened web page, trying to pass captcha")
        # time.sleep(30)  # Wait for manual captcha if needed
        print("passed captcha timeout")
        # Wait for the first ticket price block to be clickable and click it
        ticket_div = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-test-id="price"]'))
        )
        ticket_div.click()
        print("Clicked first ticket div")

        # Wait for the module to appear and then click the 'Купить' button for the first proposal
        buy_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/div/div/div[2]/div/div[2]/div[3]/div[1]/div[1]/div/div[2]/button'))
        )
        
        # 1. Save the handle of the current (Aviasales) window
        original_window = driver.current_window_handle

        buy_button.click() # Here it redirects to another website to pay
        print("Clicked 'Купить' button for first proposal")

        # 3. Wait for the new window or tab to open
        WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))

        # 4. Loop through handles to find the new one
        for window_handle in driver.window_handles:
            if window_handle != original_window:
                driver.switch_to.window(window_handle)
                break

        # Now the 'driver' is focused on the airline/booking website
        print(f"New page title: {driver.title}")

        # Fill booking form fields using XPaths and values
        email = "example@astanait.edu.kz"
        phone = "7051682938"
        name = "Temutjin"
        lastname = "Koszhanov"
        birth_day = 28
        birth_month = 2
        birth_year = 2006
        passport_number = "123456798"
        passport_exp_day = 15
        passport_exp_month = 3
        passport_exp_year = 2032
        natianalaty="Россия"

        # Email
        email_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="contact_email"]'))
        )
        email_input.clear()
        email_input.send_keys(email)

        # Phone
        phone_input = driver.find_element(By.XPATH, '//*[@id="contact_cellphone"]')
        phone_input.clear()
        phone_input.send_keys(phone)

        # Name
        name_input = driver.find_element(By.XPATH, '//*[@id="firstName_0"]')
        name_input.clear()
        name_input.send_keys(name)

        # Lastname
        lastname_input = driver.find_element(By.XPATH, '//*[@id="lastName_0"]')
        lastname_input.clear()
        lastname_input.send_keys(lastname)


        # Sex (male) - handle overlay if present
        male_label = driver.find_element(By.XPATH, '//*[@id="gender_M_0"]')
        if not male_label.is_selected():
            try:
                # Try to close overlay if it exists
                close_overlay = driver.find_elements(By.CSS_SELECTOR, '.membership-container [data-testid="closeIcon"]')
                if close_overlay:
                    close_overlay[0].click()
                    WebDriverWait(driver, 5).until(EC.invisibility_of_element_located((By.ID, 'membershipContainer')))
                male_label.click()
            except Exception:
                # If still not clickable, use JS click
                driver.execute_script("arguments[0].click();", male_label)

        # Date of birth
        from selenium.webdriver.support.ui import Select
        Select(driver.find_element(By.XPATH, '//*[@id="birthDateDay_0"]')).select_by_value(f"{birth_day:02d}")
        Select(driver.find_element(By.XPATH, '//*[@id="birthDateMonth_0"]')).select_by_value(f"{birth_month:02d}")
        Select(driver.find_element(By.XPATH, '//*[@id="birthDateYear_0"]')).select_by_value(str(birth_year))

        # Passport number
        passport_input = driver.find_element(By.XPATH, '//*[@id="passportNoAll_0"]')
        passport_input.clear()
        passport_input.send_keys(passport_number)

        # Passport expiration
        Select(driver.find_element(By.XPATH, '//*[@id="passportDay_0"]')).select_by_value(f"{passport_exp_day:02d}")
        Select(driver.find_element(By.XPATH, '//*[@id="passportMonth_0"]')).select_by_value(f"{passport_exp_month:02d}")
        Select(driver.find_element(By.XPATH, '//*[@id="passportYear_0"]')).select_by_value(str(passport_exp_year))

        # Nationality selection (searchable dropdown)
        dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.searchable-select__selection'))
        )
        dropdown.click()

        search_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '.searchable-select__search'))
        )
        search_input.clear()
        search_input.send_keys(natianalaty)

        option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class, 'searchable-select__option') and text()='{natianalaty}']"))
        )
        option.click()
        print(f"Selected nationality: {natianalaty}")


        comfort_package = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'provider-package__select') and .//p[text()='Comfort']]"))
        )
        comfort_package.click()
        print("Selected 'Comfort' flight package")    

        time.sleep(10)

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
