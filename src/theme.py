import resources as rs
from tkinter import Button
from tkinter import Entry

### List of all windows as master (Tkinter.tk) objects
window_list = []

### for change theme 0 - light | 1 - dark

color_mode=rs.config['DEFAULT']['color_mode']

default_background_color="#F0F0F0"
default_font_color="Black"

### TODO: move window_list to another location?
def set_theme(master):
	#defaultbg = tk.cget('bg')
	#print(defaultbg)
	#print("fucking color mode is: "+str(color_mode))
	if int(color_mode)==1:
		default_background_color="Black"
		default_font_color="White"
		master.tk_setPalette(background=default_background_color, foreground=default_font_color)
		master.update()
		wlist = master.winfo_children()
		#print(len(wlist))
		for widget in wlist:
			if(isinstance(widget, Button)):
				widget.configure(bg="#404040", fg=default_font_color)
			elif(isinstance(widget, Entry)):
				widget.configure(bg="#404040", fg=default_font_color)
			wlist2 = widget.winfo_children()
			for x in wlist2:
				#print(x.winfo_class())
				if(isinstance(x, Button)):
					x.configure(bg="#404040", fg=default_font_color)
				elif(isinstance(x, Entry)):
					x.configure(bg="#404040", fg=default_font_color)
	else:
		default_background_color="#d9d9d9"
		default_font_color="Black"
		master.tk_setPalette(background=default_background_color, foreground=default_font_color)
		master.update()
		wlist = master.winfo_children()
		for widget in wlist:
			if(isinstance(widget, Button)):
				widget.configure(bg=default_background_color, fg=default_font_color)
			elif(isinstance(widget, Entry)):
				widget.configure(bg=default_background_color, fg=default_font_color)
			wlist2 = widget.winfo_children()
			for x in wlist2:
				print(x.winfo_class())
				if(isinstance(x, Button)):
					x.configure(bg=default_background_color, fg=default_font_color)
				elif(isinstance(x, Entry)):
					x.configure(bg=default_background_color, fg=default_font_color)

	for window in window_list:
		if int(color_mode)==1:
			default_background_color="Black"
			default_font_color="White"
			window.tk_setPalette(background=default_background_color, foreground=default_font_color)
			window.update()
			wlist = window.winfo_children()
			for widget in wlist:
				if(isinstance(widget, Button)):
					widget.configure(bg="#404040", fg=default_font_color)

				elif(isinstance(widget, Entry)):
					widget.configure(bg="#404040", fg=default_font_color)
				wlist2 = widget.winfo_children()
				for x in wlist2:
					if(isinstance(x, Button)):
						x.configure(bg="#404040", fg=default_font_color)			
					elif(isinstance(x, Entry)):
						x.configure(bg="#404040", fg=default_font_color)
					wlist3 = x.winfo_children()
					for z in wlist3:
						if(isinstance(z, Button)):
							z.configure(bg="#404040", fg=default_font_color)						
						elif(isinstance(z, Entry)):
							z.configure(bg="#404040", fg=default_font_color)
					

		else:
			default_background_color="#d9d9d9"
			default_font_color="Black"
			window.tk_setPalette(background=default_background_color, foreground=default_font_color)
			window.update()
			wlist = window.winfo_children()
			for widget in wlist:
				if(isinstance(widget, Button)):
					widget.configure(bg=default_background_color, fg=default_font_color)
				elif(isinstance(widget, Entry)):
					widget.configure(bg=default_background_color, fg=default_font_color)
				wlist2 = widget.winfo_children()
				for x in wlist2:
					if(isinstance(x, Button)):
						x.configure(bg=default_background_color, fg=default_font_color)
					elif(isinstance(x, Entry)):
						x.configure(bg=default_background_color, fg=default_font_color)
					wlist3 = x.winfo_children()
					for z in wlist3:
						if(isinstance(z, Button)):
							z.configure(bg=default_background_color, fg=default_font_color)
						elif(isinstance(z, Entry)):
							z.configure(bg=default_background_color, fg=default_font_color)
