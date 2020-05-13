#!/usr/bin/python
import os 
import subprocess as sp
dir_path = os.path.dirname(os.path.realpath(__file__))
f_content = '[Desktop Entry]\nEncoding=UTF-8\nName=Commander Pi\nComment=System info and overclocking\nExec=lxterminal -e "/home/pi/Commander_Pi/src/start.sh"\nIcon=/home/pi/Commander_Pi/src/build/logo.png\nCategories=Application;\nVersion=1.0\nType=Application\nTerminal=true'
d_dir = "/home/pi/Desktop/Commander.desktop"
print(d_dir)
f = open(d_dir, "w+")
f.write(f_content)
f.close
