#!/usr/bin/python3.6

# By: Ricardo Diaz
# Date: 20181001
# Python3.6
# Name: dev_python_dictionary_ver_1.01.py
# Referance: https://www.programiz.com/python-programming/nested-dictionary

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
dict_interface = {}
dict_switchport_mode = {}

# ~~~~~~~~~~
# Define regex
# ~~~~~~~~~~
#re_interface = r"^interface\s([A-Za-z]*\d{1,3}\/\d{1,3}\/\d{1,3})" # Capture group ex. [GigabitEthernet2/2/44]
re_interface = r"^interface\s([A-Za-z]*-*[A-Za-z].*)"
re_switchport_access_vlan = r"\sswitchport\saccess\svlan\s(\d*)" # Capture group vlan number ex. [20]
re_switchport_mode = r"(\sswitchport\smode\s)(\w*)" # Capture group (2): [ switchport mode ][access or trunk]

# ~~~~~~~~~~
# Define functions
# ~~~~~~~~~~
def def_open_file():
    global var_open_ui_filename
    with open(ui_filename, 'r') as var_open_ui_filename: # opens file, reads file and store in variable
        var_open_ui_filename = [line.rstrip('\n') for line in var_open_ui_filename]

# TESTING WITH THIS FUNCTION
'''
def def_re_out_switchport_mode_and_vlan():
    for line in var_open_ui_filename: # iterate through every line (for loop)
        if re.search(re_switchport_mode, line): # every line will be matched to see if the line matches if statement/regex | \sswitchport\smode\s(\w*)
            re_match_switchport_mode = re.search(re_switchport_mode, line)
            #print (re_match_switchport_mode) # prints <_sre.SRE_Match object; span=(0, 23), match=' switchport mode access'>
            var_re_match_switchport_mode_g0 = re_match_switchport_mode.group(0)
            var_re_match_switchport_mode_g1 = re_match_switchport_mode.group(1)
            var_re_match_switchport_mode_g2 = re_match_switchport_mode.group(2)

            #print (var_re_match_switchport_mode_g0) #prints  switchport mode access
            #print (var_re_match_switchport_mode_g1) #prints  switchport mode
            #print (var_re_match_switchport_mode_g2) #prints access

            dict_switchport_mode.update({var_re_match_switchport_mode_g1: var_re_match_switchport_mode_g2})

#var_def_re_out_switchport_mode_and_vlan = (def_re_out_switchport_mode_and_vlan)#TESTING
'''

def def_re_out_interface():
    # for loop and iterate through every line
    for line in var_open_ui_filename: # iterate through every line (for loop)
        if re.search(re_interface, line): # every line will be matched to see if the line matches if statement/regex | ^interface\s([A-Za-z]*\d{1,3}\/\d{1,3}\/\d{1,3})

            #print (line)#TESTING
            re_match_interface = re.search(re_interface, line)
            #print (re_match_interface) # prints <_sre.SRE_Match object; span=(0, 30), match='interface GigabitEthernet1/0/2'>
            var_re_match_interface_g0 = re_match_interface.group(0)
            var_re_match_interface_g1 = re_match_interface.group(1)

            #print (var_re_match_interface_g0) # prints interface TenGigabitEthernet2/1/4
            #print (var_re_match_interface_g1) # prints TenGigabitEthernet2/1/4

            #dict_interface.update({var_re_match_interface_g1: cnt})
            #print (dict_interface)#TESTING

            #dict_interface[var_re_match_interface_g1] = {}


        if re.search(re_switchport_mode, line): # every line will be matched to see if the line matches if statement/regex | \sswitchport\smode\s(\w*)
            re_match_switchport_mode = re.search(re_switchport_mode, line)

            #print (line) # TESTING
            #print (re_match_switchport_mode) # prints <_sre.SRE_Match object; span=(0, 23), match=' switchport mode access'>
            var_re_match_switchport_mode_g0 = re_match_switchport_mode.group(0)
            var_re_match_switchport_mode_g1 = re_match_switchport_mode.group(1)
            var_re_match_switchport_mode_g2 = re_match_switchport_mode.group(2)
            #print (var_re_match_switchport_mode_g0) #prints  switchport mode access
            #print (var_re_match_switchport_mode_g1) #prints  switchport mode
            #print (var_re_match_switchport_mode_g2) #prints access

            #[var_re_match_interface_g1][var_re_match_switchport_mode_g1] = (var_re_match_switchport_mode_g2)
            #dict_interface.update({var_re_match_interface_g1: cnt})

            #print (test01 + '\n')

            dict_interface[var_re_match_interface_g1] = {}
            dict_interface[var_re_match_interface_g1][var_re_match_switchport_mode_g1] = var_re_match_switchport_mode_g2
            print (dict_interface)

    print ('OUT OF THE FOR LOOP')



# ~~~~~~~~~~
# Start program here
# User input
# ~~~~~~~~~~
ui_filename = input('Enter filename: ')


# ~~~~~~~~~~
# Call upon functions
# ~~~~~~~~~~
def_open_file()
def_re_out_interface()
#def_re_out_switchport_mode_and_vlan()
