import os
import subprocess as sp
import fileinput




def reboot():
	os.system("sudo reboot now")
cpu_usage_path = "build/cpu_usage.txt"
temperature = "build/actual_temp.txt"

#cpu_usagex = sp.getoutput('vcgencmd measure_clock arm')
def refusage():
	cpu_usagex = sp.getoutput('vcgencmd measure_clock arm')
	cpu_usage = ""
	buff=cpu_usagex[14:17]
	buff=int(buff)
	buffg=cpu_usagex[14:15]
	buffm=cpu_usagex[15:16]
	if ( buff < 500 ):
		cpu_usage = "Processor usage is: " + buffg+ "." + buffm + "GHz"
	else:
		buff = str(buff)
		cpu_usage = "Processor usage is: " + buff + "MHz"
	return cpu_usage



temperature = sp.getoutput('vcgencmd measure_temp')
def reftemp():
	return sp.getoutput('vcgencmd measure_temp')
	

host_name = sp.getoutput('uname -n')
system_name = sp.getoutput('uname')
kernel_version = sp.getoutput('uname -r')

config_path = "/boot/config.txt"
gpu_freq = "400" #default
gexist = False

arm_freq = "1500" #default

over_voltage = "4" #default
oexist = False
f = open(config_path)
for line in f:


	if "arm_freq" in line:
		arm_freq = line
	if "gpu_freq" in line:
		gpu_freq = line
		gexist = True
	if "over_voltage" in line:
		over_voltage = line
		oexist = True
		
f.close()


def overclock_over_voltage(new_over_voltage):
	global oexist
	if oexist:
		
		fin = open(config_path, "rt")
		#read file contents to string
		data = fin.read()
		#replace all occurrences of the required string
		data = data.replace(over_voltage, 'over_voltage='+new_over_voltage+'\n')
		#close the input file
		fin.close()
		#open the input file in write mode
		fin = open(config_path, "wt")
		#overrite the input file with the resulting data
		fin.write(data)
		#close the file
		fin.close()
		print(new_over_voltage)
		new_over_voltage = None
	else:
		oexist = True
		file_object = open(config_path, 'a')
		file_object.write('over_voltage='+new_over_voltage+'\n')
		file_object.close()

def overclock_gpu_freq(gpu_new_freq):
	global gexist
	if gexist:
		
		fin = open(config_path, "rt")
		#read file contents to string
		data = fin.read()
		#replace all occurrences of the required string
		data = data.replace(gpu_freq, 'gpu_freq='+gpu_new_freq+'\n')
		#close the input file
		fin.close()
		#open the input file in write mode
		fin = open(config_path, "wt")
		#overrite the input file with the resulting data
		fin.write(data)
		#close the file
		fin.close()
		print(gpu_new_freq)
		gpu_new_freq = None
	else:
		gexist = True
		file_object = open(config_path, 'a')
		file_object.write('gpu_freq='+gpu_new_freq+'\n')
		file_object.close()
		
		

def overclock_arm_freq(arm_new_freq):
	print(arm_new_freq)
	fin = open(config_path, "rt")
	#read file contents to string
	data = fin.read()
	#replace all occurrences of the required string
	data = data.replace(arm_freq, 'arm_freq='+arm_new_freq+'\n')
	#close the input file
	fin.close()
	#open the input file in write mode
	fin = open(config_path, "wt")
	#overrite the input file with the resulting data
	fin.write(data)
	#close the file
	fin.close()
	arm_new_freq = None
