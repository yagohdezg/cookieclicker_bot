import os
import time
from modules import king

def main():
    manager = king.King(save_path="save.txt")
    manager.click_cookie()

    time.sleep(100)

if __name__ == '__main__':
    main()