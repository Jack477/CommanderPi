#!/usr/bin/python
import resources as rs
import tkinter as tk
import importlib
from tkinter import messagebox as msb
from tkinter import *
from PIL import Image, ImageTk

def killwindow(event, master):
	master.destroy()

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
		
		processor_architecture_label = tk.Label( master, text="Processor architecture: " + rs.processor_architecture )
		processor_architecture_label.pack(fill=X)
		
		memory_use_label = tk.Label( master, text = "" )
		memory_use_label.pack(fill=X)
		
		actual_cpu_temp_label = tk.Label(master, text = "" )
		actual_cpu_temp_label.pack(fill=X)
		
		actual_cpu_usage_label = tk.Label(master, text = "")
		actual_cpu_usage_label.pack(fill=X)
		
		
		bind_label = tk.Label( master, text="Press Escape to close" )
		bind_label.pack(side=BOTTOM)
		master.bind('<Escape>', lambda e:killwindow(e, master))
		
		
		#REFRESH CPU USAGE, MEMORY USAGE AND TEMPERATURE
		def refresh():
			ttext = rs.reftemp()
			ptext = rs.refusage()
			mtext = rs.refmem()
			#dtext = "CPU usage " + rs.cpu_usagex +" MHz"
			memory_use_label.configure(text = "Memory usage " + mtext + "/100%")
			actual_cpu_temp_label.configure(text = "Actual CPU " + ttext)
			actual_cpu_usage_label.configure(text = ptext)
			master.after(1000, refresh)
		refresh()

		
		master.mainloop()
		
	
class Overclock_Window:

	def __init__(master):
		master = tk.Tk()
		master.geometry("400x600")
		master.title("Commander Pi")

		title_label = tk.Label( master, text = "Overclocking\n")	
		title_label.pack(fill=X)

		arm_freq_b = tk.Button ( master, text="Set arm_freq", command = lambda:overclock_push(arm_freq_entry, 1), font=("Courier", 24))
		arm_freq_b.pack(fill=X)
		
		arm_freq_entry = tk.Entry(master, font=("Courier", 24), justify=CENTER)
		arm_freq_entry.pack(fill=X)
		
		gpu_freq_b = tk.Button ( master, text="Set gpu_freq", command = lambda:overclock_push(gpu_freq_entry, 2), font=("Courier", 24))
		gpu_freq_b.pack(fill=X)
		
		gpu_freq_entry = tk.Entry(master, font=("Courier", 24), justify=CENTER)
		gpu_freq_entry.pack(fill=X)
		
		over_voltage_b = tk.Button ( master, text="Set over_voltage", command = lambda:overclock_push(over_voltage_entry, 3), font=("Courier", 24))
		over_voltage_b.pack(fill=X)
		
		over_voltage_entry = tk.Entry(master, font=("Courier", 24), justify=CENTER)
		over_voltage_entry.pack(fill=X)
		
		
		proposition = tk.Label( master, text="Stable proposed values:\narm_freq=2000\ngpu_freq=600\nover_voltage=6\nMax level:\narm_freq=2147\ngpu_freq=750\nover_voltage=6", fg="red", font=("Courier", 18) )
		proposition.pack(fill=X)
		
		reboot_b = tk.Button (master, text="Apply and Reboot", command = lambda:confirum_push(), font=("Courier", 24))
		reboot_b.pack(fill=X)

		def overclock_push(entry_stuff, state):
			entry_instance = entry_stuff.get()
			if entry_instance.isdigit():
				rs.set_push_state(state)
				entry_stuff.config(state='disabled')
				print("Its a number so it works!")
			else:
				print("Its not a number!")
		#def overclock_push2(entry_stuff):
		#	global overclock_push_state2
		#	overclock_push_state2 = True
		#	entry_stuff.config(state='disabled')
		#def overclock_push3(entry_stuff):		
		#	global overclock_push_state3
		#	overclock_push_state3 = True		
		#	entry_stuff.config(state='disabled')
			
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

class About_Window:

	def __init__(master):
	
		master = tk.Tk()
		master.geometry("300x300")
		master.title("Commander Pi")

		title_label = tk.Label( master, text = "About application\n")	
		title_label.pack(fill=X)		

		about_label = tk.Label( master, text = "Commander Pi 2020 by Jack477\n for RaspbianX\n\nInspired by Salva", justify=CENTER)
		about_label.pack(fill=X)
		
		bind_label = tk.Label( master, text="Press Escape to close" )
		bind_label.pack(side=BOTTOM)
		master.bind('<Escape>', lambda e:killwindow(e, master))
		
		master.mainloop()		
class Window:
	def __init__(master):
	
		master = tk.Tk()
		master.geometry("350x450")
		master.title("Commander Pi")

		title_label = tk.Label( master, text = "Welcome in Commander Pi\n", fg="red" )	
		title_label.pack(fill=X)
		
		btn1 = Button( master, text="System information", command = lambda:bopen(Info_Window))
		btn1.pack(fill=X)
		
		btn2 = Button( master, text="Overclocking", command = lambda:bopen(Overclock_Window))
		btn2.pack(fill=X)
		
		img = ImageTk.PhotoImage(file = 'build/logo.png')
		img_label = tk.Label ( master, image=img )
		img_label.pack(side=TOP)
		
		btn3 = Button( master, text="About", command = lambda:bopen(About_Window))
		btn3.pack(side=BOTTOM)
		
		#d = Info_Window()
		master.mainloop()
		
