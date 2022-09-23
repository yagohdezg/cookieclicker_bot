import os
import time
from modules import king

def main():
    manager = king.King(save_path="")
    time.sleep(100)
    manager.kill()

if __name__ == '__main__':
    main()