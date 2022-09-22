import re
import time
import queue

from threading import Thread

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class King(object):
    def __init__(self, save_path: str = "") -> None:
        # Constructor variables
        self.save = save_path
        # Driver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)         
        self.driver.get('http://orteil.dashnet.org/cookieclicker/')

        # Class variables
        self.clicker_queue = queue.Queue()
        
        # Select language
        try:        
            lang = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="langSelectButton title"]'))
            )

        except:
            self.driver.quit()
            
        lang.click()
        
        # Wait for page to load
        while not re.search('loading', self.driver.page_source, re.IGNORECASE):
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//button[@id="bigCookie"]'))
            )

        # Load save
        if self.save:
            with open(self.save, 'r+') as file:
                self.save = file.read()
                
            self.__load_save()

    def __load_save(self):
        cond = self.driver.execute_script('return Game.bakeryName ')
        while not cond:
            cond = self.driver.execute_script('return Game.bakeryName ')
        
        self.driver.execute_script(f'Game.ImportSaveCode("{self.save}")')
    
    def click_cookie(self):
        try:
            cookie = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//button[@id="bigCookie"]'))
            )
        
        except:
            self.driver.quit()

        def cookie_clicker_thread(cookie):
            while True:
                if self.clicker_queue.empty():
                    cookie.click()
                
                time.sleep(0.1)

        thread = Thread(target=cookie_clicker_thread, args=(cookie,), daemon=True)
        thread.start()   

        
    
     