from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import os
import time


chromedriver_path = "../chromedriver-mac-x64/chromedriver"


service = ChromeService(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service)

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

    prikazi_trenera_link = driver.find_element(By.LINK_TEXT, "Komentari")
    prikazi_trenera_link.click()

    odobri_button = driver.find_element(By.XPATH, "//input[@type='submit' and @value='Odobri!']")
    driver.execute_script("arguments[0].scrollIntoView(true);", odobri_button)

    time.sleep(2)

    odobri_button.click()


    alert = driver.switch_to.alert
    alert.accept()

    time.sleep(3)

    logout_link = driver.find_element(By.XPATH, "//a[@class='btn' and text()='LOG OUT']")
    driver.execute_script("arguments[0].scrollIntoView();", logout_link)

    time.sleep(4)

    logout_link.click()

    time.sleep(2)

finally:
    # Close the browser
    driver.quit()