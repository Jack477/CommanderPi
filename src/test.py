#!/usr/bin/python
#TODO
#ADD FUNCTION TO READ VALUE FROM LABEL
#ADD FUNCTION TO WRITE config.txt FILE
#ADD TEMPERATURE OF CPU
#ADD CPU ACTUAL USAGE
#ADD ENABLE/DISABLE SSH
#ADD WIFI CONFIGURATION
import tkinter as tk
from tkinter import *


cpu_usage_path = "build/cpu_usage.txt"
temperature = "build/actual_temp.txt"
cpu_usage = "600";
temperature = 0;

config_path = "config.txt"
arm_freq = ""

f = open(config_path)
for line in f:
	if "arm_freq" in line:
		arm_freq = line
class Window:
	def __init__(master):
	
		master = tk.Tk()
		master.geometry("500x500")
		master.title("Commander Pi")

		title_label = tk.Label( master, text = "Welcome in Commander Pi\n Choice an option:" )	
		title_label.grid(row=0, column=0)
		
		actual_freq_label = tk.Label( master, text = "Actual frequency of the ARM CPU in MHz: "+str(cpu_usage))
		actual_freq_label.grid(row=1, column=0, sticky=W)
		
		temp_label = tk.Label( master, text = "Actual CPU temperature: "+str(temperature))
		temp_label.grid(row=2, column=0, sticky=W)
		
		
		label2 = tk.Label( master, text = "Frequency of the ARM CPU in MHz: "+arm_freq)					
		label2.grid(row=3, column=0, sticky=W)
		
		cpu_set = tk.Entry(master, width=15)
		cpu_set.grid(row=3, column=1)
		
		add_btn = Button(master, text="SET", width=12)
		add_btn.grid(row=3, column=2)
		
		master.mainloop()
		
		
		
window = Window();
