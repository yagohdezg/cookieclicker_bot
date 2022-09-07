import os
import copy

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

class Buildings(object):
    def __init__(self, save: str) -> None:
        self.save = save
        self.buildings = {}
        self.cps_multiplier = 0
        
        self.__download_data()
        
    def __download_data(self):
        # Configure selenium
        options = Options()
        options.headless = True
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        # Wait for page to load
        driver.get("http://orteil.dashnet.org/cookieclicker/")
        cond = driver.execute_script('return Game.bakeryName ')
        while not cond:
            cond = driver.execute_script('return Game.bakeryName ')
            
        # Obtain data
        driver.execute_script(f'Game.ImportSaveCode("{self.save}")')
        buildings = driver.execute_script('return Object.keys(Game.Objects)')
        self.cps_multiplier = driver.execute_script('return Game.globalCpsMult')
        
        quantities = {
            'amount': driver.execute_script(
                'var amount = {};Object.keys(Game.Objects).forEach(function(key)'+\
                '{amount[key] = Game.Objects[key]["amount"]});return amount'
            ),
            
            'price': driver.execute_script(
                'var price = {};Object.keys(Game.Objects).forEach(function(key)'+\
                '{price[key] = Game.Objects[key]["price"]});return price'
            ),
            
            'cps': driver.execute_script(
                'var cps = {};Object.keys(Game.Objects).forEach(function(key)'+\
                '{cps[key] = Game.Objects[key].cps(Game.Objects[key])});return cps'
            )
        }
        
        for building in buildings:
            self.buildings[building] = {}
            for key in quantities:
                self.buildings[building][key] = quantities[key][building]

    def best_next_building(self, _dict: dict):
        ratios = {}
        for key, item in _dict.items():
            ratios[key] = (item["cps"] * self.cps_multiplier) / item["price"]
            
        _max = max(ratios, key=lambda key: ratios[key])
        
        return _max
    
    def best_next_n_buildings(self, n: int):
        buildings = copy.deepcopy(self.buildings)
        
        for k in range(n):
            next = self.best_next_building(buildings)
            buildings[next]['amount'] += 1
            buildings[next]['price'] *= 1.15
            
            yield next, buildings[next]['amount']
            
def main():
    with open('save.txt', 'r') as file: 
        save = file.read()
    buildings = Buildings(save)
    
    for i, val in enumerate(buildings.best_next_n_buildings(50)):
        print(f'{i}: {val}')

if __name__ == '__main__':
    main()
        