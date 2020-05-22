#!/usr/bin/python
import os 
import subprocess as sp
dir_path = os.path.dirname(os.path.realpath(__file__))
f_content = '[Desktop Entry]\nName=CommanderPi\nComment=System info and overclocking\nExec=/home/pi/Commander_Pi/src/start.sh\nIcon=/home/pi/Commander_Pi/src/logo.png\nCategories=Utility;\nVersion=1.0\nType=Application\nTerminal=false\nStartupNotify=true'
d_dir = "/home/pi/Desktop/test.desktop"
x_dir = "/usr/share/applications/test.desktop"
print(d_dir)
f = open(d_dir, "w+")
f.write(f_content)
f.close
f2 = open(x_dir, "w+")
f2.write(f_content)
f2.close
