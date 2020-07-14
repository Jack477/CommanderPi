#!/bin/bash
problem=$(dpkg -s python3-tk|grep installed)
path=$(pwd)
echo $path
echo Checking for tkinter: $problem
if [ "" == "$problem" ]; then
	sudo apt-get install python3-tk
fi
sudo apt-get install python3-pil python3-pil.imagetk
sudo python3 c_desktop.py ${HOME}
sudo chmod +x ${HOME}/CommanderPi/src/start.sh
sudo chmod +x ${HOME}/Desktop/commanderpi.desktop
