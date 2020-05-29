import os
import subprocess as sp
import psutil

path = os.path.dirname(os.path.realpath(__file__))
bootloader_version = sp.getoutput('vcgencmd bootloader_version')

def read_bootloader():
	print(os.path.dirname(os.path.realpath(__file__)))
	if(os.path.exists(path+"/build/bootconf.txt")):
		f = open(path+"/build/bootconf.txt")
		bootloader_config = f.read()
		f.close()
		print("File is exist!")
		return bootloader_config
	else:
		os.system('sudo mkdir '+path+'/build')
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
		
		
##BOOTLOADER CONFIG STUFF
BOOT_UART
WAKE_ON_GPIO
POWER_OFF_ON_HALT
DHCP_TIMEOUT
DHCP_REQ_TIMEOUT
TFTP_FILE_TIMEOUT
TFTP_IP
TFTP_PREFIX
BOOT_ORDER
SD_BOOT_MAX_RETRIES
NET_BOOT_MAX_RETRIES
FREEZE_VERSION

def set_to_var_bootloader():
	f = open(path+"/build/bootconf.txt")
	for line in f:
		if "BOOT_UART" in line:
			BOOT_UART=line
		if "WAKE_ON_GPIO" in line:
			WAKE_ON_GPIO=line
		if "POWER_OFF_ON_HALT" in line:
			POWER_OFF_ON_HALT=line
		if "DHCP_TIMEOUT" in line:
			DHCP_TIMEOUT=line
		if "DHCP_REQ_TIMEOUT" in line:
			DHCP_REQ_TIMEOUT=line
		if "TFTP_FILE_TIMEOUT" in line:
			TFTP_FILE_TIMEOUT=line
		if "TFTP_IP" in line:
			TFTP_IP=line
		if "TFTP_PREFIX" in line:
			TFTP_PREFIX=line
		if "BOOT_ORDER" in line:
			BOOT_ORDER=line
		if "SD_BOOT_MAX_RETRIES" in line:
			SD_BOOT_MAX_RETRIES=line
		if "NET_BOOT_MAX_RETRIES" in line:
			NET_BOOT_MAX_RETRIES=line
		if "FREEZE_VERSION" in line:
			FREEZE_VERSION=line
			
def set_BOOT_UART(new_value):
	print(new_value)
	fin = open(path+"/build/bootconf.txt", "rt")
	#read file contents to string
	data = fin.read()
	#replace all occurrences of the required string
	data = data.replace(BOOT_UART, 'BOOT_UART='+new_value+'\n')
	#close the input file
	fin.close()
	#open the input file in write mode
	fin = open(path+"/build/bootconf.txt", "wt")
	#overrite the input file with the resulting data
	fin.write(data)
	#close the file
	fin.close()
	new_value = None		
		
