#!/usr/local/bin/python3

# By: Andrew Moriarty, modified by Ricardo Diaz
# Date: 20181020
# Python3
# Name: dev_stack-list-am_ver_1.00.py
# Purpose: Program goes through files (show inventory output) and obtains serial number

# Resources
# https://www.pythonforbeginners.com/code-snippets-source-code/python-os-listdir-and-endswith


# ~~~~~~~~~~
# Import modules
# ~~~~~~~~~~
import csv
import re
import os
import sys

#   Print a list of stacked switches, their model number, serial number, and mac-address

# ~~~~~~~~~~
# Define variables
# ~~~~~~~~~~
testline = ('-' * 15 + 'TESTING LINE' + '-' * 15)
devices =[]
device_type = []
file_list = []

#os.chdir('H:\duracel\switches') #on windows os

# Change directory to folder that has the switch files (show inventory outputs)
os.chdir('/Users/rdiaz/Documents/bit_bucket/netchil33t/rdiaz/dev/andrew_moriarty/switch_dir') # on mac

# search through a given path (".") for all files that endswith ".txt".
files = (os.listdir())


####################

for file in files:
	if file.endswith('.txt'):
		file_list.append(file)

'''
print (testline)
print (list_files)
sys.exit(1)
'''
####################

# 1. Creates file. Will be writing to this file
with open('output_stacks.txt', 'w') as f_output_config:
	f_output_config.close()

f_output=''


for file in file_list:
	#mac_address = []
	switch_model = []
	switch_sn = []
	with open(file, 'r') as f_device:
		for line in f_device.readlines():
			'''
			if 'Master' in line or 'Member' in line or 'Active' in line or 'Standby' in line:
				# Match -  2       Member ecc8.8224.b980     10     0       Ready
				# Don't match -  5       Member 0000.0000.0000     0      0       Provisioned
				if 'Provisioned' not in line:
					s_mac=re.search('[a-fA-F0-9]{4}.[a-fA-F0-9]{4}.[a-fA-F0-9]{4}',line)
				if s_mac:
					mac_address.append(s_mac.group(0))
					s_mac=''
			'''
			if 'PID' in line:
				# Match - PID: WS-C3750V2-48PS-S , VID: V05, SN: FDO1441X2GC
				# Match - PID: WS-C3850-24P      , VID: V07  , SN: FCW2010D19W
				s_model=re.search('WS[-][\w\-]+',line)
				if s_model:
					s_sn=re.search('[\w]{3}[\d]{4}[\w]{4}',line)
					switch_model.append(s_model.group(0))
					switch_sn.append(s_sn.group(0))

		try:
			if switch_model:
				h_name = file.replace('heist_serial_numbers_','')
				h_name = h_name.replace('.txt','')
				with open('output_stacks.txt', 'a') as f_output_config:
					f_output_config.write('\n')
					f_output_config.write(h_name)
					f_output_config.write('\n')
					loop = 0
					for line in switch_model:
						if switch_model[loop] and switch_sn[loop]:
							out_line = (switch_model[loop] + '\t' + switch_sn[loop])
							f_output_config.write(out_line)
							f_output_config.write('\n')
						loop+=1
				f_output_config.close()

		except:
			print ('=======Issues with ', + file, + ' Check output')

	f_device.close()
