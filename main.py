import os
import time
from modules import king

def main():
    manager = king.King(save_path="save.txt")
    time.sleep(4294967)
    manager.kill()

if __name__ == '__main__':
    main()