import os
import time
from modules import king

def main():
    manager = king.King(save_path="")
    time.sleep(3)
    manager.start_clicking_cookie()
    print(list(manager.buildings.best_next_n_buildings(100)))
    time.sleep(100)
    manager.kill()

if __name__ == '__main__':
    main()