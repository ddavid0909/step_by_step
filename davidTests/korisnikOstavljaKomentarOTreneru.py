from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

chromedriver_path = "../chromedriver-mac-x64/chromedriver"

service = ChromeService(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service)

try:
    driver.maximize_window()
    driver.get("http://127.0.0.1:8000/")

    # Login as regular user
    username = driver.find_element(By.NAME, "username")
    username.send_keys("dd210102d@student.etf.bg.ac.rs")
    password = driver.find_element(By.NAME, "password")
    password.send_keys("123")
    submit = driver.find_element(By.XPATH, "//input[@type='submit' and @value='Uloguj se']")
    submit.click()

    time.sleep(2)

    # Navigate to "Ostavi komentar" page
    prikazi_trenera_link = driver.find_element(By.LINK_TEXT, "Ostavi komentar")
    prikazi_trenera_link.click()

    time.sleep(1)

    logout_link = driver.find_element(By.XPATH, "//a[@class='btn' and text()='LOG OUT']")
    driver.execute_script("arguments[0].scrollIntoView();", logout_link)

    first_radio_button = driver.find_elements(By.XPATH, "//input[@type='radio']")[0]
    driver.execute_script("arguments[0].scrollIntoView();", first_radio_button)

    time.sleep(1)
    
    first_radio_button.click()


    # Write a comment in the textarea
    textarea = driver.find_element(By.NAME, "komentar")
    textarea.send_keys("Ovo je moj komentar o treneru.")

    time.sleep(1)

    # Attempt to click the submit button (retry up to 3 times)
    submit_button = driver.find_element(By.XPATH, "//input[@type='submit' and @value='Ostavi komentar']")
    attempts = 0
    while attempts < 3:
        try:
            # Scroll to the top of the element
            driver.execute_script(
                "arguments[0].scrollIntoView({ behavior: 'auto', block: 'start', inline: 'nearest' });", submit_button)

            # Click the submit button using ActionChains
            ActionChains(driver).move_to_element(submit_button).perform()
            submit_button.click()
            break
        except Exception as e:
            attempts += 1
            print(f"Attempt {attempts}: {type(e).__name__} occurred. Retrying...")
            time.sleep(7)  # Adjust sleep time as needed

    if attempts == 3:
        print("Failed to click submit button after 3 attempts.")

    # Scroll to the logout link
    logout_link = driver.find_element(By.CLASS_NAME, "btn")
    driver.execute_script("arguments[0].scrollIntoView({ behavior: 'auto', block: 'start', inline: 'nearest' });",
                          logout_link)

    time.sleep(1)

    logout_link = driver.find_element(By.XPATH, "//a[@class='btn' and text()='LOG OUT']")
    driver.execute_script("arguments[0].scrollIntoView();", logout_link)

    time.sleep(1)
    # Click the logout link
    logout_link.click()


finally:
    driver.quit()
