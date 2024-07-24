from driver import create_driver
from tools import authenticate_agent, get_cookies, human_writing, human_delay
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def add_information(driver, email, password):
    # Define XPaths for email and password fields
    email_xpath = '//*[@id="loginEmailInput"]'
    password_xpath = '//*[@id="loginPasswordInput"]'
    confirm_xpath = "/html/body/div[1]/div[2]/div/div[1]/form/button"

    # Find the email input field and enter the email
    email_field = driver.find_element(By.XPATH, email_xpath)
    email_field.clear()
    human_writing(email_field, email)

    # Find the password input field and enter the password
    password_field = driver.find_element(By.XPATH, password_xpath)
    password_field.clear()
    human_writing(password_field, password)

    # Optionally, you can press Enter to submit the form

    human_delay()

    confirm_button = driver.find_element(By.XPATH, confirm_xpath)
    confirm_button.click()


def authentificate(link, username, password):

    driver = create_driver()

    driver.get(link)

    add_information(driver, username, password)


    return driver
