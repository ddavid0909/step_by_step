from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import os
import time


chromedriver_path = "../chromedriver-mac-x64/chromedriver"


service = ChromeService(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service)
file_path = "/Users/fafulja/Desktop/lokalni_repozitorijum/project_Cetiri_amigosa/DOKUMENTACIJA/Faza5/djangoProject/slike_trenera/1-01.jpg"

try:
    driver.maximize_window()
    driver.get("http://127.0.0.1:8000/")

    username = driver.find_element(By.NAME, "username")
    username.send_keys("admin")
    password = driver.find_element(By.NAME, "password")
    password.send_keys("admin")
    submit = driver.find_element(By.XPATH, "//input[@type='submit' and @value='Uloguj se']")
    submit.click()

    time.sleep(2)

    treneri_div = driver.find_element(By.XPATH,"//div[contains(text(), 'Treneri')]")
    treneri_div.click()

    time.sleep(2)

    uredi_link = driver.find_element(By.XPATH, "//a[@href='/urediTrenera' and text()='Uredi']")
    driver.execute_script("arguments[0].scrollIntoView();", uredi_link)
    uredi_link.click()

    time.sleep(2)

    first_radio_button = driver.find_elements(By.XPATH, "//input[@type='radio']")[1]
    driver.execute_script("arguments[0].scrollIntoView();", first_radio_button)

    time.sleep(1)

    first_radio_button.click()

    uredi_button = driver.find_element(By.XPATH, "//input[@type='submit' and @value='Izaberi']")
    driver.execute_script("arguments[0].scrollIntoView(true);", uredi_button)

    time.sleep(2)

    uredi_button.click()

    time.sleep(2)

    checkboxes = driver.find_elements(By.XPATH, "//input[@type='checkbox']")
    for index, checkbox in enumerate(checkboxes):
        if index == 0 or index % 2 == 1:
            driver.execute_script("arguments[0].scrollIntoView();", checkbox)
            time.sleep(0.5)
            checkbox.click()
            time.sleep(0.5)

    file_input = driver.find_element(By.ID, "image")
    time.sleep(0.5)
    # Send the file path to the input element
    file_input.send_keys(file_path)
    time.sleep(0.5)

    potvrdi = driver.find_element(By.XPATH, "//input[@type='submit' and @value='Potvrdi promenu']")
    driver.execute_script("arguments[0].scrollIntoView(true);", potvrdi)

    time.sleep(0.5)

    potvrdi.click()

    time.sleep(5)

    logout_link = driver.find_element(By.XPATH, "//a[@class='btn' and text()='LOG OUT']")
    driver.execute_script("arguments[0].scrollIntoView();", logout_link)

    time.sleep(4)

    logout_link.click()

    time.sleep(2)

finally:
    # Close the browser
    driver.quit()