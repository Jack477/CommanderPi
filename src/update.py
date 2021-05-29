#!/usr/bin/python3
import sys
import urllib.request
import socket
import os
import resources as rs
from tkinter import messagebox as msb
home = rs.home_path
path = os.path.dirname(os.path.realpath(__file__))
print("path is "+str(path))
Files = ["https://raw.githubusercontent.com/Jack477/CommanderPi/master/src/gui.py", "https://raw.githubusercontent.com/Jack477/CommanderPi/master/src/resources.py", "https://raw.githubusercontent.com/Jack477/CommanderPi/master/src/bootloader.py", "https://raw.githubusercontent.com/Jack477/CommanderPi/master/src/main.py", "https://raw.githubusercontent.com/Jack477/CommanderPi/master/src/update.py", "https://raw.githubusercontent.com/Jack477/CommanderPi/master/src/theme.py"]
Names = ["gui.py", "resources.py", "bootloader.py", "main.py", "update.py", "theme.py"]

### Depracted
def delete_old():
	for name in Names:
		os.system('rm '+path+'/'+name)
		print("Deleted "+name)

### Depreacted
def download_git(url, name):
	filename, headers = urllib.request.urlretrieve(url, filename=home+"/CommanderPi/src/"+name)
	print ("download start!")
	print ("download complete!")
	print ("download file location: ", filename)
	#print ("download headers: ", headers)

def update_cpi():
	url = "https://raw.githubusercontent.com/Jack477/CommanderPi/master/src/resources.py"
	with urllib.request.urlopen(url) as f:
		xcontent = f.read().decode('utf-8')
		xcontent = xcontent.splitlines()
		xversion = ""
		for line in xcontent:
			if "app_version =" in line:
				xversion=line
		if rs.app_version[:-1] in xversion:
			msb.showinfo(title=None, message="There is no update available!")
		else:
			### for 0.7.2
			'''
			delete_old()
			for f, x in zip(Files, Names):
				download_git(f, x)'''
			### since 1.0 update depends on GIT
			msb.showinfo(title=None, message="Downloading!")
			os.system("( cd ~ && rm -r "+rs.home_path+"/CommanderPi )")
			os.system("( cd ~ && git clone https://github.com/Jack477/CommanderPi "+rs.home_path+"/CommanderPi )")
			os.system("( cd ~ && sudo chown -R pi "+rs.home_path+"/CommanderPi )")
			os.system("( cd ~ && sudo chmod +x "+rs.home_path+"/CommanderPi/src/start.sh )")
			os.system("( cd ~ && sudo chmod +x "+rs.home_path+"/CommanderPi/install.sh )")
			os.system("( cd "+rs.home_path+"/CommanderPi && runuser -u pi -- ./install.sh )")
			sys.exit(0)
def is_connected(hostname):
  try:
    host = socket.gethostbyname(hostname)
    s = socket.create_connection((host, 80), 2)
    s.close()
    return True
  except:
     pass
  return False
def check_update():
	url = "https://raw.githubusercontent.com/Jack477/CommanderPi/master/src/resources.py"
	if is_connected("1.1.1.1"):
		with urllib.request.urlopen(url) as f:
			xcontent = f.read().decode('utf-8')
			xcontent = xcontent.splitlines()
			xversion = ""
			for line in xcontent:
				if "app_version =" in line:
					xversion=line
			if rs.app_version[:-1] in xversion:
				print("It works because it's same version!")
			else:
				msb.showinfo(title=None, message="An update is available!")
			print(rs.app_version)
			print(xversion)
	else:
		print("Network is disconnected.")

