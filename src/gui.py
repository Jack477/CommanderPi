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

### home path as python script terminal argument
home_path = rs.home_path


_MAIN_WINDOW = None

WINDOW_SIZE_NETWORK = (480, 280)
WINDOW_SIZE_BOOTLOADER = (430, 550)
WINDOW_SIZE_PROC_INFO = (350, 400)
WINDOW_SIZE_ADDONS = (350, 400)
WINDOW_SIZE_GPU_INFO = (360, 400)
WINDOW_SIZE_OVERCLOCK = (440, 465)
WINDOW_SIZE_ABOUT = (400, 450)


def _place_window(master, preferred_width, preferred_height, *, margin_x=20, margin_y=80, avoid_cover_main=False):
	master.update_idletasks()
	screen_w = master.winfo_screenwidth()
	screen_h = master.winfo_screenheight()
	width = min(int(preferred_width), max(240, screen_w - margin_x))
	height = min(int(preferred_height), max(200, screen_h - margin_y))

	x = max(0, int((screen_w - width) / 2))
	y = max(0, int((screen_h - height) / 2))

	global _MAIN_WINDOW
	if avoid_cover_main and _MAIN_WINDOW is not None:
		try:
			if _MAIN_WINDOW.winfo_exists():
				_MAIN_WINDOW.update_idletasks()
				main_x = int(_MAIN_WINDOW.winfo_x())
				main_y = int(_MAIN_WINDOW.winfo_y())
				main_w = int(_MAIN_WINDOW.winfo_width())
				main_h = int(_MAIN_WINDOW.winfo_height())

				gap = 20

				candidates = [
					(main_x + main_w + gap, main_y),
					(main_x - width - gap, main_y),
					(main_x, main_y + main_h + gap),
					(main_x, main_y - height - gap),
					(main_x + gap, main_y + gap),
				]

				for cand_x, cand_y in candidates:
					cand_x = max(0, min(int(cand_x), screen_w - width))
					cand_y = max(0, min(int(cand_y), screen_h - height - margin_y))
					main_right = main_x + main_w
					main_bottom = main_y + main_h
					overlaps = not (
						cand_x + width <= main_x
						or cand_x >= main_right
						or cand_y + height <= main_y
						or cand_y >= main_bottom
					)
					if not overlaps:
						x, y = cand_x, cand_y
						break
		except Exception:
			pass

	master.geometry(f"{width}x{height}+{x}+{y}")


def _make_scrollable(parent):
	outer = Frame(parent)
	outer.pack(fill=BOTH, expand=True)

	canvas = tk.Canvas(outer, highlightthickness=0)
	scrollbar = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
	canvas.configure(yscrollcommand=scrollbar.set)

	scrollbar.pack(side=RIGHT, fill=Y)
	canvas.pack(side=LEFT, fill=BOTH, expand=True)

	content = Frame(canvas)
	window_id = canvas.create_window((0, 0), window=content, anchor="nw")

	def _on_content_configure(event=None):
		canvas.configure(scrollregion=canvas.bbox("all"))

	def _on_canvas_configure(event):
		canvas.itemconfigure(window_id, width=event.width)

	content.bind("<Configure>", _on_content_configure)
	canvas.bind("<Configure>", _on_canvas_configure)

	def _on_mousewheel(event):
		if getattr(event, "delta", 0):
			canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

	for target in (canvas, content):
		target.bind("<MouseWheel>", _on_mousewheel)
		target.bind("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
		target.bind("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))

	return content


def _window_scaffold(master, *, scrollable):
	content_area = Frame(master)
	content_area.pack(fill=BOTH, expand=True)
	bottom_bar = Frame(master)
	bottom_bar.pack(fill=X, side=BOTTOM)

	if scrollable:
		content_root = _make_scrollable(content_area)
	else:
		content_root = content_area

	return content_root, bottom_bar

### change color theme, edit config file
def change_theme(master):
	if int(th.color_mode)==0:
		print("Setting color theme to 1")
		th.color_mode=1
	else:
		th.color_mode=0
	rs.config.set('DEFAULT', 'color_mode', str(th.color_mode))
	with open(home_path+'/CommanderPi/src/cpi.config', 'w') as configfile:
		rs.config.write(configfile)
	th.set_theme(master)


### Use in window class: master.protocol("WM_DELETE_WINDOW", lambda:on_Window_Close(master))
def on_Window_Close(master):
	if isinstance(master, tk.Tk):
		window_name = master.__class__
		print(window_name)
		try:
			th.window_list.remove(master)
		except ValueError:
			pass
	master.destroy()

### Using to keybind window kill
def killwindow(event, master):
	on_Window_Close(master)

### Open new window with his own master
def bopen(window):
	x = window()



### Every class is another window which is open in own master/loop

class Network_Window:
	def __init__(master):
		master = tk.Tk()
		master.title("Commander Pi")
		master.resizable(True, True)
		_place_window(master, *WINDOW_SIZE_NETWORK, avoid_cover_main=True)
		th.window_list.append(master)

		content_root, bottom_bar = _window_scaffold(master, scrollable=False)
		mainframe = Frame(content_root)
		mainframe.pack(padx=10, pady=10)	
		
		titleframe = Frame(mainframe)
		titleframe.pack(fill=X)
				
		image = Image.open(home_path+"/CommanderPi/src/icons/Networkings.png")
		photo = ImageTk.PhotoImage(image, master=titleframe) 

		title_label = tk.Label( titleframe, text = "  Networking", font=("TkDefaultFont", 18, "bold"), image = photo, compound=LEFT, anchor='w')
		title_label.image = photo
		title_label.pack(side=LEFT)
			
		network_frame = Frame(mainframe)
		network_frame.pack()
		
		ether_title = tk.Label(network_frame, text="Ethernet:", font=("TkDefaultFont", 11, "bold"))
		ether_title.grid(row=0, column=0)
		
		wlan_title = tk.Label(network_frame, text="Wi-Fi:", font=("TkDefaultFont", 11, "bold"))
		wlan_title.grid(row=0, column=1)
		
		ether_label = tk.Label( network_frame, text = rs.eth0_data, borderwidth=2, relief="groove", height=7, width=25, anchor='w', justify=LEFT )
		ether_label.grid(row=1, column=0, sticky = W)
		
		wlan_label = tk.Label( network_frame, text = rs.wlan0_data, borderwidth=2, relief="groove",  height=7, width=25, anchor='w', justify=LEFT )
		wlan_label.grid(row=1, column=1, sticky = W)
		
		cc_frame = Frame(mainframe)
		cc_frame.pack()

		quest_icon = Image.open(home_path+"/CommanderPi/src/icons/Quest.png")
		quest_photo = ImageTk.PhotoImage(quest_icon, master=cc_frame)
		country_code_label = tk.Label( cc_frame, text="Set your country code", font=("TkDefaultFont", 11, "bold"), image=quest_photo, compound=RIGHT)

		country_code_label.grid(row=0, column=0, columnspan=2)

		country_code_tip = rs.CreateToolTip(country_code_label, "Country code defines what Wi-Fi frequency should be used in your country.\nFor example: DE, GB, US, etc.")

		country_code_entry = tk.Entry( cc_frame, justify=CENTER, width=5)
		country_code_entry.grid(row=1, column=0, sticky=E)

		country_code_button = tk.Button( cc_frame, text="Apply", command=lambda:push_cc(), font=("TkDefaultFont", 10, "bold"), cursor="hand2")
		country_code_button.grid(row=1, column=1)

		bind_label = tk.Label( bottom_bar, text="Press [Esc] to close", font=("TkDefaultFont", 11, "bold") )
		bind_label.pack(pady=5)

		def push_cc():
			code = country_code_entry.get()
			if isinstance(code, str) and len(code) == 2:
				code = code.upper()
				rs.set_country_code(code)
				msb.showinfo(title="Done!", message="Your country code is now set as "+code)
			else:
				msb.showwarning(title="Error", message="Country code should be two letters!")

		th.set_theme(master)
		master.bind('<Escape>', lambda e:killwindow(e, master))
		master.protocol("WM_DELETE_WINDOW", lambda:on_Window_Close(master))
		master.mainloop()
		
class Bootloader_Info_Window:

	def __init__(master):
	

		master = tk.Tk()
		master.title("Commander Pi")
		master.resizable(True, True)
		_place_window(master, *WINDOW_SIZE_BOOTLOADER, avoid_cover_main=True)
		th.window_list.append(master)

		content_root, bottom_bar = _window_scaffold(master, scrollable=True)
		mainframe = Frame(content_root)
		mainframe.pack(padx=10, pady=10)	
		
		titleframe = Frame(mainframe)
		titleframe.pack(fill=X)
				
		image = Image.open(home_path+"/CommanderPi/src/icons/Bootloaders.png")
		photo = ImageTk.PhotoImage(image, master=titleframe) 

		title_label = tk.Label( titleframe, text = "  Bootloader", font=("TkDefaultFont", 18, "bold"), image = photo, compound=LEFT, anchor='w')
		title_label.image = photo
		title_label.pack(side=LEFT)
		
		separator = ttk.Separator(mainframe, orient='horizontal')
		separator.pack(fill=X, expand=True, pady=5)
		
		versionx_label = tk.Label(mainframe, text="Version information:", font=("TkDefaultFont", 11, "bold"), anchor='w' )
		versionx_label.pack(fill=X)

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

		separator = ttk.Separator(mainframe, orient='horizontal')
		separator.pack(fill=X, expand=True, pady=5)

		
		link = tk.Label( mainframe, text="Official bootloader documentation", cursor="hand2", fg="#1D81DA")
		link.pack(fill=X)
		mlink = 'https://www.raspberrypi.org/documentation/hardware/raspberrypi/bcm2711_bootloader_config.md'
		link.bind("<Button-1>", lambda e: rs.open_url(mlink))
		

		bind_label = tk.Label( bottom_bar, text="Press [Esc] to close", font=("TkDefaultFont", 11, "bold") )
		bind_label.pack(pady=5)
		master.bind('<Escape>', lambda e:killwindow(e, master))
		
		def switch_kernel():
				confirm_msgb = msb.askyesno(title=None, message="This feature is still experimental, some applications may not work correctly\nAre you sure?")
				if confirm_msgb == True:
					rs.set_kernel()
					rs.reboot()

		def config_boot():
			#boot_frame.grid_forget()
			msb.showwarning(title="Warning", message="This is only for advanced users!\nDo it at your own risk!")
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
		master.title("Commander Pi")
		master.resizable(True, True)
		_place_window(master, *WINDOW_SIZE_PROC_INFO, avoid_cover_main=True)
		th.window_list.append(master)

		content_root, bottom_bar = _window_scaffold(master, scrollable=True)
		mainframe = Frame(content_root)
		mainframe.pack(padx=10, pady=10)	
		
		titleframe = Frame(mainframe)
		titleframe.pack(fill=X)
				
		image = Image.open(home_path+"/CommanderPi/src/icons/CPUs.png")
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
		
		bind_label = tk.Label( bottom_bar, text="Press [Esc] to close", font=("TkDefaultFont", 11, "bold") )
		bind_label.pack(pady=5)
		th.set_theme(master)
		master.bind('<Escape>', lambda e:killwindow(e, master))
		master.protocol("WM_DELETE_WINDOW", lambda:on_Window_Close(master))	
		master.mainloop()
	

class Addons_Window:

	def __init__(master):

		master=tk.Tk()
		master.title("Commander Pi")
		master.resizable(True, True)
		_place_window(master, *WINDOW_SIZE_ADDONS, avoid_cover_main=True)
		th.window_list.append(master)

		content_root, bottom_bar = _window_scaffold(master, scrollable=False)
		mainframe = Frame(content_root)
		mainframe.pack(padx=10, pady=10)

		titleframe = Frame(mainframe)
		titleframe.pack(fill=X)

		image = Image.open(home_path+"/CommanderPi/src/icons/Tool.png")
		photo = ImageTk.PhotoImage(image, master=titleframe) 

		title_label = tk.Label( titleframe, text = "  Additional tools", font=("TkDefaultFont", 18, "bold"), image = photo, compound=LEFT, anchor='w')
		title_label.image = photo
		title_label.pack(side=LEFT)
	
		separator = ttk.Separator(mainframe, orient='horizontal')
		separator.pack(fill=X, expand=True, pady=15)



		btn_kernel = Button(mainframe, text="Switch kernel 32/64-bit", command = lambda:switch_kernel(), width=18, cursor="hand2", font=("TkDefaultFont", 10, "bold"))
		btn_kernel.pack()

		btn_force_turbo = Button(mainframe, text="Force turbo mode", command = lambda:switch_turbo(), width=18, cursor="hand2", font=("TkDefaultFont", 10, "bold"))
		btn_force_turbo.pack()

		def switch_turbo():
			confirm_msgb = msb.askyesno(title=None, message="Forces turbo mode frequencies even when the ARM cores are not busy.\nOver voltage will be set to 6. System will restart.\nAre you sure?")
			if confirm_msgb == True:
				rs.set_force_turbo()
				rs.reboot()			
		def switch_kernel():
			confirm_msgb = msb.askyesno(title=None, message="This feature is still experimental, some applications may not work correctly. System will restart.\nAre you sure?")
			if confirm_msgb == True:
				rs.set_kernel()
				rs.reboot()

		separator2 = ttk.Separator(mainframe, orient='horizontal')
		separator2.pack(fill=X, expand=True, pady=15)	
		
		bind_label = tk.Label( bottom_bar, text="Press [Esc] to close", font=("TkDefaultFont", 11, "bold") )
		bind_label.pack(pady=5)
		th.set_theme(master)
		master.bind('<Escape>', lambda e:killwindow(e, master))
		master.protocol("WM_DELETE_WINDOW", lambda:on_Window_Close(master))	
		master.mainloop()

class GPU_Info_Window:

	def __init__(master):
	
		master = tk.Tk()
		master.title("Commander Pi")
		master.resizable(True, True)
		_place_window(master, *WINDOW_SIZE_GPU_INFO, avoid_cover_main=True)
		th.window_list.append(master)

		content_root, bottom_bar = _window_scaffold(master, scrollable=True)
		mainframe = Frame(content_root)
		mainframe.pack(padx=10, pady=10)	
		
		titleframe = Frame(mainframe)
		titleframe.pack(fill=X)
				
		image = Image.open(home_path+"/CommanderPi/src/icons/Gpu.png")
		photo = ImageTk.PhotoImage(image, master=titleframe) 

		title_label = tk.Label( titleframe, text = "  GPU details", font=("TkDefaultFont", 18, "bold"), image = photo, compound=LEFT, anchor='w')
		title_label.image = photo
		title_label.pack(side=LEFT)
	
		separator = ttk.Separator(mainframe, orient='horizontal')
		separator.pack(fill=X, expand=True, pady=15)
		
		### CONTENT
		quest_icon = Image.open(home_path+"/CommanderPi/src/icons/Quest.png")
		quest_photo = ImageTk.PhotoImage(quest_icon, master=mainframe)

		gpu_info_label = tk.Label(mainframe, text=rs.get_gpu_info())
		gpu_info_label.pack()

		gpu_kms_label = tk.Label(mainframe, text=rs.get_kms_mode(), image=quest_photo, compound=RIGHT)
		gpu_label_popup = rs.CreateToolTip(gpu_kms_label, "Switching between legacy (KMS) and non-legacy (FKMS) drivers can influence 3D acceleration performance.")
		gpu_kms_label.pack()
		gpu_button = tk.Button(mainframe, text="Switch KMS", command=lambda:switch_kms(), cursor="hand2", font=("TkDefaultFont", 10, "bold"))
		gpu_button.pack()

		gpu_mem = "GPU memory: "+rs.get_gpu_mem()
		gpu_mem_label=tk.Label(mainframe, text=gpu_mem, image=quest_photo, compound=RIGHT)
		gpu_label_popup2 = rs.CreateToolTip(gpu_mem_label, "Very low or very high values should be avoided because it can cause problems like preventing Linux from booting.\nUnlike GPUs found on x86 machines, where increasing memory can improve 3D performance, the architecture of\nVideoCore is such that there is no performance advantage from specifying values larger than is necessary.")
		gpu_mem_label.pack(pady=5)
		gpu_mem_slider = tk.Scale(mainframe, label="Default: 76 | Minimum: 16 | Maximum: 512", length=300, from_=16, to=512, orient=tk.HORIZONTAL, showvalue=1)
		gpu_mem_slider.pack()
		gpu_mem_button = tk.Button(mainframe, text="Set GPU memory and reboot",cursor="hand2", font=("TkDefaultFont", 10, "bold"), command=lambda:set_gpu_mem())
		gpu_mem_button.pack()

		separator2 = ttk.Separator(mainframe, orient='horizontal')
		separator2.pack(fill=X, expand=True, pady=15)	

		def set_gpu_mem():
			confirm_msgb = msb.askokcancel(title=None, message="Extreme values should be avoided because it can cause boot problems")
			if confirm_msgb == True:
				rs.set_gpu_mem(str(gpu_mem_slider.get()))


		def switch_kms():
			confirm_msgb = msb.askyesno(title=None, message="This feature is still experimental, some applications may not work correctly. System will restart.\nAre you sure?")
			if confirm_msgb == True:
				rs.set_kms_mode()
				rs.reboot()

		bind_label = tk.Label( bottom_bar, text="Press [Esc] to close", font=("TkDefaultFont", 11, "bold") )
		bind_label.pack(pady=5)
		th.set_theme(master)
		master.bind('<Escape>', lambda e:killwindow(e, master))
		master.protocol("WM_DELETE_WINDOW", lambda:on_Window_Close(master))	
		master.mainloop()
					
class Overclock_Window:

	def __init__(master):
		master = tk.Tk()
		master.title("Commander Pi")
		master.resizable(True, True)
		_place_window(master, *WINDOW_SIZE_OVERCLOCK, avoid_cover_main=True)
		th.window_list.append(master)

		content_root, bottom_bar = _window_scaffold(master, scrollable=True)
		mainframe = Frame(content_root)
		mainframe.pack(padx=10, pady=10)
		
		titleframe = Frame(mainframe)
		titleframe.pack(fill=X)
				
		
		image = Image.open(home_path+"/CommanderPi/src/icons/Overclockings.png")
		photo = ImageTk.PhotoImage(image, master=titleframe) 

		title_label = tk.Label( titleframe, text = "  Overclocking", font=("TkDefaultFont", 18, "bold"), image = photo, compound=LEFT, anchor='w')
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
		
		image1 = Image.open(home_path+"/CommanderPi/src/icons/Checks.png")
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
		
		
		reboot_b = tk.Button (mainframe, text="Apply and reboot", command = lambda:confirum_push(), font=("TkDefaultFont", 12, "bold"), cursor="hand2")
		reboot_b.pack(side=BOTTOM, pady=35)

		set_default_b = tk.Button( mainframe, text="Set to default and reboot", command = lambda:set_default(),  font=("TkDefaultFont", 12, "bold"), cursor="hand2")
		set_default_b.pack(side=BOTTOM)
		
		def overclock_push(entry_stuff, state):
			entry_instance = entry_stuff.get()
			if entry_instance.isdigit():
				if state == 3:
					if (int(entry_instance) >= 0) and (int(entry_instance) <= 16):
						rs.set_push_state(state)
						entry_stuff.config(state='disabled')
						print("Its a number so it works!")
					else:
						print("Overvoltage can be beetwen 0-16")
				else:
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
						rs.overclock(arm_freq_entry.get(), 2)
						rs.overclock(gpu_freq_entry.get(), 3)
						rs.overclock(over_voltage_entry.get(), 1)
						rs.reboot()
					else:
						msb.showinfo(title="Warning", message="You didn't set all values!")
				else:
					importlib.reload(rs)
					on_Window_Close(master)
			def set_default():
				confirm_msgb = msb.askyesno(title=None, message="Are you sure?")
				if confirm_msgb == True:
					rs.overclock("1500", 2)
					rs.overclock("500", 3)
					rs.overclock("", 1)
					rs.reboot()
				else:
					importlib.reload(rs)
					on_Window_Close(master)			
					
			bind_label = tk.Label( bottom_bar, text="Press [Esc] to close", font=("TkDefaultFont", 11, "bold") )
			bind_label.pack(pady=5)
			master.bind('<Escape>', lambda e:killwindow(e, master))
			th.set_theme(master)	
			master.protocol("WM_DELETE_WINDOW", lambda:on_Window_Close(master))	
			msb.showwarning(title="Warning", message="Overclocking is only for advanced users!\nDo it at your own risk!")
			master.lift()
			master.mainloop()

class About_Window:

	def __init__(master):
	
		master = tk.Tk()
		master.title("Commander Pi")
		master.resizable(True, True)
		_place_window(master, *WINDOW_SIZE_ABOUT, avoid_cover_main=True)
		th.window_list.append(master)

		content_root, bottom_bar = _window_scaffold(master, scrollable=True)
		mainframe = Frame(content_root)
		mainframe.pack(padx=10, pady=10)	
		
		titleframe = Frame(mainframe)
		titleframe.pack(fill=X)
				
		image = Image.open(home_path+"/CommanderPi/src/icons/Logo.png")
		photo = ImageTk.PhotoImage(image, master=titleframe) 

		title_label = tk.Label( titleframe, text = "  About Application", font=("TkDefaultFont", 18, "bold"), image = photo, compound=LEFT, anchor='w')
		title_label.image = photo
		title_label.pack(side=LEFT)
	
		separator = ttk.Separator(mainframe, orient='horizontal')
		separator.pack(fill=X, expand=True, pady=15)		

		content_frame = Frame(mainframe)
		content_frame.pack()
		
		about_label = tk.Label( content_frame, text = "Commander Pi 2020/2021\n", justify=CENTER, font=("TkDefaultFont", 11, "bold"))
		about_label.pack()
		
		text_label = tk.Label( content_frame, text="By Jack47\n\nGraphic elements by grayduck\nIcon derived from a work by Vectors Market", justify=CENTER)
		text_label.pack(fill=X)
		
		version_label = tk.Label( content_frame, text=rs.get_app_version(), font=("TkDefaultFont", 11, "bold"), justify=CENTER)
		version_label.pack()
		
		link = tk.Label( content_frame, text="Changelog", cursor="hand2", fg="#1D81DA", pady=5)
		link.pack(fill=X)
		mlink = 'https://github.com/Jack477/CommanderPi/blob/master/CHANGELOG.md'
		link.bind("<Button-1>", lambda e: rs.open_url(mlink))
		
		separator2 = ttk.Separator(mainframe, orient='horizontal')
		separator2.pack(fill=X, expand=True, pady=15)
		
		update_button = Button(mainframe, text="Check for updates", command=lambda:update_x(), cursor="hand2", font=("TkDefaultFont", 11, "bold"))
		update_button.pack()

		color_button = Button(mainframe, text="Change colour theme", command=lambda:change_theme(master), cursor="hand2", font=("TkDefaultFont", 11, "bold"))
		color_button.pack()

		def update_x():
			up.update_cpi()

		
		bind_label = tk.Label( bottom_bar, text="Press [Esc] to close", font=("TkDefaultFont", 11, "bold") )
		bind_label.pack(pady=5)
		master.bind('<Escape>', lambda e:killwindow(e, master))
		th.set_theme(master)
		master.protocol("WM_DELETE_WINDOW", lambda:on_Window_Close(master))		
		master.mainloop()

### Main window		
hide = False
class Window:
	def __init__(master):

		master = tk.Tk()
		global _MAIN_WINDOW
		_MAIN_WINDOW = master
		x = int(master.winfo_screenwidth()/2)-210
		y = int(master.winfo_screenheight()/2)-210
		master.geometry("420x660+"+str(x)+"+"+str(y))
		master.title("Commander Pi")
		master.resizable(False, False)
		icon = PhotoImage(file = home_path+"/CommanderPi/src/icons/Icon.png")
		master.iconphoto(True, icon)
		th.window_list.append(master)
		mainframe = Frame(master)
		mainframe.pack(padx=10, pady=10)
		
		
		titleframe = Frame(mainframe)
		titleframe.pack()
		
		loadimg = Image.open(home_path+"/CommanderPi/src/icons/Title_logo.png")
		img = ImageTk.PhotoImage(image=loadimg)

		img_label = tk.Label ( titleframe, image=img)
		img_label.image = img
		img_label.grid(row=0, column=0, columnspan=2)
		
		
		separator = ttk.Separator(mainframe, orient='horizontal')
		separator.pack(fill=X, expand=True, pady=10)
		
		infoframe = Frame(mainframe)
		infoframe.pack(fill=X)
		
		title2_label = tk.Label( infoframe, text = "Real-time system information:\n", font=("TkDefaultFont", 11, "bold"), anchor='w')
		title2_label.grid(row=0, column=0, columnspan=2, sticky=W)
		
		board_version_label = tk.Label( infoframe, text= rs.board_version, fg="#D19113", anchor='w')
		board_version_label.grid(row=1, column=0, columnspan=2, sticky=W)
		
		kernel_version_label = tk.Label( infoframe, text = "Kernel version: ", width=30, anchor='w' )
		kernel_version_label.grid(row=2, column=0, sticky=W)
		
		kernel_version_label2 = tk.Label( infoframe, text = rs.get_kernel_version() , width=15, anchor='w')
		kernel_version_label2.grid(row=2, column=1)
		
		kernel_mode_label = tk.Label( infoframe, text = "Operating mode: ", width=30, anchor='w')
		kernel_mode_label.grid(row=3, column=0, sticky=W)

		kernel_mode_label2 = tk.Label( infoframe, text = rs.get_kernel_mode(), width=15, anchor='w')
		kernel_mode_label2.grid(row=3, column=1)

		processor_architecture_label = tk.Label( infoframe, text="Processor architecture: ", width=30, anchor='w' )
		processor_architecture_label.grid(row=4, column=0, sticky=W)
		
		processor_architecture_label2 = tk.Label( infoframe, text=rs.get_arch(), width=15, anchor='w')
		processor_architecture_label2.grid(row=4, column=1)

		force_turbo_label = tk.Label( infoframe, text="Force turbo: ", width=30, anchor='w' )
		force_turbo_label.grid(row=5, column=0, sticky=W)
		
		force_turbo_label2 = tk.Label( infoframe, text=rs.get_force_turbo(), width=15, anchor='w')
		force_turbo_label2.grid(row=5, column=1)

		memory_use_label = tk.Label( infoframe, text = "Memory usage: ", width=30, anchor='w' )
		memory_use_label.grid(row=6, column=0, sticky=W)
		
		memory_use_label2 = tk.Label( infoframe, text = "", width=15, anchor='w' )
		memory_use_label2.grid(row=6, column=1)
		
		actual_cpu_temp_label = tk.Label( infoframe, text = "Actual CPU temperature: ", width=30, anchor='w' )
		actual_cpu_temp_label.grid(row=7, column=0, sticky=W)
		
		actual_cpu_temp_label2 = tk.Label( infoframe, text = "", width=15, anchor='w' )
		actual_cpu_temp_label2.grid(row=7, column=1)
		
		actual_cpu_usage_label = tk.Label( infoframe, text = "Processor frequency usage: ", width=30, anchor='w')
		actual_cpu_usage_label.grid(row=8, column=0, sticky=W)
		
		actual_cpu_usage_label2 = tk.Label(infoframe, text = "",  width=15, anchor='w')
		actual_cpu_usage_label2.grid(row=8, column=1)
		
		actual_gpu_usage_label = tk.Label( infoframe, text = "GPU frequency (V3D) usage: ", width=30, anchor='w')
		actual_gpu_usage_label.grid(row=9, column=0, sticky=W)
		
		actual_gpu_usage_label2 = tk.Label(infoframe, text = "",  width=15, anchor='w')
		actual_gpu_usage_label2.grid(row=9, column=1)

		used_label = tk.Label ( infoframe, text="Used disk space: ", width=30, anchor='w')
		used_label.grid(row=10, column=0, sticky=W)
		
		##BORDER TO TABLE borderwidth=2, relief="groove",
		used_label2 = tk.Label ( infoframe, text=rs.used+"/"+rs.total+" GiB", width=15, anchor='w')
		used_label2.grid(row=10, column=1)
		
		
		separator2 = ttk.Separator(mainframe, orient='horizontal')
		separator2.pack(fill=X, expand=True, pady=10)

		#REFRESH CPU USAGE, MEMORY USAGE AND TEMPERATURE
		def refresh():

			ttext = rs.reftemp()
			ptext = rs.refusage()
			mtext = rs.refmem()
			gtext = rs.refgpu()

			memory_use_label2.configure(text = mtext + " %")
			actual_cpu_temp_label2.configure(text = ttext)
			actual_cpu_usage_label2.configure(text = ptext)
			actual_gpu_usage_label2.configure(text = gtext)

			master.after(1000, refresh)
			
		refresh()
		
		up_photo = PhotoImage(file = home_path+"/CommanderPi/src/icons/Up.png") 
		down_photo = PhotoImage(file = home_path+"/CommanderPi/src/icons/Down.png") 

		advanced_label = tk.Label( mainframe, text = "Advanced tools", font=("TkDefaultFont", 11, "bold"), anchor='w', cursor="hand2", image=up_photo, compound=RIGHT)	
		advanced_label.bind("<Button-1>", lambda e:hide_tools())
		advanced_label.pack(fill=X, pady=5)



		btn_frame = Frame(mainframe)
		btn_frame.pack(fill=X)
		
		photo_proc_info = PhotoImage(file = home_path+"/CommanderPi/src/icons/CPUs.png") 
		
		proc_info_button = Button ( btn_frame, text="CPU details", command = lambda:bopen(Proc_Info_Window), width=60, height=80, cursor="hand2", image = photo_proc_info, compound=TOP)
		proc_info_button.grid(row=0, column=0, padx=4)
		
		photo_bootloader = PhotoImage(file = home_path+"/CommanderPi/src/icons/Bootloaders.png")  
		
		bootloarder_button = Button (btn_frame, text="Bootloader", command = lambda:bopen(Bootloader_Info_Window), width=60, height=80, cursor="hand2", image = photo_bootloader, compound=TOP)
		bootloarder_button.grid(row=0, column=1, padx=4)
		
		photo_network = PhotoImage(file = home_path+"/CommanderPi/src/icons/Networkings.png")  		
		
		network_button = Button (btn_frame, text="Network", command = lambda:bopen(Network_Window),  width=60, height=80, cursor="hand2", image = photo_network, compound=TOP)
		network_button.grid(row=0, column=2, padx=4)
		
		photo_overclock = PhotoImage(file = home_path+"/CommanderPi/src/icons/Overclockings.png") 
		
		overclock_button = Button(btn_frame, text="Overclock", command = lambda:bopen(Overclock_Window),  width=60, height=80, cursor="hand2", image = photo_overclock, compound=TOP)
		overclock_button.grid(row=0, column=3, padx=4)
		

		gpu_photo = PhotoImage(file = home_path+"/CommanderPi/src/icons/Gpu.png")

		gpu_info_button = Button(btn_frame, text="GPU tools", command = lambda:bopen(GPU_Info_Window), width=60, height=80, cursor="hand2", image=gpu_photo, compound=TOP)
		gpu_info_button.grid(row=1, column=1, padx=4, pady=8)


		addons_photo = PhotoImage(file = home_path+"/CommanderPi/src/icons/Tool.png")

		addons_button = Button(btn_frame, text="Addons", command=lambda:bopen(Addons_Window), width=60, height=80, cursor="hand2", image=addons_photo, compound=TOP)
		addons_button.grid(row=1, column=2, padx=4, pady=8)

		spacer = Frame(mainframe)
		spacer.pack(fill=BOTH, expand=True)
		
		
		
		btn3 = Button( mainframe, text="About | Update", command = lambda:bopen(About_Window), font=("TkDefaultFont", 11, "bold"), cursor="hand2")
		btn3.pack(side=BOTTOM, pady=7)

		def set_window_size(width, height, x_pos, y_pos):
			master.update_idletasks()
			screen_w = master.winfo_screenwidth()
			screen_h = master.winfo_screenheight()
			margin = 60
			width = min(int(width), max(200, screen_w - 20))
			height = min(int(height), max(200, screen_h - margin))
			x_pos = max(0, min(int(x_pos), screen_w - width))
			y_pos = max(0, min(int(y_pos), screen_h - height - margin))
			master.geometry(f"{width}x{height}+{x_pos}+{y_pos}")

		def set_window_size_to_content(width, x_pos, y_pos, min_height=200):
			master.update_idletasks()
			target_height = mainframe.winfo_reqheight() + 20
			set_window_size(width, max(min_height, target_height), x_pos, y_pos)
		
		def hide_tools():
			global hide
			x_pos = master.winfo_x()
			y_pos = master.winfo_y()
			if hide==False:
				advanced_label.configure(image=down_photo)
				btn_frame.pack_forget()
				set_window_size_to_content(420, x_pos, y_pos, min_height=200)
				hide = True
			else:
				advanced_label.configure(image=up_photo)
				btn_frame.pack()
				set_window_size_to_content(420, x_pos, y_pos, min_height=200)
				hide = False
		master.protocol("WM_DELETE_WINDOW", lambda:on_Window_Close(master))
		
		set_window_size_to_content(420, x, y, min_height=200)
		hide_tools()
		th.set_theme(master)
		up.check_update()
		master.mainloop()
		
