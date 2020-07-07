#!/usr/bin/python
import sys
import os
import resources as rs
import bootloader as btl
import update as up
import tkinter as tk
import theme as th
import importlib
import webbrowser
from tkinter import messagebox as msb
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

### TODO: Move change_theme function to theme.py?
### split resources.py into smaller files
### move window_list from theme.py to resources

def change_theme(master):
	if th.color_mode==0:
		th.color_mode=1
	else:
		th.color_mode=0
	rs.config.set('DEFAULT', 'color_mode', str(th.color_mode))
	with open('CommanderPi/src/cpi.config', 'w') as configfile:
		rs.config.write(configfile)
	th.set_theme(master)
	#print(th.color_mode)

### Use in window class: master.protocol("WM_DELETE_WINDOW", lambda:on_Window_Close(master))
def on_Window_Close(master):
	if isinstance(master, tk.Tk):
		window_name = master.__class__
		print(window_name)
		th.window_list.pop()
	master.destroy()

### Using to keybind window kill
def killwindow(event, master):
	on_Window_Close(master)

### Open new window with his own master
def bopen(window):
	x = window()

### Depracted
#def callback(url):
#	webbrowser.open_new(url)

class Network_Window:
	def __init__(master):
		master = tk.Tk()
		master.geometry("480x250")
		master.title("Commander Pi")
		th.window_list.append(master)
		th.set_theme(master)

		mainframe = Frame(master)
		mainframe.pack(padx=10, pady=10)	
		
		titleframe = Frame(mainframe)
		titleframe.pack(fill=X)
				
		image = Image.open("/home/pi/CommanderPi/src/icons/Networkings.png")
		photo = ImageTk.PhotoImage(image, master=titleframe) 

		title_label = tk.Label( titleframe, text = "  Networking", font=("TkDefaultFont", 18, "bold"), image = photo, compound=LEFT, anchor='w')
		title_label.image = photo
		title_label.pack(side=LEFT)
			
		network_frame = Frame(mainframe)
		network_frame.pack()
		
		ether_title = tk.Label(network_frame, text="Ethernet:", font=("TkDefaultFont", 11, "bold"))
		ether_title.grid(row=0, column=0)
		
		wlan_title = tk.Label(network_frame, text="WiFi:", font=("TkDefaultFont", 11, "bold"))
		wlan_title.grid(row=0, column=1)
		
		ether_label = tk.Label( network_frame, text = rs.eth0_data, borderwidth=2, relief="groove", height=7, width=25, anchor='w', justify=LEFT )
		ether_label.grid(row=1, column=0, sticky = W)
		
		wlan_label = tk.Label( network_frame, text = rs.wlan0_data, borderwidth=2, relief="groove",  height=7, width=25, anchor='w', justify=LEFT )
		wlan_label.grid(row=1, column=1, sticky = W)
		
		bind_label = tk.Label( mainframe, text="Press [Esc] to close", font=("TkDefaultFont", 11, "bold") )
		bind_label.pack(side=BOTTOM)
		master.bind('<Escape>', lambda e:killwindow(e, master))
		master.protocol("WM_DELETE_WINDOW", lambda:on_Window_Close(master))
		master.mainloop()			
class Bootloader_Info_Window:

	def __init__(master):
	

		master = tk.Tk()
		master.geometry("430x550")
		master.title("Commander Pi")
		th.window_list.append(master)


		mainframe = Frame(master)
		mainframe.pack(padx=10, pady=10)	
		
		titleframe = Frame(mainframe)
		titleframe.pack(fill=X)
				
		image = Image.open("/home/pi/CommanderPi/src/icons/Bootloaders.png")
		photo = ImageTk.PhotoImage(image, master=titleframe) 

		title_label = tk.Label( titleframe, text = "  Bootloader", font=("TkDefaultFont", 18, "bold"), image = photo, compound=LEFT, anchor='w')
		title_label.image = photo
		title_label.pack(side=LEFT)
		
		separator = ttk.Separator(mainframe, orient='horizontal')
		separator.pack(fill=X, expand=True, pady=5)
		
		versionx_label = tk.Label(mainframe, text="Version information:", font=("TkDefaultFont", 11, "bold"), anchor='w' )
		versionx_label.pack(fill=X)
		#310
		

		
		bootloader_version_label = tk.Label(mainframe, text=btl.bootloader_version, justify="left", wraplength="360", anchor='w')
		bootloader_version_label.pack(fill=X)
		
		boot_frame = Frame(mainframe)
		boot_frame.pack(fill=X)
		
		bootloader_label = tk.Label(boot_frame, text=btl.read_bootloader(), justify="left", anchor='w')
		bootloader_label.grid(row=0, column=0, rowspan=11)
		

		
		separator = ttk.Separator(mainframe, orient='horizontal')
		separator.pack(fill=X, expand=True, pady=5)
		
		setup_b = tk.Button ( mainframe, text="Setup config", command=lambda:config_boot(), font=("TkDefaultFont", 10, "bold"), cursor="hand2")
		setup_b.pack()
		
		
		link = tk.Label( mainframe, text="Official bootloader documentation", cursor="hand2", fg="#1D81DA")
		link.pack(fill=X)
		mlink = 'https://www.raspberrypi.org/documentation/hardware/raspberrypi/bcm2711_bootloader_config.md'
		link.bind("<Button-1>", lambda e: rs.cpi_open_url(mlink))
		

		bind_label = tk.Label( mainframe, text="Press [Esc] to close", font=("TkDefaultFont", 11, "bold") )
		bind_label.pack(side=BOTTOM)
		master.bind('<Escape>', lambda e:killwindow(e, master))
		
		def config_boot():

			#boot_frame.grid_forget()
			setup_b.destroy()
			bootloader_label.destroy()
			config_stuff = "BOOT_UART:\nWAKE_ON_GPIO:\nPOWER_OFF_ON_HALT:\nDHCP_TIMEOUT:\nDHCP_REQ_TIMEOUT:\nTFTP_FILE_TIMEOUT:\nTFTP_IP:\nTFTP_PREFIX:\nBOOT_ORDER:\nSD_BOOT_MAX_RETRIES:\nNET_BOOT_MAX_RETRIES:\n"
			#bootloader_label.config(text=config_stuff, font=("TkDefaultFont", 12))
			#config_text_label = tk.Label(boot_frame, text=config_stuff, justify="left", anchor='w')
			#config_text_label.grid(row=0, column=0, rowspan=11)
			btl_label1 = tk.Label(boot_frame, text="BOOT_UART:", justify=LEFT, width=25, anchor='w')
			btl_label1.grid(row=0, column=0)
		
			BOOT_UART_entry = tk.Entry(boot_frame, justify=CENTER, width=10)
			BOOT_UART_entry.grid(row=0, column=1, pady=0, sticky=N)
			
			btl_label2 = tk.Label(boot_frame, text="WAKE_ON_GPIO:", justify=LEFT, width=25, anchor='w')
			btl_label2.grid(row=1, column=0)
			WAKE_ON_GPIO_entry = tk.Entry(boot_frame, justify=CENTER, width=10)
			WAKE_ON_GPIO_entry.grid(row=1, column=1, pady=0, sticky=N)
		
			btl_label3 = tk.Label(boot_frame, text="POWER_OFF_ON_HALT:", justify=LEFT, width=25, anchor='w')
			btl_label3.grid(row=2, column=0)		
			POWER_OFF_ON_HALT_entry = tk.Entry(boot_frame, justify=CENTER, width=10)
			POWER_OFF_ON_HALT_entry.grid(row=2, column=1, pady=0, sticky=N)

			btl_label4 = tk.Label(boot_frame, text="DHCP_TIMEOUT:", justify=LEFT, width=25, anchor='w')
			btl_label4.grid(row=3, column=0)			
			DHCP_TIMEOUT_entry = tk.Entry(boot_frame, justify=CENTER, width=10)
			DHCP_TIMEOUT_entry.grid(row=3, column=1, pady=0, sticky=N)

			btl_label5 = tk.Label(boot_frame, text="DHCP_REQ_TIMEOUT:", justify=LEFT, width=25, anchor='w')
			btl_label5.grid(row=4, column=0)			
			DHCP_REQ_TIMEOUT_entry = tk.Entry(boot_frame, justify=CENTER, width=10)
			DHCP_REQ_TIMEOUT_entry.grid(row=4, column=1, pady=0, sticky=N)

			btl_label6 = tk.Label(boot_frame, text="TFTP_FILE_TIMEOUT:", justify=LEFT, width=25, anchor='w')
			btl_label6.grid(row=5, column=0)			
			TFTP_FILE_TIMEOUT_entry = tk.Entry(boot_frame, justify=CENTER, width=10)
			TFTP_FILE_TIMEOUT_entry.grid(row=5, column=1, pady=0, sticky=N)

			btl_label7 = tk.Label(boot_frame, text="TFTP_IP:", justify=LEFT, width=25, anchor='w')
			btl_label7.grid(row=6, column=0)			
			TFTP_IP_entry = tk.Entry(boot_frame, justify=CENTER, width=10)
			TFTP_IP_entry.grid(row=6, column=1, pady=0, sticky=N)
			
			btl_label8 = tk.Label(boot_frame, text="TFTP_PREFIX:", justify=LEFT, width=25, anchor='w')
			btl_label8.grid(row=7, column=0)			
			TFTP_PREFIX_entry = tk.Entry(boot_frame, justify=CENTER, width=10)
			TFTP_PREFIX_entry.grid(row=7, column=1, pady=0, sticky=N)


			btl_label9 = tk.Label(boot_frame, text="BOOT_ORDER", justify=LEFT, width=25, anchor='w')
			btl_label9.grid(row=8, column=0)			
			BOOT_ORDER_entry = tk.Entry(boot_frame, justify=CENTER, width=10)
			BOOT_ORDER_entry.grid(row=8, column=1, pady=0, sticky=N)
			
			
			btl_label10 = tk.Label(boot_frame, text="SD_BOOT_MAX_RETRIES:", justify=LEFT, width=25, anchor='w')
			btl_label10.grid(row=9, column=0)			
			SD_BOOT_MAX_RETRIES_entry = tk.Entry(boot_frame, justify=CENTER, width=10)
			SD_BOOT_MAX_RETRIES_entry.grid(row=9, column=1, pady=0, sticky=N)
	
			btl_label11 = tk.Label(boot_frame, text="NET_BOOT_MAX_RETRIES:", justify=LEFT, width=25, anchor='w')
			btl_label11.grid(row=10, column=0)	
			NET_BOOT_MAX_RETRIES_entry = tk.Entry(boot_frame, justify=CENTER, width=10)
			NET_BOOT_MAX_RETRIES_entry.grid(row=10, column=1, pady=0, sticky=N)
			
			btl_btn1 = tk.Button(boot_frame, text="Apply and save", font=("TkDefaultFont", 10, "bold"), cursor="hand2", command=lambda:push_config())
			btl_btn1.grid(row=11, column=1)
			btl_btn2 = tk.Button(boot_frame, text="Cancel", font=("TkDefaultFont", 10, "bold"), cursor="hand2", command=lambda:cancel())
			btl_btn2.grid(row=11, column=0, sticky=W)
			th.set_theme(master)
			msb.showwarning(title="Warning", message="This is only for advanced users!\nDo it on your own risk!")

			### Insert default bootloader values, TODO in future
			#BOOT_UART_entry.insert(END, btl.BOOT_UART[-2:-1])
			#WAKE_ON_GPIO_entry.insert(END, btl.WAKE_ON_GPIO[-2:-1])
			#POWER_OFF_ON_HALT_entry.insert(END, btl.POWER_OFF_ON_HALT[-2:-1])
			#DHCP_TIMEOUT_entry.insert(END, btl.DHCP_TIMEOUT[-6:-1])

			def push_config():
				confirm_msgb = msb.askyesno(title=None, message="Are you sure?")
				if confirm_msgb == True:
					btl.set_bootloader_value("BOOT_UART", BOOT_UART_entry.get())
					btl.set_bootloader_value("WAKE_ON_GPIO", WAKE_ON_GPIO_entry.get())
					btl.set_bootloader_value("POWER_OFF_ON_HALT", POWER_OFF_ON_HALT_entry.get())
					btl.set_bootloader_value("DHCP_TIMEOUT", DHCP_TIMEOUT_entry.get())
					btl.set_bootloader_value("DHCP_REQ_TIMEOUT", DHCP_REQ_TIMEOUT_entry.get())
					btl.set_bootloader_value("TFTP_FILE_TIMEOUT", TFTP_FILE_TIMEOUT_entry.get())
					btl.set_bootloader_value("TFTP_IP", TFTP_IP_entry.get())
					btl.set_bootloader_value("TFTP_PREFIX", TFTP_PREFIX_entry.get())
					btl.set_bootloader_value("BOOT_ORDER", BOOT_ORDER_entry.get())
					btl.set_bootloader_value("SD_BOOT_MAX_RETRIES", SD_BOOT_MAX_RETRIES_entry.get())
					btl.set_bootloader_value("NET_BOOT_MAX_RETRIES", NET_BOOT_MAX_RETRIES_entry.get())
					btl.write_bootloader()
					on_Window_Close(master)
					msb.showinfo(title="", message="Now you need to reboot")
					#rs.reboot()
		def cancel():
			importlib.reload(rs)
			importlib.reload(btl)
			on_Window_Close(master)
			bopen(Bootloader_Info_Window)
		th.set_theme(master)
		master.protocol("WM_DELETE_WINDOW", lambda:on_Window_Close(master))
		master.mainloop()
	

class Proc_Info_Window:

	def __init__(master):
	
		master = tk.Tk()
		master.geometry("350x400")
		master.title("Commander Pi")
		th.window_list.append(master)
		th.set_theme(master)
		mainframe = Frame(master)
		mainframe.pack(padx=10, pady=10)	
		
		titleframe = Frame(mainframe)
		titleframe.pack(fill=X)
				
		image = Image.open("/home/pi/CommanderPi/src/icons/CPUs.png")
		photo = ImageTk.PhotoImage(image, master=titleframe) 

		title_label = tk.Label( titleframe, text = "  CPU Details", font=("TkDefaultFont", 18, "bold"), image = photo, compound=LEFT, anchor='w')
		title_label.image = photo
		title_label.pack(side=LEFT)
	
		separator = ttk.Separator(mainframe, orient='horizontal')
		separator.pack(fill=X, expand=True, pady=15)
		
		cpu_content_frame = Frame(mainframe)
		cpu_content_frame.pack(fill=X)
		
		cpu_label = tk.Label( cpu_content_frame, text = rs.getproc0(), justify=LEFT, width=20, anchor='w' )
		cpu_label.grid(row=0, column=0, rowspan=14, sticky=W)
		
		cpu_label2 = tk.Label( cpu_content_frame, text = rs.getproc1(), justify=LEFT, width=13, anchor='w' )
		cpu_label2.grid(row=0, column=1, rowspan=14, sticky=W)
		
		separator2 = ttk.Separator(mainframe, orient='horizontal')
		separator2.pack(fill=X, expand=True, pady=15)	
		
		bind_label = tk.Label( mainframe, text="Press [Esc] to close", font=("TkDefaultFont", 11, "bold") )
		bind_label.pack(side=BOTTOM)
		master.bind('<Escape>', lambda e:killwindow(e, master))
		master.protocol("WM_DELETE_WINDOW", lambda:on_Window_Close(master))	
		master.mainloop()
	
### Depracted, to delete
class Fast_Overclock_Window:

	def __init__(master):
	
		master = tk.Tk()
		master.geometry("350x400")
		master.title("Commander Pi")

		title_label = tk.Label( master, text = "Fast overclocking for non-advanced users!\n")	
		title_label.grid(row=0, column=0, columnspan=2)			
		
		factory_label = tk.Label( master, text="factory settings", justify=CENTER, fg="green", wraplength="150", borderwidth=2, relief="groove", width="30")
		factory_label.grid(row=1, column=0)
		
		factory_b = tk.Button(master, text="Factory", justify=CENTER, width="7", command = lambda:confirum_push(1))
		factory_b.grid(row=1, column=1)
		
		stable_label = tk.Label( master, text="stable settings, you should have a cooling", justify=CENTER, fg="yellow", wraplength="150", borderwidth=2, relief="groove", width="30")
		stable_label.grid(row=2, column=0)
		
		stable_b = tk.Button(master, text="Stable", justify=CENTER, width="7", command = lambda:confirum_push(2))
		stable_b.grid(row=2, column=1)	
		
		extreme_label = tk.Label( master, text="extreme settings, you must have a cooling!", justify=CENTER, fg="red", wraplength="150", borderwidth=2, relief="groove", width="30")
		extreme_label.grid(row=3, column=0)
		
		factory_b = tk.Button(master, text="Extreme", justify=CENTER, width="7", command = lambda:confirum_push(3))
		factory_b.grid(row=3, column=1)

		def confirum_push(num):
			arm_freq="0"
			gpu_freq="0"
			over_voltage="0"
			if num == 1:
				arm_freq="1500"
				gpu_freq="400"
				over_voltage="4"	
			if num == 2:
				arm_freq="2000"
				gpu_freq="600"
				over_voltage="6"	
			if num == 3:
				arm_freq="2147"
				gpu_freq="750"
				over_voltage="6"
			confirm_msgb = msb.askyesno(title=None, message="Are you sure?")
			if confirm_msgb == True:
				#rs.overclock_arm_freq(arm_freq)
				#rs.overclock_gpu_freq(gpu_freq)
				#rs.overclock_over_voltage(over_voltage)
				print("It works!")
				print(arm_freq)
				print(gpu_freq)
				print(over_voltage)
				master.destroy()
				#rs.reboot()

			else:
				importlib.reload(rs)
				master.destroy()
		master.mainloop()
	
		
			
class Overclock_Window:

	def __init__(master):
		master = tk.Tk()
		master.geometry("440x465")
		master.title("Commander Pi")
		th.window_list.append(master)

		mainframe = Frame(master)
		mainframe.pack(padx=10, pady=10)
		
		titleframe = Frame(mainframe)
		titleframe.pack(fill=X)
				
		
		image = Image.open("/home/pi/CommanderPi/src/icons/Overclockings.png")
		photo = ImageTk.PhotoImage(image, master=titleframe) 

		title_label = tk.Label( titleframe, text = "  Overclocking", font=("TkDefaultFont", 18, "bold"), image = photo, compound=LEFT, anchor='w')
		#title_label = tk.Label( master=titleframe, image = photo, compound=TOP)
		title_label.image = photo
		title_label.pack(side=LEFT)
		
		
		separator = ttk.Separator(mainframe, orient='horizontal')
		separator.pack(fill=X, expand=True, pady=15)
		
		entry_frame = Frame(mainframe)
		entry_frame.pack()
		
		arm_freq_label = tk.Label( entry_frame, text="CPU speed (arm_freq): ")
		arm_freq_label.grid(row=0, column=0)
		
		arm_freq_entry = tk.Entry( entry_frame, justify=CENTER, width=10)
		arm_freq_entry.grid(row=0, column=1, ipady=3)
		
		image1 = Image.open("/home/pi/CommanderPi/src/icons/Checks.png")
		photo1 = ImageTk.PhotoImage(image1, master=entry_frame) 
		
		arm_freq_b = tk.Button ( entry_frame, text="Set", command = lambda:overclock_push(arm_freq_entry, 1), font=("TkDefaultFont", 10, "bold"), cursor="hand2", image = photo1, compound=LEFT)
		arm_freq_b.grid(row=0, column=2)
		

		
		gpu_freq_label = tk.Label( entry_frame, text="GPU speed (gpu_freq): ")
		gpu_freq_label.grid(row=1, column=0)
		
		gpu_freq_entry = tk.Entry( entry_frame, justify=CENTER, width=10)
		gpu_freq_entry.grid(row=1, column=1, ipady=3)
		
		
		gpu_freq_b = tk.Button ( entry_frame, text="Set", command = lambda:overclock_push(gpu_freq_entry, 2), font=("TkDefaultFont", 10, "bold"), cursor="hand2", image = photo1, compound=LEFT)
		gpu_freq_b.grid(row=1, column=2)
		
		
		over_voltage_label = tk.Label( entry_frame, text="Volt. adj. (over_voltage):")
		over_voltage_label.grid(row=2, column=0)
		
		over_voltage_entry = tk.Entry( entry_frame, justify=CENTER, width=10)
		over_voltage_entry.grid(row=2, column=1, ipady=3)

		over_voltage_b = tk.Button ( entry_frame, text="Set", command = lambda:overclock_push(over_voltage_entry, 3), font=("TkDefaultFont", 10, "bold"), cursor="hand2", image = photo1, compound=LEFT)
		over_voltage_b.grid(row=2, column=2)
		
		separator2 = ttk.Separator(mainframe, orient='horizontal')
		separator2.pack(fill=X, expand=True, pady=15)
		
		recommended_frame = Frame(mainframe)
		recommended_frame.pack()
		
		r1 = tk.Label( recommended_frame, text="Recommended values:", font=("TkDefaultFont", 10, "bold"), anchor='w', width=25)
		r1.grid(row=0, column=0, sticky=W)
		r2 = tk.Label(recommended_frame, text="CPU speed: 2000", anchor='w', width=25)
		r2.grid(row=1, column=0, sticky=W)
		r3 = tk.Label(recommended_frame, text="GPU speed: 600", anchor='w', width=25)
		r3.grid(row=2, column=0, sticky=W)
		r4 = tk.Label(recommended_frame, text="Voltage adjustment: 6", anchor='w', width=25)
		r4.grid(row=3, column=0, sticky=W)
		
		r5 = tk.Label(recommended_frame, text="Maximum values:", font=("TkDefaultFont", 10, "bold"), anchor='w')
		r5.grid(row=0, column=1, sticky=W)
		r6 = tk.Label(recommended_frame, text="CPU speed: 2147", anchor='w')
		r6.grid(row=1, column=1, sticky=W)
		r7 = tk.Label(recommended_frame, text="GPU speed: 700", anchor='w')
		r7.grid(row=2, column=1, sticky=W)
		r8 = tk.Label(recommended_frame, text="Voltage adjustment: 6", anchor='w')
		r8.grid(row=3, column=1, sticky=W)
		separator3 = ttk.Separator(mainframe, orient='horizontal')
		separator3.pack(fill=X, expand=True, pady=10)
		
		#proposition = tk.Label( master, text="Stable proposed values:\narm_freq=2000\ngpu_freq=600\nover_voltage=6\nMax level:\narm_freq=2147\ngpu_freq=750\nover_voltage=6", fg="red", font=("Courier", 18) )
		#proposition.pack(fill=X)
		

		
		reboot_b = tk.Button (mainframe, text="Apply and Reboot", command = lambda:confirum_push(), font=("TkDefaultFont", 12, "bold"), cursor="hand2")
		reboot_b.pack(side=BOTTOM, pady=35)

		set_default_b = tk.Button( mainframe, text="Set to default and reboot", command = lambda:set_default(),  font=("TkDefaultFont", 12, "bold"), cursor="hand2")
		set_default_b.pack(side=BOTTOM)
		
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
				on_Window_Close(master)
		def set_default():
			confirm_msgb = msb.askyesno(title=None, message="Are you sure?")
			if confirm_msgb == True:
				rs.overclock_arm_freq("1500")
				rs.overclock_gpu_freq("500")
				rs.overclock_over_voltage("")
				print("It works!")	
				rs.reboot()
			else:
				importlib.reload(rs)
				on_Window_Close(master)			
				
		th.set_theme(master)	
		master.protocol("WM_DELETE_WINDOW", lambda:on_Window_Close(master))	
		msb.showwarning(title="Warning", message="Overclocking is only for advanced users!\nDo it on your own risk!")	
		master.mainloop()

class About_Window:

	def __init__(master):
	
		master = tk.Tk()
		master.geometry("400x450")
		master.title("Commander Pi")
		th.window_list.append(master)
		mainframe = Frame(master)
		mainframe.pack(padx=10, pady=10)	
		
		titleframe = Frame(mainframe)
		titleframe.pack(fill=X)
				
		image = Image.open("/home/pi/CommanderPi/src/icons/logo.png")
		photo = ImageTk.PhotoImage(image, master=titleframe) 

		title_label = tk.Label( titleframe, text = "  About Application", font=("TkDefaultFont", 18, "bold"), image = photo, compound=LEFT, anchor='w')
		title_label.image = photo
		title_label.pack(side=LEFT)
	
		separator = ttk.Separator(mainframe, orient='horizontal')
		separator.pack(fill=X, expand=True, pady=15)		

		content_frame = Frame(mainframe)
		content_frame.pack()
		
		about_label = tk.Label( content_frame, text = "Commander Pi 2020\n", justify=CENTER, font=("TkDefaultFont", 11, "bold"))
		about_label.pack()
		
		text_label = tk.Label( content_frame, text="By Jack477\nFor Twister OS\n\nGraphic elements by grayduck\nIcon derived from a work by Vectors Market\nApp idea by Salva\n", justify=CENTER)
		text_label.pack(fill=X)
		
		version_label = tk.Label( content_frame, text=rs.getAppVersion(), font=("TkDefaultFont", 11, "bold"), justify=CENTER)
		version_label.pack()
		
		link = tk.Label( content_frame, text="Changelog", cursor="hand2", fg="#1D81DA", pady=5)
		link.pack(fill=X)
		mlink = 'https://github.com/Jack477/CommanderPi/blob/master/CHANGELOG.md'
		link.bind("<Button-1>", lambda e: rs.cpi_open_url(mlink))
		
		separator2 = ttk.Separator(mainframe, orient='horizontal')
		separator2.pack(fill=X, expand=True, pady=15)
		
		update_button = Button(mainframe, text="Check for updates", command=lambda:update_x(), cursor="hand2", font=("TkDefaultFont", 11, "bold"))
		update_button.pack()

		color_buton = Button(mainframe, text="Change color theme", command=lambda:change_theme(master), cursor="hand2", font=("TkDefaultFont", 11, "bold"))
		color_buton.pack()

		def update_x():
			up.update_cpi()
			sys.exit(0)
		
		bind_label = tk.Label( mainframe, text="Press [Esc] to close", font=("TkDefaultFont", 11, "bold") )
		bind_label.pack(side=BOTTOM)
		master.bind('<Escape>', lambda e:killwindow(e, master))
		th.set_theme(master)
		master.protocol("WM_DELETE_WINDOW", lambda:on_Window_Close(master))		
		master.mainloop()

### Main window		
class Window:
	def __init__(master):

		master = tk.Tk()
		master.geometry("420x500")
		master.title("Commander Pi")
		master.resizable(False, False)
		th.window_list.append(master)
		mainframe = Frame(master)
		mainframe.pack(padx=10, pady=10)
		
		
		titleframe = Frame(mainframe)
		titleframe.pack()
		
		loadimg = Image.open("/home/pi/CommanderPi/src/icons/title_logo.png")
		img = ImageTk.PhotoImage(image=loadimg)

		img_label = tk.Label ( titleframe, image=img)
		img_label.image = img
		img_label.grid(row=0, column=0, columnspan=2)
		
		#title_label = tk.Label( titleframe, text = "Commander Pi", font=("TkDefaultFont", 22, "bold") )
		#title_label.grid(row=0, column=1)
		
		separator = ttk.Separator(mainframe, orient='horizontal')
		separator.pack(fill=X, expand=True, pady=10)
		
		infoframe = Frame(mainframe)
		infoframe.pack(fill=X)
		
		title2_label = tk.Label( infoframe, text = "Real-time system information:\n", font=("TkDefaultFont", 11, "bold"), anchor='w')
		title2_label.grid(row=0, column=0, columnspan=2, sticky=W)
		
		board_version_label = tk.Label( infoframe, text= rs.board_version, fg="red", anchor='w')
		board_version_label.grid(row=1, column=0, columnspan=2, sticky=W)
		
		kernel_version_label = tk.Label( infoframe, text = "Kernel version: ", width=30, anchor='w' )
		kernel_version_label.grid(row=2, column=0, sticky=W)
		
		kernel_version_label2 = tk.Label( infoframe, text = rs.kernel_version , width=15, anchor='w')
		kernel_version_label2.grid(row=2, column=1)
		
		processor_architecture_label = tk.Label( infoframe, text="Processor architecture: ", width=30, anchor='w' )
		processor_architecture_label.grid(row=3, column=0, sticky=W)
		
		processor_architecture_label2 = tk.Label( infoframe, text=rs.processor_architecture, width=15, anchor='w')
		processor_architecture_label2.grid(row=3, column=1)
		
		
		memory_use_label = tk.Label( infoframe, text = "Memory usage: ", width=30, anchor='w' )
		memory_use_label.grid(row=4, column=0, sticky=W)
		
		memory_use_label2 = tk.Label( infoframe, text = "", width=15, anchor='w' )
		memory_use_label2.grid(row=4, column=1)
		
		actual_cpu_temp_label = tk.Label( infoframe, text = "Actual CPU temperature: ", width=30, anchor='w' )
		actual_cpu_temp_label.grid(row=5, column=0, sticky=W)
		
		actual_cpu_temp_label2 = tk.Label( infoframe, text = "", width=15, anchor='w' )
		actual_cpu_temp_label2.grid(row=5, column=1)
		
		actual_cpu_usage_label = tk.Label( infoframe, text = "Processor frequency usage is: ", width=30, anchor='w')
		actual_cpu_usage_label.grid(row=6, column=0, sticky=W)
		
		actual_cpu_usage_label2 = tk.Label(infoframe, text = "",  width=15, anchor='w')
		actual_cpu_usage_label2.grid(row=6, column=1)
		
		
		used_label = tk.Label ( infoframe, text="Used disk space: ", width=30, anchor='w')
		used_label.grid(row=7, column=0, sticky=W)
		
		##BORDER TO TABLE borderwidth=2, relief="groove",
		used_label2 = tk.Label ( infoframe, text=rs.used+"/"+rs.total+" GiB", width=15, anchor='w')
		used_label2.grid(row=7, column=1)
		
		
		separator2 = ttk.Separator(mainframe, orient='horizontal')
		separator2.pack(fill=X, expand=True, pady=10)

				#REFRESH CPU USAGE, MEMORY USAGE AND TEMPERATURE
		def refresh():
			#for x in th.window_list:
			#	print(x.__class__)
			ttext = rs.reftemp()
			ptext = rs.refusage()
			mtext = rs.refmem()
			#dtext = str(rs.get_disk_percent())
			#dtext = "CPU usage " + rs.cpu_usagex +" MHz"
			memory_use_label2.configure(text = mtext + "/100%")
			actual_cpu_temp_label2.configure(text = ttext)
			actual_cpu_usage_label2.configure(text = ptext)
			#disk_use_label.configure(text = "Disk space usage" +dtext+"/100%")
			master.after(1000, refresh)
			
		refresh()
		
		#fast_overclock_b = Button(master, text="Overclocking for non-advanced", command = lambda:bopen(Fast_Overclock_Window), width=20, cursor="hand2", fg="green")
		#fast_overclock_b.pack(fill=X)
		
		advanced_label = tk.Label( mainframe, text = "Advanced tools", font=("TkDefaultFont", 11, "bold"), anchor='w' )	
		advanced_label.pack(fill=X)
		
		btn_frame = Frame(mainframe)
		btn_frame.pack(fill=X)
		
		photo1 = PhotoImage(file = r"/home/pi/CommanderPi/src/icons/CPUs.png") 
		#photoimage1 = photo1.subsample(15, 15) 
		
		proc_info_button = Button ( btn_frame, text="CPU details", command = lambda:bopen(Proc_Info_Window), width=60, height=80, cursor="hand2", image = photo1, compound=TOP)
		proc_info_button.grid(row=0, column=0, padx=4)
		
		photo2 = PhotoImage(file = r"/home/pi/CommanderPi/src/icons/Bootloaders.png")  
		
		btn4 = Button (btn_frame, text="Bootloader", command = lambda:bopen(Bootloader_Info_Window), width=60, height=80, cursor="hand2", image = photo2, compound=TOP)
		btn4.grid(row=0, column=1, padx=4)
		
		photo3 = PhotoImage(file = r"/home/pi/CommanderPi/src/icons/Networkings.png")  		
		
		btn5 = Button (btn_frame, text="Network", command = lambda:bopen(Network_Window),  width=60, height=80, cursor="hand2", image = photo3, compound=TOP)
		btn5.grid(row=0, column=2, padx=4)
		
		photo4 = PhotoImage(file = r"/home/pi/CommanderPi/src/icons/Overclockings.png") 
		
		btn2 = Button(btn_frame, text="Overclock", command = lambda:bopen(Overclock_Window),  width=60, height=80, cursor="hand2", image = photo4, compound=TOP)
		btn2.grid(row=0, column=3, padx=4)
		

		
		btn3 = Button( mainframe, text="About/Update", command = lambda:bopen(About_Window), font=("TkDefaultFont", 11, "bold"), cursor="hand2")
		btn3.pack(side=BOTTOM, pady=5)
		
		#d = Info_Window()
		master.protocol("WM_DELETE_WINDOW", lambda:on_Window_Close(master))
		th.set_theme(master)
		master.mainloop()
		
