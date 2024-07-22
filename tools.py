import time
import random
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException

def human_delay():
    time.sleep(random.uniform(2, 4))


def human_writing(element, text):
    for char in text:
        try:
            element.send_keys(char)
            time.sleep(random.uniform(0.01, 0.1))
        except Exception as e:
            print(f"We can't write this char: {char} because: {e}")


def authenticate_agent(driver, cookies, link=None):
    human_delay()
    if link:
        driver.get(link)
        human_delay()
    for cookie in cookies:
        try:
            driver.add_cookie(cookie)
        except Exception as e:
            print(f"Failed to add cookie {cookie}: {e}")
    return driver


def get_cookies(path=None):
    if path:
        with open(path, "r", encoding="utf-8") as file:
            lines = file.read().split("\n")

    return_cookies = []
    for line in lines:
        split = line.split("\t")
        if len(split) < 6:
            continue

        split = [x.strip() for x in split]

        try:
            split[4] = int(split[4])
        except ValueError:
            split[4] = None

        return_cookies.append(
            {
                "name": split[5],
                "value": split[6],
                "domain": split[0],
                "path": split[2],
            }
        )

        if split[4]:
            return_cookies[-1]["expiry"] = split[4]
    return return_cookies


def save_accounts(usernames, path):
    with open(path, "w") as file:
        json.dump(usernames, file, indent=4)
        
def click_checkbox_container(wait):
    username_container_xpath = '//*[@id="fullScreenComposerMountPoint"]/div/div/div/div/div/div[2]/div/div[1]/div/div/div/div[1]/div[2]/div[1]/div/div/input'
    username_container = wait.until(EC.presence_of_element_located((By.XPATH, username_container_xpath)))
    username_container.click()



def extract_usernames(wait, driver):
 
    # Click the input 
    click_checkbox_container(wait)
    
    # Let's extract the usernames 
    time.sleep(3)
    
    main_div_xpath = '//*[@id="fullScreenComposerMountPoint"]/div/div/div/div/div/div[2]/div/div[1]/div/div/div/div[1]/div[2]/div[2]/div[1]/div/div[1]/div'
    username_elements = driver.find_elements(By.XPATH, f"{main_div_xpath}//div[contains(@class, 'vk-ProfileListItemTitle')]")

    print(f"Found {len(username_elements)} usernames")
    
    # Extract the usernames and remove duplicates
    usernames = []
    seen_usernames = set()
    for element in username_elements:
        username = element.text
        if username not in seen_usernames:
            seen_usernames.add(username)
            usernames.append({"username": username})
    
    
    # Check the first username's checkbox for demonstration
    return usernames

def checkbox_username(username, driver):
    try:
        time.sleep(8)
        # Find the checkbox using the aria-label attribute
        checkbox_xpath = f'//input[@aria-label="{username} TikTok Business profile"][@type="checkbox"]'
        checkbox = driver.find_element(By.XPATH, checkbox_xpath)
        
        # Scroll into view
        driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)
        
        # Optionally, wait for any animations or transitions
        time.sleep(1)
        
        # Click the checkbox using JavaScript
        driver.execute_script("arguments[0].click();", checkbox)
        print(f"Checkbox clicked for username: {username}")
    except NoSuchElementException:
        print(f"No checkbox found for username: {username}")
    except ElementClickInterceptedException:
        print(f"Element click intercepted for username: {username}")