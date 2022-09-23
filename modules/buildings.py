import copy
import time

from selenium import webdriver
from selenium.common.exceptions import (
    JavascriptException
)


class Buildings(object):
    def __init__(self, driver: webdriver.Chrome) -> None:
        self.driver = driver
        self.buildings = {}
        self.cps_multiplier = 0
        
        self.__download_data()
        
    def __download_data(self):
        cond = True
        while cond:
            try:
                buildings = self.driver.execute_script('return Object.keys(Game.Objects)')
                cond = False
            except JavascriptException:
                print("Game not loaded, retrying in 0.5s")
                
            time.sleep(0.5)
            
        self.cps_multiplier = self.driver.execute_script('return Game.globalCpsMult')
        print(self.cps_multiplier)
        
        quantities = {
            'amount': self.driver.execute_script(
                'var amount = {};Object.keys(Game.Objects).forEach(function(key)'+\
                '{amount[key] = Game.Objects[key]["amount"]});return amount'
            ),
            
            'price': self.driver.execute_script(
                'var price = {};Object.keys(Game.Objects).forEach(function(key)'+\
                '{price[key] = Game.Objects[key]["price"]});return price'
            ),
            
            'cps': self.driver.execute_script(
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
            