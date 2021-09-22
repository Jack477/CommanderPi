import os
import fileinput
import configparser

# set config defaults as strings
cpi_version     = '0.8.0'
cpi_debug_lvl   = '2'
cpi_debug       = 'False'
cpi_auto_check  = 'True'
cpi_auto_update = 'False'
cpi_color_mode  = '0'

### debug level
#   0 - off (no output to console)
#   1 - custom for developers, move afterwards (no other output)
#   2 - general information (updateing.. created.. no_net..) 
#   3 - full debug info (complex and/or detailed output)
#       eg  open.. read.. close.. failed.. system checks etc
#
### printDebug(string,integer); 
def printDebug(strVal,lvl):
	if debug:
		if debug_lvl>=lvl:
			print(strVal)

### retTrueFalse(string); ret(boolean)
def retTrueFalse(value):
	value = value.casefold()
	if value=='false':
		return False
	if value=='no':
		return False
	if value=='true':
		return True
	if value=='yes':
		return True

debug_lvl=int(cpi_debug_lvl)
debug=retTrueFalse(cpi_debug)

path = os.path.dirname(os.path.realpath(__file__))
config = configparser.ConfigParser()
if os.path.exists(path+'/../cpi.config'):
	printDebug("Exists: cpi.config",2)
	config.read(path+'/../cpi.config')
	printDebug("Read:Config: cpi.config",3)
else:
	printDebug("Creating config ...",2)
	# these are all string values
	config['DEFAULT'] = {
		'version'     : cpi_version,
		'#debug_level': '1	# 0=none 1=custom 2=general 3=debug',
		'debug_level' : cpi_debug_lvl,
		'#debug'      : 'True		# turn on console debug output',
		'debug'       : cpi_debug,
		'#auto_check' : 'False	# dont check for update at startup',
		'auto_check'  : cpi_auto_check,
		'#auto_update': 'True	# auto install update at startup',
		'auto_update' : cpi_auto_update,
		'#color_mode' : '1		# use dark theme, 0=light',
		'color_mode'  : cpi_color_mode
	}
	try:
		with open(path+'/../cpi.config', 'w') as configfile:
			printDebug("Opened:Create: cpi.config",3)
			config.write(configfile)
		printDebug("Created: cpi.config",2)
	except:
		printDebug("Failed:Create: cpi.config",2)
	finally:
		if configfile:
			configfile.close()
		printDebug("Closed:Create: cpi.config",3)

### getTrueFalse(string,boolean); ret(boolean)
def getTrueFalse(val,defaultReturn):
	if val=='':
		return defaultReturn
	else:
		bVal = retTrueFalse(val)
	if bVal!=True and bVal!=False:
		return defaultReturn
	return bVal

### getCPiValue(string,string,(optional)boolean); ret(string|boolean)
def getCPiValue(CPiKey,defaultValue,retBoolean=False):
	if retBoolean:
		bVal = retTrueFalse(defaultValue)
	if CPiKey in config['DEFAULT']:
		if retBoolean:
			return getTrueFalse(config['DEFAULT'][CPiKey], bVal)
		else:
			return config['DEFAULT'][CPiKey]
	else:
		printDebug("Failed: config['DEFAULT']['"+CPiKey+"']",3)
		if retBoolean:
			return bVal
		else:
			return defaultValue

TrueFalse   = True # is it a Boolean value we want returned
version     = getCPiValue('version',cpi_version)
debug_lvl   = int(getCPiValue('debug_level',cpi_debug_lvl))
debug       = getCPiValue('debug',cpi_debug,TrueFalse)
auto_check  = getCPiValue('auto_check',cpi_auto_check,TrueFalse)
auto_update = getCPiValue('auto_update',cpi_auto_update,TrueFalse)
color_mode  = int(getCPiValue('color_mode',cpi_color_mode))

app_version=''
def get_app_version():
	app_version = "Version "+version+"\n"
	return app_version
app_version = get_app_version()

def updateCPiConfig():
	printDebug("Updating config...",3)
	# these are not all string values, so convert them 
	config['DEFAULT'] = {
		'version'     : version,
		'#debug_level': '1	# 0=none 1=custom 2=general 3=debug',
		'debug_level' : str(debug_lvl),
		'#debug'      : 'True		# turn on console debug output',
		'debug'       : str(debug),
		'#auto_check' : 'False	# dont check for update at startup',
		'auto_check'  : str(auto_check),
		'#auto_update': 'True	# auto install update at startup',
		'auto_update' : str(auto_update),
		'#color_mode' : '1		# use dark theme, 0=light',
		'color_mode'  : str(color_mode)
	}
	try:
		with open(path+'/../cpi.config', 'w') as configfile:
			printDebug("Opened:Update: cpi.config",3)
			config.write(configfile)
		printDebug("Updated: cpi.config",2)
	except:
		printDebug("Failed:Update: cpi.config",2)
	finally:
		if configfile:
			configfile.close()
		printDebug("Closed:Update: cpi.config",3)
