from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

def create_driver():
    options = webdriver.ChromeOptions()
    
    # Add desired options
    options.add_argument("--start-maximized")  # Set the window full screen
    # Set up the Chrome driver using ChromeDriverManager
    driver_path = ChromeDriverManager().install()
    service = Service(driver_path)
    
    driver = webdriver.Chrome(service=service, options=options)
    return driver
