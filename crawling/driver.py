from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

def get_chrome_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('incognito')
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver