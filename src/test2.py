#!/usr/bin/python
import os
import subprocess as sp
import fileinput
config_path = "config.txt"
arm_freq = ""
f = open(config_path)
def overclock_arm_freq(arm_new_freq):
	f = open(config_path)
	for line in f:
		if "arm_freq" in line:
			f.write(line.replace(line, arm_new_freq))
dupa = "works"
overclock_arm_freq(dupa)