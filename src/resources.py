import os
import sys
import subprocess as sp
import fileinput
import configparser
import psutil
import platform
import webbrowser
import tkinter as tk
from os import path
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

home_path = sys.argv[1]

print("Here is home_path "+str(home_path))

### update stuff
app_version = "Version 1.0\n"
print("Here is app-1 "+app_version[:-1])
def get_app_version():
	return app_version

### create config file
config = configparser.ConfigParser()
if os.path.exists(home_path+'/CommanderPi/src/cpi.config'):
	config.read(home_path+'/CommanderPi/src/cpi.config')
	print("Exist and read")
else:
	print("Creating config...")
	config['DEFAULT'] = {'color_mode': '0',
	'version': app_version[:-1]}
	with open(home_path+'/CommanderPi/src/cpi.config', 'w') as configfile:
		config.write(configfile)


### open url at new tab in default browser
def open_url(url):
	webbrowser.open_new_tab(url)

### network data

network = psutil.net_if_addrs()
ipv4eth = network['eth0'][0][1]
ipv6eth = None
maceth = network['eth0'][0][2]
try:
	ipv6eth = network['eth0'][1][1]
	maceth = network['eth0'][2][1]
except IndexError:
	ipv6eth = None
	ipv4eth = None
	maceth = network['eth0'][0][1]

broadcasteth = network['eth0'][0][3]

eth0_data = "IPv4 "+str(ipv4eth)+"\nIPv6 "+str(ipv6eth)+"\nMAC "+str(maceth)+"\nBroadcast "+str(broadcasteth)

ipv4wlan0 = network['wlan0'][0][1]
ipv6wlan0 = None
try:
	ipv6wlan0 = network['wlan0'][1][1]
	macwlan0 = network['wlan0'][2][1]
except IndexError:
	ipv6wlan0 = None
	ipv4wlan0 = None
	macwlan0 = network['wlan0'][0][1]
broadcastwlan = network['wlan0'][0][3]

wlan0_data = "IPv4 "+str(ipv4wlan0)+"\nIPv6 "+str(ipv6wlan0)+"\nMAC "+str(macwlan0)+"\nBroadcast "+str(broadcastwlan)


### network country code
def get_country_code():
	country_code = sp.getoutput('iw reg get')
	country_code = country_code.splitlines()
	xcountry_code = ''
	for line in country_code:
		if "country" in line:
			xcountry_code = line
	return xcountry_code

print("Country code is:")
print(get_country_code())

### set country code
def set_country_code(code):
	path = "/etc/default/crda"
	xcode = ""
	with open(path) as f:
		for line in f:
			if "REGDOMAIN=" in line:
				xcode = line
	print(xcode)
	fin = open(path, "rt")
	data = fin.read()
	data = data.replace(xcode, 'REGDOMAIN='+str(code))
	fin.close()
	fin = open(path, "wt")
	fin.write(data)
	fin.close()
	os.system("sudo iw reg set "+code)



### DISK SPACE 
hdd = psutil.disk_usage('/')
def get_total_space():
	return hdd.total / (2**30)
def get_used_space():
	return hdd.used / (2**30)
def get_free_space():
	return hdd.free / (2**30)
def get_disk_percent():
	return hdd.percent

total = str(round(get_total_space(), 2))
used = str(round(get_used_space(), 2))
free = str(round(get_free_space(),2))
disk = str(get_disk_percent())


#### Check entry in gui (overclocking) is preesed
push_state1 = False
push_state2 = False
push_state3 = False
def set_push_state(state):
	global push_state1
	global push_state2
	global push_state3
	if ( state == 1 ):
		push_state1 = True
	elif ( state == 2):
		push_state2 = True
	elif (state == 3):
		push_state3 = True

### get cpu informations

def getproc0():
	cpu = sp.getoutput('lscpu | head -n 14 | cut -d \: -f 1 | sed -e s/$/:/')
	cpux = str(cpu)
	return cpux
	
def getproc1():
	cpu = sp.getoutput('lscpu | head -n 14 | cut -d \: -f 2 | sed -e s/^[[:space:]]*//')
	cpux = str(cpu)
	return cpux

### reboot RPI	
def reboot():
	os.system("sudo reboot now")
	
### get cpu usage in MHz & GHz
def refusage():
	cpu_freq = psutil.cpu_freq()
	buff = cpu_freq[0]
	return str(buff)+" MHz"

### get gpu usage in MHz & GHz
def refgpu():
	gpu_usagex = sp.getoutput('vcgencmd measure_clock v3d')
	gpu_usage = ""
	buff=gpu_usagex[14:17]
	buff=int(buff)
	buffg=gpu_usagex[14:15]
	buffm=gpu_usagex[15:16]
	if ( buff < 200 ):
		gpu_usage = buffg+ "." + buffm + " GHz"
	else:
		buff = str(buff)
		gpu_usage = buff + " MHz"
	return gpu_usage


### get ram usage
def refmem():
	memory_usex = psutil.virtual_memory().percent
	memory_use = str(memory_usex)
	return memory_use

### get temperatue
def reftemp():
	temp = psutil.sensors_temperatures()
	temp = round(temp['cpu_thermal'][0][1])
	return str(temp)+"'C"
	

	
### board version
board_versionx = sp.getoutput('cat /proc/device-tree/model')
board_version = board_versionx[:-1]

def get_board_version():
	if "ROCK Pi" in board_version:
		return board_version
	if "Pi 3 Model B Plus" in board_version:
		return 3
	if "Pi 4 Model" in board_version:
		return 4
		

### processor architecture
def get_arch():
	processor_architecture = platform.machine()
	return processor_architecture

### kernel version
def get_kernel_version():
	kernel_version = platform.release()
	return kernel_version

gpu_info="Model: Broadcom VideoCore VI\n"
def get_gpu_info():
	return gpu_info
### check device config path
config_path=""
if path.exists("/boot/config.txt"):
	config_path = "/boot/config.txt"
elif path.exists("/boot/firmware/usercfg.txt"):
	config_path = "/boot/firmware/usercfg.txt"
elif path.exists("/media/pi/boot/config.txt"):
	config_path = "/media/pi/boot/config.txt"
elif path.exists("/boot/firmware/config.txt"):
	config_path = "/boot/firmware/config.txt"
else:
	print("Can't find RaspberryPi config file!")


gpu_freq = "400" #default
gexist = False

arm_freq = "1500" #default
aexist = False

over_voltage = "4" #default
oexist = False

arm_64bit = "0" #default
arm_64bitexist = False

gpu_mem = "76" #default?
gpu_memexist = False

force_turbo = "0"
force_turboexist = False

kms_mode = "#dtoverlay=vc4-fkms-v3d" #default
kms_modeexist = False

f = open(config_path)
for line in f:

	if "arm_freq" in line:
		arm_freq = line
		aexist = True
	if "gpu_freq" in line:
		gpu_freq = line
		gexist = True
	if "over_voltage" in line:
		over_voltage = line
		oexist = True
	if "arm_64bit" in line:
		arm_64bit = line
		arm_64bitexist = True
	if "force_turbo" in line:
		force_turbo = line
		force_turboexist = True
	if "dtoverlay=vc4-" in line:
		kms_mode = line
		kms_modeexist = True #should be everytime true?
	if "gpu_mem" in line:
		gpu_mem = line
		gpu_memexist = True
f.close()

### minimum gpu_mem=16
### lowest gpu_mem == better linux performance
### higher gpu_mem (gpu_mem>512) == linux could crash, there is no performance advantage from specifying values larger than is necessary

def get_gpu_mem():
	value = ""
	for x in gpu_mem:
		if x.isnumeric():
			value+=x
	return value

def set_gpu_mem(new_value):
	if gpu_memexist:
		f = open(config_path, "rt")
		data = f.read()
		data.replace(gpu_mem, 'gpu_mem='+new_value+'\n')
		f.close()
		f = open(config_path, "wt")
		f.write(data)
		f.close()





### gpu driver
# dtoverlay=vc4-fkms-v3d 
# mesa must be 19.1.0 or later
# not available on 64-bit (AARCH64) ?
# dtoverlay=vc4-kms-v3d-pi4 <- default active?



### KMS should set gpu_mem to 128?

def get_kms_mode():
	if "pi4" in kms_mode:
		return "KMS mode: KMS"
	elif "fkms" in kms_mode:
		return "KMS mode: FKMS"
	else:
		return "KMS MODE: "+kms_mode

def set_kms_mode():
	print(kms_mode)
	if "fkms" in kms_mode:
		print("setting up kms to KMS")
		fin = open(config_path, "rt")
		data = fin.read()
		data = data.replace(kms_mode, 'dtoverlay=vc4-kms-v3d-pi4\n')
		fin.close()
		fin = open(config_path, "wt")
		fin.write(data)
		fin.close()
	else:
		print("setting up kms to FKMS")
		fin = open(config_path, "rt")
		data = fin.read()
		data = data.replace(kms_mode, 'dtoverlay=vc4-fkms-v3d\n')
		fin.close()
		fin = open(config_path, "wt")
		fin.write(data)
		fin.close()
	

### return kernel mode
def get_kernel_mode():
	if "arm_64bit=1" in arm_64bit:
		return "64bit"
	else:
		return "32bit"

### return force_turbo status (on/off)
def get_force_turbo():
	if "force_turbo=1" in force_turbo:
		return "ON"
	else:
		return "OFF"


### setting up force_turbo and overvoltage in config.txt
### CHECK IF OVERVOLTAGE EXIST!!!
def set_force_turbo():
	global force_turboexist
	global oexist
	print(oexist)
	print(force_turboexist)
	force_turbo_new = ""
	if force_turboexist and oexist:
		print("FORCE TURBO EXIST")
		fin = open(config_path, "rt")
		data = fin.read()
		if "force_turbo=0" in force_turbo:
			force_turbo_new="1"
			if oexist:
				fin = open(config_path, "rt")
				data = fin.read()
				data = data.replace(over_voltage, 'over_voltage=6\n')
				fin.close()
				fin = open(config_path, "wt")
				fin.write(data)
				fin.close()
			else:
				oexist = True
				file_object = open(config_path, 'a')
				file_object.write('over_voltage=6\n')
				file_object.close()
		else:
			force_turbo_new="0"

		data = data.replace(force_turbo, 'force_turbo='+force_turbo_new+'\n')
		fin.close()
		fin = open(config_path, "wt")
		fin.write(data)
		fin.close()
		force_turbo_new = None

	else:
		if oexist:
			fin = open(config_path, "rt")
			data = fin.read()
			data = data.replace(over_voltage, 'over_voltage=6\n')
			fin.close()
			fin = open(config_path, "wt")
			fin.write(data)
			fin.close()
		else:
			oexist = True
			file_object = open(config_path, 'a')
			file_object.write('over_voltage=6\n')
			file_object.close()

		if force_turboexist:
			if "force_turbo=0" in force_turbo:
				force_turbo_new="1"
			else:
				force_turbo_new="0"
			fin = open(config_path, "rt")
			data = fin.read()
			data = data.replace(force_turbo, 'force_turbo='+force_turbo_new+'\n')
			fin.close()
			fin = open(config_path, "wt")
			fin.write(data)
			fin.close()
		else:
			force_turboexist = True
			force_turbo_new = "1"
			file_object = open(config_path, 'a')
			file_object.write('force_turbo='+force_turbo_new+'\n')
			file_object.close()
			force_turbo_new = None

### setting up 64/32 kernel mode
def set_kernel():
	global arm_64bitexist
	arm_64bit_new = ""
	if arm_64bitexist:
		if "arm_64bit=0" in arm_64bit:
			arm_64bit_new="1"
		else:
			arm_64bit_new="0"
		fin = open(config_path, "rt")
		data = fin.read()
		data = data.replace(arm_64bit, 'arm_64bit='+arm_64bit_new+'\n')
		fin.close()
		fin = open(config_path, "wt")
		fin.write(data)
		fin.close()
		arm_64bit_new = None
	else:
		arm_64bitexist = True
		arm_64bit_new = "1"
		file_object = open(config_path, 'a')
		file_object.write('arm_64bit='+arm_64bit_new+'\n')
		file_object.close()



### replace values in config file
### type_of_value: 1 - overvoltage, 2 - arm_freq, 3 - gpu_freq <-- its not an array it is a tuple list!
config_strings = ("over_voltage=", "arm_freq=", "gpu_freq=")
config_readed_data = (over_voltage, arm_freq, gpu_freq)
def overclock(new_value, type_of_value: int):
	global oexist, aexist, gexist
	exist_status = None
	if type_of_value.__eq__(1):
		exist_status = oexist
	elif type_of_value.__eq__(2):
		exist_status = aexist
	elif type_of_value.__eq__(3):
		exist_status = gexist
	if exist_status:
		fin = open(config_path, "rt")
		data = fin.read()
		data = data.replace(config_readed_data[type_of_value-1], config_strings[type_of_value-1]+new_value+'\n')
		fin.close()
		fin = open(config_path, "wt")
		fin.write(data)
		fin.close()
	else:
		exist_status = True
		file_object = open(config_path, 'a')
		file_object.write(config_strings[type_of_value-1]+new_value+'\n')
		file_object.close()


### ToolTip by vegaseat from DaniWeb
class CreateToolTip(object):
    '''
    create a tooltip for a given widget
    '''
    def __init__(self, widget, text='widget info'):
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.close)

    def enter(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = tk.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
                       background='white', foreground='black', relief='solid', borderwidth=1,
                       font=("times", "10", "normal"))
        label.pack(ipadx=1)

    def close(self, event=None):
        if self.tw:
            self.tw.destroy()