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

class TestSendEmail(unittest.TestCase):
    def setUp(self):
        service = Service('') # Set the browser type; you can change this to 'firefox', 'chrome', 'safari', or 'edge'
        self.driver = webdriver.Firefox(service=service) # Change to 'chrome', 'safari', or 'edge' as needed
        self.driver.get("https://pedb.onrender.com/contact/")

    def test_send_email(self):
        driver = self.driver

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "name"))
        )

        driver.find_element(By.NAME, "name").send_keys("name")
        driver.find_element(By.NAME, "email").send_keys("email@test.com")
        driver.find_element(By.NAME, "content").send_keys("content")

        submit_button = driver.find_element(By.CSS_SELECTOR, ".btn-block")
        driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-block")))
        driver.execute_script("arguments[0].click();", submit_button)

        time.sleep(2)

        try:
            success_message = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".alert-success"))
            )
            print("Success message found:", success_message.text)
        except Exception as e:
            print("Success message not found. Error:", e)
            print("Current URL:", driver.current_url)

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "content"))
            )
            print("Form is still present after submission.")
        except Exception as e:
            print("Form is no longer present. Error:", e)

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
