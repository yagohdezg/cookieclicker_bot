import copy
import queue
import time

from threading import Thread
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import (
    JavascriptException
)

class Buildings(object):
    def __init__(self, driver: webdriver.Chrome, clicker_queue: queue.Queue) -> None:
        self.driver = driver
        self.clicker_queue = clicker_queue
        self.buildings = {}
        self.cps_multiplier = 0
        
        # Useful functions
        self.wait = WebDriverWait(self.driver, 10, 1, ignored_exceptions=JavascriptException)
        
        self.__download_data()
        self.__start_buying()
        
    def __download_data(self):
        
        buildings = self.wait.until(
            lambda browser: browser.execute_script('return Object.keys(Game.Objects)'))
            
        self.cps_multiplier = self.wait.until(
            lambda browser: browser.execute_script('return Game.globalCpsMult'))
        
        quantities = {
            'amount': self.wait.until(lambda browser: browser.execute_script(
                'var amount = {};Object.keys(Game.Objects).forEach(function(key)'+\
                '{amount[key] = Game.Objects[key]["amount"]});return amount'
            )),
            
            'price': self.wait.until(lambda browser: browser.execute_script(
                'var price = {};Object.keys(Game.Objects).forEach(function(key)'+\
                '{price[key] = Game.Objects[key]["price"]});return price'
            )),
            
            'cps': self.wait.until(lambda browser: browser.execute_script(
                'var cps = {};Object.keys(Game.Objects).forEach(function(key)'+\
                '{cps[key] = Game.Objects[key].cps(Game.Objects[key])});return cps'
            ))
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
    
    # def best_next_n_buildings(self, n: int):
    #     buildings = copy.deepcopy(self.buildings)
        
    #     for k in range(n):
    #         next = self.best_next_building(buildings)
                        
    #         yield next, buildings[next]['price']
            
    #         buildings[next]['amount'] += 1
    #         buildings[next]['price'] *= 1.15
            
    def __start_buying(self):
        def worker_buyer_thread():
            while True:
                if self.clicker_queue.empty():
                    next = self.best_next_building(self.buildings)
                    capital = self.driver.execute_script('return Game.cookies')
                    
                    if capital >= self.buildings[next]['price']:
                        self.clicker_queue.put(
                            '//div[@id="product{id}"]'.format(
                                id=list(self.buildings.keys()).index(next)))
                        
                        self.add_building(next)
                                   
                time.sleep(1)
                
        thread = Thread(target=worker_buyer_thread, args=(), daemon=True)
        thread.start() 
        
    def add_building(self, building: str):
        self.buildings[building]['amount'] += 1
        self.buildings[building]['price'] *= 1.15
        
    def get_buildings(self):
        return self.buildings