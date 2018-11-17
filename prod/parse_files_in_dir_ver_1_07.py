#!/usr/local/bin/python3

# By: Ricardo Diaz
# Date: 20181110
# Python3
# Name: parse_files_in_dir_ver_1_07.py
# Purpose: Program goes through files in a directory, run through each file, pull data (show command) and add to one file. example below
#################################
#switch_hostname - ip mac_address
#COMMAND: show inventory
#===============
#show inventory
#NAME: "1", DESCR: "WS-C3750G-24PS"
#PID: WS-C3750G-24PS-S  , VID: V05  , SN: FOC1142Y19P
#
#NAME: "GigabitEthernet1/0/25", DESCR: "1000BaseLX SFP"
#PID: Unspecified       , VID:      , SN: AGC1136U41V
#
#NAME: "2", DESCR: "WS-C3750G-24PS"
#PID: WS-C3750G-24PS-S  , VID: V05  , SN: FOC1141Y4MU
#
#NAME: "GigabitEthernet2/0/25", DESCR: "1000BaseLX SFP"
#PID: Unspecified       , VID:      , SN: AGC1136U42H
#################################

# Resources
# https://www.pythonforbeginners.com/code-snippets-source-code/python-os-listdir-and-endswith
# https://stackoverflow.com/questions/7098530/repeatedly-extract-a-line-between-two-delimiters-in-a-text-file-python?fbclid=IwAR3q1ng4QT7i6tt2qH-8jmLnon1EV6hWm_R-f9tzLeQIkhsK0ENgCYUEfIo
# https://stackoverflow.com/questions/7559397/python-read-file-from-and-to-specific-lines-of-text?fbclid=IwAR3k4yGC4pckox1Y_y0EEo_P5nR1AEfuyx4zhvT1OcDuIbIZ-MhehdMXjd0

# ~~~~~~~~~~
# Import modules
# ~~~~~~~~~~
import csv
import re
import os
import sys

# ~~~~~~~~~~
# Define variables
# ~~~~~~~~~~
testline = ('-' * 15 + 'TESTING LINE' + '-' * 15)
devices =[]
list_device_hostname = []
dict_device_output = {}
device_type = []

ui_start = input('Starting string: ')
ui_end = ('-----end_of_line-----')
regex_sum = ui_start + '(.*?)' + ui_end



# ~~~~~~~~~~
# Change directory
# ~~~~~~~~~~
# Enter directory that you want to parse each file
folder_path = input("Enter full directory path: ")
# Change directory to folder that has the switch files (show inventory outputs)
os.chdir(folder_path) # TESTING NEW CODE

# search through a given path (".") for all files that endswith ".txt".
files = (os.listdir())
file_list = []
for file in files:
	if file.endswith('.txt'):
		file_list.append(file)


# ~~~~~~~~~~
# Define regex
# ~~~~~~~~~~
re_command = (r"^COMMAND: show inventory")
re_endofline = (r"-----end_of_line-----")
re_hostname = (r"^hostname\s([\w|\d|-]+)")


# ~~~~~~~~~~
# Define functions
# ~~~~~~~~~~
def def_open_file_rstrip(file):
    global var_open_ui_filename_rstrip
    with open(file, 'r') as var_open_ui_filename: # opens file, reads file and store in variable
        var_open_ui_filename_rstrip = [line.rstrip('\n') for line in var_open_ui_filename] #TESTING

def def_open_file_read():
    global var_open_ui_filename_read
    with open(ui_filename, 'r') as var_open_ui_filename: # opens file, reads file and store in variable
        var_open_ui_filename_read = var_open_ui_filename.read()

def def_hostnames_into_list():
    global device_hostname_list
    device_hostname_list = []
    for line in var_open_ui_filename_rstrip:
    	re_match_hostname = re.search(re_hostname, line) # Regex search for hostname
    	if re_match_hostname:
    		re_match_hostname_g0 = re_match_hostname.group(0) # prints, hostname router01
    		re_match_hostname_g1 = re_match_hostname.group(1) # prints, router01
    		device_hostname_list.append(re_match_hostname_g1)
    with open('parse_output.txt', 'a') as f_output_config:
        f_output_config.write('\n' + re_match_hostname_g1)
    		#print (device_hostname_list)

def def_capture_switch_output(infile):
    global show_command_output
    with open(infile, 'r') as fp:
        #print (fp.read())
        for result in re.findall(regex_sum, fp.read(), re.S):
            show_command_output = result
            #print (show_command_output)
    with open ('parse_output.txt', 'a') as f_output_config:
        f_output_config.write(show_command_output)


def def_main():
    for file in file_list:
        def_open_file_rstrip(file) # Open file to get hostname
        def_hostnames_into_list() # Append hostname to list
        def_capture_switch_output(file)

# ~~~~~~~~~~
# Start program here
# User input
# ~~~~~~~~~~
#ui_start = input('Starting string: ')
#ui_end = input('Ending string: ')
#regex_sum = ui_start + '(.*?)' + ui_end

# ~~~~~~~~~~
# Creates file. Will be writing to this file
# ~~~~~~~~~~
with open('parse_output.txt', 'w') as f_output_config:
	f_output_config.close()


# ~~~~~~~~~~
# Call upon functions
# ~~~~~~~~~~
def_main()

sys.exit(1)
# ~~~~~~~~~~
# Code from andrew_moriarty below
# ~~~~~~~~~~

# 1. Creates file. Will be writing to this file
#with open('parse_output.txt', 'w') as f_output_config:
#	f_output_config.close()

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


# ~~~~~~~~~~
# Testing area
# ~~~~~~~~~~


'''
def GetTheSentences(infile):
     with open(infile) as fp:
         for result in re.findall(r"COMMAND: show inventory(.*?)-----end_of_line-----", fp.read(), re.S):
             print (result)


GetTheSentences('file')

sys.exit(1)

# PRINTS THE BELOW
Ricardo-Mac:dir_parse_files rdiaz$ python3.6 parse_files_in_dir_ver_1_03.py

===============
show inventory
NAME: "871", DESCR: "871 chassis, Hw Serial#: FHK123222TX, Hw Revision: 0x300"
PID: CISCO871-K9         , VID: V05 , SN: FHK123222TX



Ricardo-Mac:dir_parse_files rdiaz$




# Creating list (will be empty at first)
#hostname_list = ['switch01', 'switch02', 'switch03']
#ip_list = ['10.1.1.1', '10.2.2.2', '10.3.3.3.3']
#
#sw01_list = ['you are on host switch01. line 0', 'line 1', 'line 2', '', 'line 4']
#sw02_list = ['you are on host switch02. line 0', 'line 1', 'line 2', '', 'line 4']
#sw03_list = ['you are on host switch03. line 0', 'line 1', 'line 2', '', 'line 4']
#
#switch_output_list = [sw01_list, sw02_list, sw03_list]

switch_output_dict = {
	'sw01': {1: 'COMMAND: show inventory',
			2: '===============',
			3: 'show inventory',
			4: 'NAME: "871", DESCR: "871 chassis, Hw Serial#: FHK123222TX, Hw Revision: 0x300"'},
	'sw02': {1: 'COMMAND: show inventory',
			2: '===============',
			3: 'show inventory',
			4: 'NAME: "2911", DESCR: "2911 chassis, Hw Serial#: AAABBBCCCDD, Hw Revision: 0x300"'}
	}
#print (switch_output_dict)

#for key, value in switch_output_dict.items():
#    print ('\nSwitch Hostname: ', key)
#    for nested_key in value:
#        print(nested_key, ':', value[nested_key])

for hostname, value in switch_output_dict.items():
	print ('\nSwitch Hostname: ', hostname)

	for nested_key in value:
		print (value[nested_key])


# BELOW CODE PRINTS THE BELOW RESULT
for hostname, value in switch_output_dict.items():
	print ('\nSwitch Hostname: ', hostname)

	for nested_key in value:
		print (value[nested_key])

# RESULT

Switch Hostname:  sw01
COMMAND: show inventory
===============
show inventory
NAME: "871", DESCR: "871 chassis, Hw Serial#: FHK123222TX, Hw Revision: 0x300"

Switch Hostname:  sw02
COMMAND: show inventory
===============
show inventory
NAME: "2911", DESCR: "2911 chassis, Hw Serial#: AAABBBCCCDD, Hw Revision: 0x300"
'''


#print (hostname_list[0] + '\t' + ip_list[0])
#print (switch_output_list[0])
#for line in switch_output_list[0]:
#	print (line)
