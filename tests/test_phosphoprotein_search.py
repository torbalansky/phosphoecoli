import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.safari.service import Service as SafariService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope="module")
def driver():
    service = Service('') # Set the browser type; you can change this to 'firefox', 'chrome', 'safari', or 'edge'
    driver = webdriver.Firefox(service=service) # Change to 'chrome', 'safari', or 'edge' as needed
    yield driver
    driver.quit()

def test_search_by_uniprot_code(driver):
    driver.get("https://pedb.onrender.com/protein_list/")

    search_bar = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "q"))
    )
    search_bar.send_keys("P30138")

    search_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@class='btn btn-primary']"))
    )
    search_button.click()

    view_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'btn btn-light') and text()='View']"))
    )
    view_button.click()

    uniprot_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'uniprotkb/P30138')]"))
    )
    assert uniprot_link.is_displayed(), "UniProt link P30138 not found."
    print("UniProt link P30138 found!")

def test_search_by_protein_name(driver):
    driver.get("https://pedb.onrender.com/protein_list/")

    search_bar = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "q"))
    )
    search_bar.send_keys("Isocitrate dehydrogenase [NADP]")

    search_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@class='btn btn-primary']"))
    )
    search_button.click()
    results = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//tr[contains(@data-protein-url, '')]"))
    )
    assert len(results) > 0, "No results found for protein name."
    print("Search results displayed for protein name.")

def test_search_by_protein_name_and_strain(driver):
    driver.get("https://pedb.onrender.com/protein_list/")
    search_bar = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "q"))
    )
    search_bar.send_keys("Isocitrate dehydrogenase [NADP]")

    coli_strain_dropdown = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "coli_strain"))
    )
    coli_strain_dropdown.click()
    
    coli_strain_option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//option[text()='Escherichia coli K12']"))
    )
    coli_strain_option.click()

    search_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@class='btn btn-primary']"))
    )
    search_button.click()

    results = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//tr[contains(@data-protein-url, '')]"))
    )
    assert len(results) > 0, "No results found for protein name and E. coli strain."
    print("Search results displayed for protein name and E. coli strain.")

