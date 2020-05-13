#!/bin/bash
problem=$(dpkg -s python3-tk|grep installed)
echo Checking for tkinter: $problem
if [ "" == "$problem" ]; then
	sudo apt-get install python3-tk
fi
sudo python3 c_desktop.py
