#!/usr/bin/python
import sys
import os
import subprocess as sp
from os.path import expanduser

user = sys.argv[1]
home_path = expanduser("~%s" % user)

dir_path = os.path.dirname(os.path.realpath(__file__))

print(dir_path)
f_content = "[Desktop Entry]\nName=CommanderPi\nComment=System info and overclocking\nExec="+dir_path+"/src/start.sh\nIcon="+dir_path+"/src/icons/Icon.png\nCategories=Utility;\nVersion=1.0\nType=Application\nTerminal=false\nStartupNotify=true"
print(f_content)

d_dir = home_path+"/Desktop/commanderpi.desktop"
x_dir = "/usr/share/applications/commanderpi.desktop"

print("Save desktop shortcut to %s" % d_dir)
try:
    f = open(d_dir, "w")
except FileNotFoundError:
    print("Couldn't create desktop shortcut!")
else:
    with f:
        f.write(f_content)


print("Save menu shortcut to %s" % x_dir)
try:
    f2 = open(x_dir, "w")
except FileNotFoundError:
    print("Couldn't create menu shortcut!")
else:
    with f2:
        f2.write(f_content)
