#!/bin/sh
problem=$(dpkg -s python3-tk|grep installed)
path=$(pwd)
echo $path
echo Checking for tkinter: $problem
sudo pip3 install psutil
sudo apt-get install git python3-tk python3-pil python3-pil.imagetk
sudo python3 c_desktop.py $USER
sudo chown $USER ~/Desktop/commanderpi.desktop
sudo chmod +x ${path}/src/start.sh
sudo chmod +x ${HOME}/Desktop/commanderpi.desktop
