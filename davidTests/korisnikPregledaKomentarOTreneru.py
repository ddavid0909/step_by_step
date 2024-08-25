from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import time

chromedriver_path = "../chromedriver-mac-x64/chromedriver"

service = ChromeService(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service)

try:
    driver.maximize_window()
    driver.get("http://127.0.0.1:8000/")

    username = driver.find_element(By.NAME, "username")
    username.send_keys("dd210102d@student.etf.bg.ac.rs")
    password = driver.find_element(By.NAME, "password")
    password.send_keys("123")
    submit = driver.find_element(By.XPATH, "//input[@type='submit' and @value='Uloguj se']")
    submit.click()

    time.sleep(2)

    prikazi_trenera_link = driver.find_element(By.LINK_TEXT, "Komentari")  # Adjust the link text as needed
    prikazi_trenera_link.click()

    time.sleep(2)


    # Locate the trainer links
    treneri_links = driver.find_elements(By.XPATH, "//a[contains(@href, '/trenerKorisnik')]")
    if treneri_links:
        link_to_click = treneri_links[0]

        # Scroll to the element
        driver.execute_script("arguments[0].scrollIntoView();", link_to_click)

        # Wait for the element to be clickable
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/trenerKorisnik')]")))

        # Retry mechanism to handle potential interception issues
        attempts = 0
        while attempts < 3:
            try:
                link_to_click.click()
                break  # Exit loop if click is successful
            except Exception as e:
                #print(f"Attempt {attempts + 1} failed with error: {e}")
                time.sleep(2)  # Wait before retrying
                attempts += 1
                # Scroll again to ensure the element is in view
                driver.execute_script("arguments[0].scrollIntoView();", link_to_click)

        if attempts == 3:
            print("Neuspio klik.")
        else:
            time.sleep(2)
    else:
        print("Nema trenera")

    logout_link = driver.find_element(By.XPATH, "//a[@class='btn' and text()='LOG OUT']")
    driver.execute_script("arguments[0].scrollIntoView();", logout_link)

    time.sleep(5)

    logout_link.click()

    time.sleep(2)

finally:
    driver.quit()
