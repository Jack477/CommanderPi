#!/usr/bin/python
import urllib.request
Files = ["https://raw.githubusercontent.com/Jack477/CommanderPi/master/src/gui.py", "https://raw.githubusercontent.com/Jack477/CommanderPi/master/src/resources.py", "https://raw.githubusercontent.com/Jack477/CommanderPi/master/src/bootloader.py", "https://raw.githubusercontent.com/Jack477/CommanderPi/master/src/main.py"]
Names = ["gui.py", "resources.py", "bootloader.py", "main.py"]
def download_git(url, name):
	filename, headers = urllib.request.urlretrieve(url, filename="/home/pi/CommanderPi/src/"+name)
	print ("download start!")
	print ("download complete!")
	print ("download file location: ", filename)
	print ("download headers: ", headers)
def update_cpi():
	for f, x in zip(Files, Names):
		download_git(f, x)

