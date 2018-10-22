#!/usr/bin/python3.6

# By: Ricardo Diaz
# Date: 20181001
# Python3.6
# Name: dev_extract_ips.py
# Referance: heist_list

# ~~~~~~~~~~
# Import modules
# ~~~~~~~~~~
import re
import os


# ~~~~~~~~~~
# Testing area (may need to move in order to test)
# ~~~~~~~~~~



# ~~~~~~~~~~
# Define variables
# ~~~~~~~~~~
cnt = 0
test01 = '--------------RICARDO TEST----------------'
dict_interface = {'KEY': 'VALUE'}
dict_switchport_mode = {}

# ~~~~~~~~~~
# Define regex
# ~~~~~~~~~~
re_interface = r"^interface\s([A-Za-z]*\d{1,3}\/\d{1,3}\/\d{1,3})" # Capture group ex. [GigabitEthernet2/2/44]
re_switchport_access_vlan = r"\sswitchport\saccess\svlan\s(\d*)" # Capture group vlan number ex. [20]
re_switchport_mode = r"(\sswitchport\smode\s)(\w*)" # Capture group (2): [ switchport mode ][access or trunk]
regex_ip_address = r"(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})"

# ~~~~~~~~~~
# Define functions
# ~~~~~~~~~~
def def_open_file():
    global var_open_ui_filename
    with open(ui_filename, 'r') as var_open_ui_filename: # opens file, reads file and store in variable
        var_open_ui_filename = [line.rstrip('\n') for line in var_open_ui_filename]

		

def def_re_out_openfile_get_ip():
	for line in var_open_ui_filename:
		#print (line) test
		if re.search(regex_ip_address, line):
			re_match_ip = re.search(regex_ip_address, line)
			
			var_re_match_ip = re_match_ip.group(0)
			
			print (var_re_match_ip)
		
# ~~~~~~~~~~
# Start program here
# User input
# ~~~~~~~~~~
ui_filename = input('Enter filename: ')
		
		
# ~~~~~~~~~~
# Call functions
# ~~~~~~~~~~		
def_open_file()
def_re_out_openfile_get_ip()
