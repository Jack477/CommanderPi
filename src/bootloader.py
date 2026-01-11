import os
import subprocess as sp
import glob

path = os.path.dirname(os.path.realpath(__file__))
bootloader_version = sp.getoutput('vcgencmd bootloader_version')
x_version = bootloader_version[0:11]


def _bootconf_path():
	cache_dir = os.path.join(os.path.expanduser("~"), ".cache", "CommanderPi")
	os.makedirs(cache_dir, exist_ok=True)
	return os.path.join(cache_dir, "bootconf.txt")


BOOTCONF_PATH = _bootconf_path()

def _candidate_eeprom_dirs():
	return [
		"/lib/firmware/raspberrypi/bootloader",
		"/usr/lib/firmware/raspberrypi/bootloader",
		"/lib/firmware/raspberrypi/bootloader-2711",
		"/usr/lib/firmware/raspberrypi/bootloader-2711",
		"/lib/firmware/raspberrypi/bootloader-2712",
		"/usr/lib/firmware/raspberrypi/bootloader-2712",
	]


def _find_latest_eeprom_image(channel="stable"):
	for base in _candidate_eeprom_dirs():
		channel_dir = os.path.join(base, channel)
		if not os.path.isdir(channel_dir):
			continue
		candidates = sorted(glob.glob(os.path.join(channel_dir, "pieeprom-*.bin")), reverse=True)
		if candidates:
			return candidates[0]
	return None


def get_actual_version():
	image = _find_latest_eeprom_image("stable")
	return os.path.basename(image) if image else ""


ad = get_actual_version()
print('Here is ad: '+ad)
def write_bootloader():

	#os.system('rpi-eeprom-config --out pieeprom-new.bin --config '+path+"/build/bootconf.txt"+' /lib/firmware/raspberrypi/bootloader/stable/pieeprom-2020-04-16.bin')
	base_image = _find_latest_eeprom_image("stable")
	if not base_image:
		print("ERROR: EEPROM image not found; is rpi-eeprom installed and is this a Pi with EEPROM bootloader?")
		return

	os.makedirs(os.path.join(path, "build"), exist_ok=True)
	out_image = os.path.join(path, "build", os.path.basename(base_image))

	os.system(f'rpi-eeprom-config --out "{out_image}" --config "{BOOTCONF_PATH}" "{base_image}"')
	os.system(f'sudo rpi-eeprom-update -d -f "{out_image}"')

def read_bootloader():
	text = ''
	print(x_version)
	print(os.path.dirname(os.path.realpath(__file__)))
	regenerate = False
	if(os.path.exists(BOOTCONF_PATH)):
		f = open(BOOTCONF_PATH)
		bootloader_config = f.read()
		f.close()
		if "No such file or directory" in bootloader_config or bootloader_config.lstrip().startswith("ERROR:"):
			regenerate = True
		else:
			print("File is exist!")
			return bootloader_config

	if regenerate or not os.path.exists(BOOTCONF_PATH):
		os.makedirs(os.path.join(path, "build"), exist_ok=True)
		base_image = _find_latest_eeprom_image("stable")
		if base_image:
			text = sp.getoutput(f'rpi-eeprom-config "{base_image}"')
		else:
			text = "ERROR: Failed to find a local EEPROM image under /usr/lib/firmware or /lib/firmware.\n"
			text += "This usually means the rpi-eeprom package isn't installed, or this device doesn't use an EEPROM bootloader.\n"
		#os.system("rpi-eeprom-config /lib/firmware/raspberrypi/bootloader/stable/pieeprom-2020-04-16.bin > build/bootconf.txt")
		try:
			f = open(BOOTCONF_PATH, "w+")
			f.write(text)
			f.close()
		except Exception as e:
			print(f"ERROR: Failed to write bootloader config to {BOOTCONF_PATH}: {e}")
			return text
		print("File is not exist! Creating file...")
		f2 = open(BOOTCONF_PATH)
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
f = open(BOOTCONF_PATH)
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
	fin = open(BOOTCONF_PATH, "rt")
	#read file contents to string
	data = fin.read()
	#replace all occurrences of the required string
	data = data.replace(x, name+'='+new_value+'\n')
	#close the input file
	fin.close()
	#open the input file in write mode
	fin = open(BOOTCONF_PATH, "wt")
	#overrite the input file with the resulting data
	fin.write(data)
	#close the file
	fin.close()
	#name= None
	#new_value = None		
		
