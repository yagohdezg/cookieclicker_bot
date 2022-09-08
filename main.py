import re
import time

from threading import Thread

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def main():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service) 
    
    driver.get('http://orteil.dashnet.org/cookieclicker/')
    
    try:        
        lang = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="langSelectButton title"]'))
        )

    except:
        driver.quit()
        
    lang.click()
    
    while not re.search('loading', driver.page_source, re.IGNORECASE):
        time.sleep(0.1)
        
    try:
        cookie = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//button[@id="bigCookie"]'))
        )
    
    except:
        driver.quit()
    
    
    def click_cookie(cookie):
        while True:
            cookie.click()
            time.sleep(0.1)
    
    thread = Thread(target=click_cookie, args=(cookie,), daemon=True)
    thread.start()    
    
    with open('source.html', 'w+') as file:
        file.write(driver.page_source)
    time.sleep(100)
    
if __name__ == '__main__':
    main()