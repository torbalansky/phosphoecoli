import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.safari.service import Service as SafariService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestUserRegistration(unittest.TestCase):
    def setUp(self):
        service = Service('') # Set the browser type; you can change this to 'firefox', 'chrome', 'safari', or 'edge'
        self.driver = webdriver.Firefox(service=service) # Change to 'chrome', 'safari', or 'edge' as needed
        self.driver.get("https://pedb.onrender.com")

    def test_delete_user(self):
        driver = self.driver

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "navbarDropdownContribute"))
        ).click()

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Login"))
        ).click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        ).send_keys("username")
        
        driver.find_element(By.NAME, "password").send_keys("passwor")
        driver.find_element(By.CSS_SELECTOR, ".custom-login-btn").click()

        WebDriverWait(driver, 10).until(EC.url_contains("/profile/"))

        delete_account_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "deleteAccount"))
        )

        driver.execute_script("arguments[0].scrollIntoView(true);", delete_account_button)

        delete_account_button.click()

        WebDriverWait(driver, 10).until(EC.alert_is_present()).accept()
        print("User account deletion confirmed.")

        WebDriverWait(driver, 10).until(EC.url_changes(driver.current_url))

        self.assertEqual(driver.current_url, "https://pedb.onrender.com/", "User should be redirected to the home page after account deletion.")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
