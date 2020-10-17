import os
import subprocess as sp
import psutil

path = os.path.dirname(os.path.realpath(__file__))
bootloader_version = sp.getoutput('vcgencmd bootloader_version')
x_version = bootloader_version[0:11]
def get_actual_version():
	latest_eeprom = sp.getoutput("ls /lib/firmware/raspberrypi/bootloader/stable -r | grep --color=never 'pieeprom' | head -n 1")[9:19]
	return latest_eeprom

ad = get_actual_version()
print('Here is ad: '+ad)
def write_bootloader():

	#os.system('rpi-eeprom-config --out pieeprom-new.bin --config '+path+"/build/bootconf.txt"+' /lib/firmware/raspberrypi/bootloader/stable/pieeprom-2020-04-16.bin')
	os.system('rpi-eeprom-config --out /lib/firmware/raspberrypi/bootloader/stable/pieeprom-'+ad+'.bin --config '+path+"/build/bootconf.txt"+' /lib/firmware/raspberrypi/bootloader/stable/pieeprom-'+ad+'.bin')
	os.system('sudo rpi-eeprom-update -d -f /lib/firmware/raspberrypi/bootloader/stable/pieeprom-'+ad+'.bin')

def read_bootloader():
	text = ''
	get_actual_version()
	print(x_version)
	print(os.path.dirname(os.path.realpath(__file__)))
	if(os.path.exists(path+"/build/bootconf.txt")):
		f = open(path+"/build/bootconf.txt")
		bootloader_config = f.read()
		f.close()
		print("File is exist!")
		return bootloader_config
	else:
		os.system('sudo mkdir '+path+'/build')
		if os.path.exists('/lib/firmware/raspberrypi/bootloader/stable/pieeprom-'+ad+'.bin'):
			text = sp.getoutput('rpi-eeprom-config /lib/firmware/raspberrypi/bootloader/stable/pieeprom-'+ad+'.bin')
		else:
			text = sp.getoutput('rpi-eeprom-config /lib/firmware/raspberrypi/bootloader/stable/pieeprom-2020-07-16.bin')
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
BOOT_UART=""
WAKE_ON_GPIO=""
POWER_OFF_ON_HALT=""
DHCP_TIMEOUT=""
DHCP_REQ_TIMEOUT =""
TFTP_FILE_TIMEOUT=""
TFTP_IP=""
TFTP_PREFIX=""
BOOT_ORDER=""
SD_BOOT_MAX_RETRIES=""
NET_BOOT_MAX_RETRIES=""
FREEZE_VERSION=""

read_bootloader()

#def set_to_var_bootloader():
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

			
def set_bootloader_value(name, new_value):
	x=""
	if name in BOOT_UART:
		x = BOOT_UART
	elif name in WAKE_ON_GPIO:
		x = WAKE_ON_GPIO
	elif name in POWER_OFF_ON_HALT:
		x = POWER_OFF_ON_HALT
	elif name in DHCP_TIMEOUT:
		x = DHCP_TIMEOUT
	elif name in DHCP_REQ_TIMEOUT:
		x = DHCP_REQ_TIMEOUT
	elif name in TFTP_FILE_TIMEOUT:
		x = TFTP_FILE_TIMEOUT
	elif name in TFTP_IP:
		x = TFTP_IP
	elif name in TFTP_PREFIX:
		x = TFTP_PREFIX
	elif name in BOOT_ORDER:
		x = BOOT_ORDER
	elif name in SD_BOOT_MAX_RETRIES:
		x = SD_BOOT_MAX_RETRIES
	elif name in NET_BOOT_MAX_RETRIES:
		x = NET_BOOT_MAX_RETRIES
	print(new_value)
	fin = open(path+"/build/bootconf.txt", "rt")
	#read file contents to string
	data = fin.read()
	#replace all occurrences of the required string
	data = data.replace(x, name+'='+new_value+'\n')
	#close the input file
	fin.close()
	#open the input file in write mode
	fin = open(path+"/build/bootconf.txt", "wt")
	#overrite the input file with the resulting data
	fin.write(data)
	#close the file
	fin.close()
	#name= None
	#new_value = None		
		
