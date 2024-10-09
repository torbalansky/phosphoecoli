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

    def test_delete_protein(self):
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
        
        driver.find_element(By.NAME, "password").send_keys("password")
        driver.find_element(By.CSS_SELECTOR, ".custom-login-btn").click()

        WebDriverWait(driver, 10).until(EC.url_contains("/profile/"))

        target_protein_name = "test_protein"
        
        protein_cards = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.card"))
        )

        for card in protein_cards:
            if target_protein_name in card.find_element(By.CSS_SELECTOR, ".card-title").text:
                delete_button = card.find_element(By.CSS_SELECTOR, "a.delete-protein")

                driver.execute_script("arguments[0].scrollIntoView(true);", delete_button)

                WebDriverWait(driver, 10).until(
                    EC.visibility_of(delete_button)
                )

                # Check if the delete button is enabled and visible
                if delete_button.is_displayed() and delete_button.is_enabled():
                    driver.execute_script("arguments[0].click();", delete_button)

                    # Handle the confirmation alert
                    WebDriverWait(driver, 10).until(EC.alert_is_present()).accept()
                    print(f"{target_protein_name} deletion confirmed.")
                else:
                    print(f"{target_protein_name} delete button is not interactable.")
                break

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
