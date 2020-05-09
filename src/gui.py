#!/usr/bin/python
import resources as rs
import tkinter as tk
import importlib
from tkinter import messagebox as msb
from tkinter import *


def bopen(window):
	x = window()
class Info_Window:

	def __init__(master):
	
		master = tk.Tk()
		master.geometry("300x300")
		master.title("Commander Pi")

		title_label = tk.Label( master, text = "System information\n")	
		title_label.pack(fill=X)
		
		sys_name_label = tk.Label( master, text = "System name: " + rs.system_name )
		sys_name_label.pack(fill=X)
		
		kernel_version_label = tk.Label( master, text = "Kernel version: " + rs.kernel_version )
		kernel_version_label.pack(fill=X)
		
		actual_cpu_temp_label = tk.Label(master, text = "" )
		actual_cpu_temp_label.pack(fill=X)
		
		actual_cpu_usage_label = tk.Label(master, text = "")
		actual_cpu_usage_label.pack(fill=X)
		
		#REFRESH CPU USAGE AND TEMPERATURE
		def refresh():
			ttext = rs.reftemp()
			ptext = rs.refusage()
			#dtext = "CPU usage " + rs.cpu_usagex +" MHz"
			actual_cpu_temp_label.configure(text = "Actual CPU " + ttext)
			actual_cpu_usage_label.configure(text = ptext)
			master.after(1000, refresh)
		refresh()

		
		master.mainloop()
		
	
class Overclock_Window:

	def __init__(master):
		master = tk.Tk()
		master.geometry("300x400")
		master.title("Commander Pi")

		title_label = tk.Label( master, text = "Overclocking\n")	
		title_label.pack(fill=X)

		arm_freq_entry = tk.Entry(master)
		arm_freq_entry.pack(fill=X)
		
		arm_freq_b = tk.Button ( master, text="Set arm_freq", command = lambda:overclock_push(arm_freq_entry, 1))
		arm_freq_b.pack(fill=X)
		
		gpu_freq_entry = tk.Entry(master)
		gpu_freq_entry.pack(fill=X)
		
		gpu_freq_b = tk.Button ( master, text="Set gpu_freq", command = lambda:overclock_push(gpu_freq_entry, 2))
		gpu_freq_b.pack(fill=X)
		
		over_voltage_entry = tk.Entry(master)
		over_voltage_entry.pack(fill=X)
		
		over_voltage_b = tk.Button ( master, text="Set over_voltage", command = lambda:overclock_push(over_voltage_entry, 3))
		over_voltage_b.pack(fill=X)
		
		reboot_b = tk.Button (master, text="Apply and Reboot", command = lambda:confirum_push())
		reboot_b.pack(fill=X)
		
		proposition = tk.Label( master, text="Stable proposed values:\narm_freq=2000\ngpu_freq=400\nover_voltage=6\nMax level:\narm_freq=2147\ngpu_freq=750\nover_voltage=6", fg="red" )
		proposition.pack(fill=X)

		def overclock_push(entry_stuff, state):
			entry_instance = entry_stuff.get()
			if entry_instance.isdigit():
				rs.set_push_state(state)
				entry_stuff.config(state='disabled')
				print("Its a number so it works!")
			else:
				print("Its not a number!")

			
		def confirum_push():
			print(rs.push_state1)
			print(rs.push_state2)
			print(rs.push_state3)
			confirm_msgb = msb.askyesno(title=None, message="Are you sure?")
			if confirm_msgb == True:
				if arm_freq_entry.get() != "" and gpu_freq_entry.get() != "" and over_voltage_entry.get() != "" and rs.push_state1 == True and rs.push_state2 == True and rs.push_state3 == True:
					rs.overclock_arm_freq(arm_freq_entry.get())
					rs.overclock_gpu_freq(gpu_freq_entry.get())
					rs.overclock_over_voltage(over_voltage_entry.get())
					print("It works!")
					rs.reboot()
				else:
					msb.showinfo(title="Warning", message="You don't set all values!")
			else:
				importlib.reload(rs)
				master.destroy()
				
				
				
		msb.showwarning(title="Warning", message="Overclocking is only for advanced users!\nDo it on your own risk!")
		master.mainloop()

		
class Window:
	def __init__(master):
	
		master = tk.Tk()
		master.geometry("300x300")
		master.title("Commander Pi")

		title_label = tk.Label( master, text = "Welcome in Commander Pi\n", fg="red" )	
		title_label.pack(fill=X)
		
		btn1 = Button( master, text="System information", command = lambda:bopen(Info_Window))
		btn1.pack(fill=X)
		
		btn2 = Button( master, text="Overclocking", command = lambda:bopen(Overclock_Window))
		btn2.pack(fill=X)
		
		
		
		#d = Info_Window()
		master.mainloop()
		
