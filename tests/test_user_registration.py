import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.safari.service import Service as SafariService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class TestUserRegistration(unittest.TestCase):
    def setUp(self):
        service = Service('') # Set the browser type; you can change this to 'firefox', 'chrome', 'safari', or 'edge'
        self.driver = webdriver.Firefox(service=service) # Change to 'chrome', 'safari', or 'edge' as needed
        self.driver.get("https://pedb.onrender.com")

    def test_user_registration(self):
        driver = self.driver
        
        contribute_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "navbarDropdownContribute"))
        )
        contribute_link.click()

        register_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Register"))
        )
        register_link.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )

        driver.find_element(By.NAME, "username").send_keys("testuser")
        driver.find_element(By.NAME, "first_name").send_keys("Test")
        driver.find_element(By.NAME, "last_name").send_keys("User")
        driver.find_element(By.NAME, "email").send_keys("testuser@example.com")
        driver.find_element(By.NAME, "password1").send_keys("!Spassword123")
        driver.find_element(By.NAME, "password2").send_keys("!Spassword123")
        driver.find_element(By.NAME, "institution_name").send_keys("Test Institution")
        driver.find_element(By.NAME, "country").send_keys("Test Country")

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

        submit_button = driver.find_element(By.CSS_SELECTOR, ".register")
        driver.execute_script("arguments[0].click();", submit_button)

        WebDriverWait(driver, 10).until(EC.url_changes(driver.current_url))

        print("Redirected to:", driver.current_url)

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
