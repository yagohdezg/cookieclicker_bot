import os
import matplotlib.pyplot as plt

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def main():
    # Intro text
    os.system('cls' if os.name == 'nt' else 'clear')
    title = 'Cookie Clicker optimisation program'
    dashes = 61
    print('-' * dashes)
    print(
        int((dashes - len(title)) / 2) * '-' + title + int((dashes - len(title)) / 2) * '-'
    )
    print('-' * dashes)
    
    # Configure selenium
    
    options = Options()
    options.headless = True
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    # Set secondary tasks
    with open('save.txt', 'r') as file: 
        save = file.read()
    
    # Start driver and load save
    driver.get("http://orteil.dashnet.org/cookieclicker/")
    cond = driver.execute_script('return Game.bakeryName ')
    while not cond:
        cond = driver.execute_script('return Game.bakeryName ')
        
    driver.execute_script(f'Game.ImportSaveCode("{save}")')
    
    # Read dict
    buildings = driver.execute_script(
                'var cps = {};Object.keys(Game.Objects).forEach(function(key)'+\
                '{cps[key] = Game.Objects["key"].cps(Game.Objects["key"])});return cps'
            )
    
    print(buildings)

if __name__ == '__main__':
    main()