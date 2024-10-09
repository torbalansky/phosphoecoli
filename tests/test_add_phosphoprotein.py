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

    def test_user_login(self):
        driver = self.driver

        contribute_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "navbarDropdownContribute"))
        )
        contribute_link.click()

        login_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Login"))
        )
        login_link.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        driver.find_element(By.NAME, "username").send_keys("username")
        driver.find_element(By.NAME, "password").send_keys("password")

        submit_button = driver.find_element(By.CSS_SELECTOR, ".custom-login-btn")
        driver.execute_script("arguments[0].click();", submit_button)

        WebDriverWait(driver, 10).until(
            EC.url_contains("/profile/")
        )
 
        add_phosphoprotein_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-success.profile"))
        )

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "uniprot_code"))
        )
        driver.find_element(By.NAME, "uniprot_code").send_keys("P0TEST")
        driver.find_element(By.NAME, "gene_name").send_keys("test_gene")
        driver.find_element(By.NAME, "protein_name").send_keys("test_protein")
        driver.find_element(By.NAME, "position").clear()
        driver.find_element(By.NAME, "position").send_keys("10")
        driver.find_element(By.NAME, "window_5_aa").send_keys("AAAAASAAAAA")
        driver.find_element(By.NAME, "method").send_keys("HTP-MS")
        driver.find_element(By.NAME, "modification_type").send_keys("S")
        driver.find_element(By.NAME, "reference").send_keys("PMID:TEST123")

        add_phosphoprotein_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        driver.execute_script("arguments[0].scrollIntoView(true);", add_phosphoprotein_button)
        driver.execute_script("arguments[0].click();", add_phosphoprotein_button)

        print("Phosphoprotein added successfully. Current URL:", driver.current_url)

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
