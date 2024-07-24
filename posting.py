from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from tools import human_writing, save_accounts, extract_usernames, checkbox_username, click_checkbox_container
import time
import json

class Posting:
    
    def __init__(self, driver, description, video_link, iteration=1):
        self.driver = driver
        self.wait = WebDriverWait(driver, 100)
        self.description = description
        self.video_link = video_link
        self.iteration = iteration

        self.do_post()
        
        # self.redirect_to_post()
        # self.post_video()
        
        time.sleep(500)
    
        
        
    def do_post(self):
        
        self.redirect_to_post()
        usernames = extract_usernames(self.wait, self.driver)
        usernames_len = len(usernames)
               
        if usernames:
            save_accounts(usernames, "usernames.json")
            checkbox_username(usernames[0]['username'], self.driver)
        else:
            print("No usernames found")
            return
        
        already_used =  []
        
        for i in range(usernames_len):
            
            
            
            self.create_post()
            time.sleep(10)
            self.post_video()
            
            click_checkbox_container(self.wait)
            
            checkbox_username(usernames[0]['username'], self.driver)
            
            already_used.append(usernames[0])
            
            usernames = usernames[1:]
            
            save_accounts(already_used, "already_used.json")
            
            if usernames:
                self.driver.get("https://hootsuite.com/dashboard")
                self.redirect_to_post()
                click_checkbox_container(self.wait)
                
                save_accounts(usernames, "usernames.json")
                checkbox_username(usernames[0]['username'], self.driver)
                
            else:
                print("we do for all the usernames")
                
                save_accounts(usernames, "usernames.json")
                time.sleep(3)
                self.driver.close()
                return
            
           
            
        
    def redirect_to_post(self):
        creer_post_button_xpath = '//*[@id="secondaryView"]/div/div/header/div[2]/div[2]/button'
        creer_post_button = self.wait.until(EC.presence_of_element_located((By.XPATH, creer_post_button_xpath)))
        creer_post_button.click()
        
    def create_post(self):
        # Write the description
        description_xpath = '//*[@id="message-edit-content-tiktok"]/div[1]/div[1]/div[2]/div'
        description_field = self.wait.until(EC.presence_of_element_located((By.XPATH, description_xpath)))
        human_writing(description_field, self.description)
        
        # Post video process
        # Click in the button container
        try:
            post_button_container_xpath = '//*[@id="message-edit-content-tiktok"]/div[2]/div[2]/div/div[1]/div/div[1]/div/div/div/div/div/div[1]/div/button'
            post_button_container = self.wait.until(EC.presence_of_element_located((By.XPATH, post_button_container_xpath)))
            post_button_container.click()
        except Exception as e:
            print(f"Failed to click in the button container because: {e}")
                
        # Load the video 
        load_input_xpath = '//*[@id="message-edit-content-tiktok"]/div[2]/div[2]/div/div[1]/div/div[1]/div/div/input'
        load_input = self.wait.until(EC.presence_of_element_located((By.XPATH, load_input_xpath)))
        load_input.send_keys(self.video_link)
        
        contains_mp4_xpath = '//*[contains(@id, "mp4")]/span/div'
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH, contains_mp4_xpath)))
            print("Element containing 'mp4' in its id appeared")
        except TimeoutException:
            print("Timeout waiting for element containing 'mp4' in its id")
            
        # time.sleep(800)
        
    def post_video(self):
                
        if self.iteration <= 1:  
            post_button_xpath = '//*[@id="fullScreenComposerMountPoint"]/div/div/div/div/div/div[3]/div[2]/button'
            post_button = self.wait.until(EC.presence_of_element_located((By.XPATH, post_button_xpath)))
            post_button.click()    
        else:
            for i in range(self.iteration):
                if i == 0:
                    # Click the container
                    post_button_container_xpath = '//*[@id="fullScreenComposerMountPoint"]/div/div/div/div/div/div[3]/div[2]/div/div[1]/button'
                    post_button_container = self.wait.until(EC.presence_of_element_located((By.XPATH, post_button_container_xpath)))
                    post_button_container.click()
                    time.sleep(2)
                    # Click the post duplicate button
                    post_duplicate_css_selector = '/html/body/div[13]/div/div/div/div/div/div[3]/div[2]/div/div[2]/div/ul/li[2]'
                    try:
                        post_duplicate = self.wait.until(EC.presence_of_element_located((By.XPATH, post_duplicate_css_selector)))
                        post_duplicate.click()      
                    except TimeoutException as e:
                        print(f"Failed to click the post duplicate button because: {e}")
                        
                else:
                    # Click the post duplicate button
                    post_duplicate_xpath = '//*[@id="fullScreenComposerMountPoint"]/div/div/div/div/div/div[3]/div[2]/button'
                    post_duplicate = self.wait.until(EC.presence_of_element_located((By.XPATH, post_duplicate_xpath)))
                    post_duplicate.click()
                       
                time.sleep(60)           

