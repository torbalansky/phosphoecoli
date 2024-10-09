import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.safari.service import Service as SafariService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class TestUserRegistration(unittest.TestCase):
    def setUp(self):
        service = Service('') # Set the browser type; you can change this to 'firefox', 'chrome', 'safari', or 'edge'
        self.driver = webdriver.Firefox(service=service) # Change to 'chrome', 'safari', or 'edge' as needed
        self.driver.get("https://pedb.onrender.com")

    def test_update_protein(self):
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

        target_protein_name = "protein"
        
        protein_cards = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.card"))
        )

        for card in protein_cards:
            if target_protein_name in card.find_element(By.CSS_SELECTOR, ".card-title").text:
                update_protein = card.find_element(By.CSS_SELECTOR, 'a[title="Edit"]')

                driver.execute_script("arguments[0].scrollIntoView(true);", update_protein)
                WebDriverWait(driver, 10).until(
                    EC.visibility_of(update_protein)
                )

                if update_protein.is_displayed() and update_protein.is_enabled():
                    driver.execute_script("arguments[0].click();", update_protein)

                    WebDriverWait(driver, 10).until(EC.url_contains("/update_phosphoprotein/"))
                    WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.NAME, "uniprot_code"))
                    )

                    driver.find_element(By.NAME, "uniprot_code").clear()
                    driver.find_element(By.NAME, "uniprot_code").send_keys("updated_protein_code")
                    
                    driver.find_element(By.NAME, "gene_name").clear()
                    driver.find_element(By.NAME, "gene_name").send_keys("updated_protein_gene_name")

                    driver.find_element(By.NAME, "protein_name").clear()
                    driver.find_element(By.NAME, "protein_name").send_keys("updated_protein_name")

                    driver.find_element(By.NAME, "position").clear()
                    driver.find_element(By.NAME, "position").send_keys("2")

                    driver.find_element(By.NAME, "window_5_aa").clear()
                    driver.find_element(By.NAME, "window_5_aa").send_keys("AAAAAXAAAAA")

                    driver.find_element(By.NAME, "method").clear()
                    driver.find_element(By.NAME, "method").send_keys("updated_method")

                    modification_type_input = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.NAME, "modification_type"))
                    )
                    
                    driver.execute_script("arguments[0].scrollIntoView(true);", modification_type_input)
                    WebDriverWait(driver, 10).until(EC.visibility_of(modification_type_input))

                    driver.execute_script("arguments[0].value = '';", modification_type_input)
                    modification_type_input.send_keys("T")

                    reference_input = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.NAME, "reference"))
                    )
                    
                    driver.execute_script("arguments[0].scrollIntoView(true);", reference_input)
                    WebDriverWait(driver, 10).until(EC.visibility_of(reference_input))

                    driver.execute_script("arguments[0].value = '';", reference_input)
                    reference_input.send_keys("PMID:UPDATED123")

                    submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
                    driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
                    
                    WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable(submit_button)
                    )

                    driver.execute_script("arguments[0].click();", submit_button)

                    print(f"Updated protein details for {target_protein_name} successfully.")
                else:
                    print(f"{target_protein_name} edit button is not interactable.")
                break

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
