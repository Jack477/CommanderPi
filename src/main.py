#!/usr/bin/python
import gui as g
import tkinter as tk
import resources as rs
import os
import sys
from tkinter import *
### this trick should fix missing file problem for update from 0.7.2 to 1.0
if not os.path.exists(rs.home_path+"/CommanderPi/src/icons/Gpu.png"):
    os.system("( cd ~ && rm -r "+rs.home_path+"/CommanderPi )")
    os.system("( cd ~ && git clone https://github.com/Jack477/CommanderPi "+rs.home_path+"/CommanderPi )")
    os.system("( cd ~ && sudo chown -R pi "+rs.home_path+"/CommanderPi )")
    os.system("( cd ~ && sudo chmod +x "+rs.home_path+"/CommanderPi/src/start.sh )")
    os.system("( cd ~ && sudo chmod +x "+rs.home_path+"/CommanderPi/install.sh )")
    os.system("( cd "+rs.home_path+"/CommanderPi && runuser -u pi -- ./install.sh )")

    sys.exit(0)


def main():
    start = g.Window()
	
	
if __name__ == '__main__':
    main()
