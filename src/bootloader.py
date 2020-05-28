import os
import subprocess as sp
import psutil

bootloader_version = sp.getoutput('vcgencmd bootloader_version')

def read_bootloader():
	print(os.path.dirname(os.path.realpath(__file__)))
	path = os.path.dirname(os.path.realpath(__file__))
	if(os.path.exists(path+"/build/bootconf.txt")):
		f = open(path+"/build/bootconf.txt")
		bootloader_config = f.read()
		f.close()
		print("File is exist!")
		return bootloader_config
	else:
		text = sp.getoutput('rpi-eeprom-config /lib/firmware/raspberrypi/bootloader/stable/pieeprom-2020-04-16.bin')
		#os.system("rpi-eeprom-config /lib/firmware/raspberrypi/bootloader/stable/pieeprom-2020-04-16.bin > build/bootconf.txt")
		f = open(path+"/build/bootconf.txt", "w+")
		f.write(text)
		print("File is not exist! Creating file...")
		f.close()
		f2 = open(path+"/build/bootconf.txt")
		bootloader_config = f2.read()
		f2.close()
		print("File created")
		return bootloader_config
