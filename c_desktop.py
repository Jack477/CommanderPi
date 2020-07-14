#!/usr/bin/python
import sys
import os 
import subprocess as sp
home_path = sys.argv[1]
dir_path = os.path.dirname(os.path.realpath(__file__))
f_content = "[Desktop Entry]\nName=CommanderPi\nComment=System info and overclocking\nExec="+home_path+"/CommanderPi/src/start.sh\nIcon="+home_path+"/CommanderPi/src/icon.png\nCategories=Utility;\nVersion=1.0\nType=Application\nTerminal=false\nStartupNotify=true"
d_dir = home_path+"/Desktop/commanderpi.desktop"
x_dir = "/usr/share/applications/commanderpi.desktop"
print(d_dir)
f = open(d_dir, "w+")
f.write(f_content)
f.close
f2 = open(x_dir, "w+")
f2.write(f_content)
f2.close
