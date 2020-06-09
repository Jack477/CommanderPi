#!/usr/bin/python3
import urllib.request
import os
import resources as rs

#def update_alert():
#	git_version=""
#	data = ""
#	data = urllib.request.urlopen('https://raw.githubusercontent.com/Jack477/CommanderPi/master/src/update.py')
#	for line in data.readlines():
#		print(line)
#		if "app_version" in line:
#			git_version = line
#	print(git_version)

	#print(git_version)
path = os.path.dirname(os.path.realpath(__file__))
Files = ["https://raw.githubusercontent.com/Jack477/CommanderPi/master/src/gui.py", "https://raw.githubusercontent.com/Jack477/CommanderPi/master/src/resources.py", "https://raw.githubusercontent.com/Jack477/CommanderPi/master/src/bootloader.py", "https://raw.githubusercontent.com/Jack477/CommanderPi/master/src/main.py"]
Names = ["gui.py", "resources.py", "bootloader.py", "main.py"]
def delete_old():
	for name in Names:
		os.system('rm '+path+'/'+name)
		print("Deleted "+name)
def download_git(url, name):
	filename, headers = urllib.request.urlretrieve(url, filename="/home/pi/CommanderPi/src/"+name)
	print ("download start!")
	print ("download complete!")
	print ("download file location: ", filename)
	#print ("download headers: ", headers)
def update_cpi():
	delete_old()
	for f, x in zip(Files, Names):
		download_git(f, x)
