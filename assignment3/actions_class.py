import unittest
import time
import math
from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ActionChainsTests(unittest.TestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)
        self.actions = ActionChains(self.driver)

    def test_1_keyboard_symphony(self):
        # 1. KEYBOARD ACTIONS - Interactive Typing Test
   
        self.driver.get("https://demoqa.com/text-box")
        wait = WebDriverWait(self.driver, 10)

        full_name_input = wait.until(
            EC.visibility_of_element_located((By.ID, "userName"))
        )

        self.actions.click(full_name_input)\
            .key_down(Keys.SHIFT)\
            .send_keys("john")\
            .key_up(Keys.SHIFT)\
            .perform()
        
        self.actions.send_keys(" doe").perform()
        
        self.assertEqual(full_name_input.get_attribute("value"), "JOHN doe")
        time.sleep(1)

        self.actions.key_down(Keys.CONTROL)\
            .send_keys("a")\
            .key_up(Keys.CONTROL)\
            .send_keys(Keys.DELETE)\
            .perform()
        
        self.assertEqual(full_name_input.get_attribute("value"), "")
        time.sleep(1)

        email_input = self.driver.find_element(By.ID, "userEmail")
        
        self.actions.click(full_name_input)\
            .send_keys("Selenium Master")\
            .send_keys(Keys.TAB)\
            .send_keys("test@selenium.dev")\
            .perform()
        
        self.assertEqual(full_name_input.get_attribute("value"), "Selenium Master")
        self.assertEqual(email_input.get_attribute("value"), "test@selenium.dev")
        time.sleep(1)

        current_address = self.driver.find_element(By.ID, "currentAddress")
        self.actions.click(current_address)\
            .send_keys("123 Main Street")\
            .send_keys(Keys.HOME)\
            .key_down(Keys.SHIFT)\
            .send_keys(Keys.END)\
            .key_up(Keys.SHIFT)\
            .perform()
        
        self.actions.key_down(Keys.CONTROL)\
            .send_keys("c")\
            .key_up(Keys.CONTROL)\
            .perform()
        time.sleep(1)

        submit_btn = self.driver.find_element(By.ID, "submit")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
        time.sleep(0.5)
        
        self.actions.send_keys(Keys.TAB)\
            .send_keys(Keys.TAB)\
            .send_keys(Keys.ENTER)\
            .perform()

        output = wait.until(
            EC.visibility_of_element_located((By.ID, "output"))
        )
        self.assertTrue(output.is_displayed())
        

        print("Demonstrated: SHIFT typing, Ctrl+A, DELETE, TAB navigation, HOME/END, Ctrl+C, ENTER submit")

    def test_2_mouse_maestro(self):
        # 2. MOUSE INTERACTIONS - Hover, Double Click, Right Click

        self.driver.get("https://demoqa.com/menu")
        wait = WebDriverWait(self.driver, 10)

        main_item_2 = wait.until(
            EC.visibility_of_element_located((By.LINK_TEXT, "Main Item 2"))
        )
        
        self.actions.move_to_element(main_item_2).perform()
        time.sleep(1)
        
        sub_sub_list = wait.until(
            EC.visibility_of_element_located((By.LINK_TEXT, "SUB SUB LIST »"))
        )
        self.actions.move_to_element(sub_sub_list).perform()
        time.sleep(1)
        
        sub_sub_item = wait.until(
            EC.visibility_of_element_located((By.LINK_TEXT, "Sub Sub Item 1"))
        )
        self.assertTrue(sub_sub_item.is_displayed())

        self.driver.get("https://demoqa.com/buttons")
        wait = WebDriverWait(self.driver, 10)
        
        self.actions = ActionChains(self.driver)

        double_click_btn = wait.until(
            EC.visibility_of_element_located((By.ID, "doubleClickBtn"))
        )
        
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", double_click_btn)
        time.sleep(0.5)
        
        self.actions.double_click(double_click_btn).perform()
        
        double_click_msg = wait.until(
            EC.visibility_of_element_located((By.ID, "doubleClickMessage"))
        )
        self.assertIn("double click", double_click_msg.text.lower())
        time.sleep(1)

        # --- PART C: RIGHT CLICK (Context Click) ---
        self.actions = ActionChains(self.driver)
        right_click_btn = self.driver.find_element(By.ID, "rightClickBtn")
        
        self.actions.context_click(right_click_btn).perform()
        
        right_click_msg = wait.until(
            EC.visibility_of_element_located((By.ID, "rightClickMessage"))
        )
        self.assertIn("right click", right_click_msg.text.lower())
        time.sleep(1)

        self.actions = ActionChains(self.driver)
        dynamic_btn = self.driver.find_element(
            By.XPATH, "//button[text()='Click Me']"
        )
        
        self.actions.move_to_element(dynamic_btn).click().perform()
        
        dynamic_msg = wait.until(
            EC.visibility_of_element_located((By.ID, "dynamicClickMessage"))
        )
        self.assertIn("dynamic click", dynamic_msg.text.lower())
        time.sleep(1)
 
   
        print("Demonstrated: hover/move_to_element, double_click, context_click, dynamic click")

    def test_3_draw_heart_art(self):
        # DRAG AND DROP - Drawing a Heart ❤️
    
        self.driver.get("https://kleki.com/")
        wait = WebDriverWait(self.driver, 15)

        canvas = wait.until(
            EC.visibility_of_element_located((By.TAG_NAME, "canvas"))
        )
        time.sleep(2) 
        
        self.actions = ActionChains(self.driver)
        self.actions.move_to_element(canvas).click().perform()
        time.sleep(0.5)
    
        scale = 6
        
        heart_points = []
        for i in range(0, 80):  
            t = (i / 79) * 2 * math.pi
            x = 16 * (math.sin(t) ** 3)
            y = -(13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t))
            heart_points.append((int(x * scale), int(y * scale)))
        
        self.actions = ActionChains(self.driver)
        
        start_x, start_y = heart_points[0]
        self.actions.move_to_element_with_offset(canvas, start_x, start_y - 40)
        self.actions.click_and_hold()
        
        prev_x, prev_y = start_x, start_y - 40
        for x, y in heart_points:
            y = y - 40 
            dx = x - prev_x
            dy = y - prev_y
            if dx != 0 or dy != 0:
                self.actions.move_by_offset(dx, dy)
            prev_x, prev_y = x, y
        
        self.actions.release()
        self.actions.perform()
        
        print("Drew a heart using parametric equations! ❤️")
        
        time.sleep(3) 

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()