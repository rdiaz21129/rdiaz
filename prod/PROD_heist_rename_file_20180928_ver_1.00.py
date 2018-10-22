#!/usr/bin/python2.7

# By: Ricardo Diaz
# Date: 20180928
# Python2.7
# Name: PROD_heist_rename_file_20180928_ver_1.00.py
# Referance:


# ~~~~~~~~~~
# Import modules
# ~~~~~~~~~~
import re
import os


# ~~~~~~~~~~
# Define variables
# ~~~~~~~~~~
cnt = 0
test01 = '--------------RICARDO TEST----------------'
dict = {}


# ~~~~~~~~~~
# Define regex
# ~~~~~~~~~~
regex_cisco_hostname = r"^hostname\s+([\w\d\-]*)"
regex_ip_address = r"(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})"

# CHANGE "HEIST" TO SITE NAME, EX "AARSCHOT_PLANT"
regex_sw_backup_filename = r"(HEIST_backup_)(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}.txt)"

# ~~~~~~~~~~
# Define functions
# ~~~~~~~~~~
# regex out the file name for group 1
def def_regexout_filename_group01(sw_name):
    #regex_sw_backup_filename = r"(HEIST_backup_)(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}.txt)"
    match_filename = re.search(regex_sw_backup_filename, sw_name)
    #print 'GROUP 1: ' + match_filename.group(1) # prints [HEIST_backup_]
    group01_regexout_file = match_filename.group(1)
    return group01_regexout_file

# regex out the file name for group 2
def def_regexout_filename_group02(sw_name):
    #regex_sw_backup_filename = r"(HEIST_backup_)(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}.txt)"
    match_filename = re.search(regex_sw_backup_filename, sw_name)
    group02_regexout_file = match_filename.group(2)
    #print group02_regexout_file # **TEST**
    return group02_regexout_file

# functions that opens file and searches the file for a line begining with [hostname XXXXX], returns the regex group 01 (hostname)
def def_open_file_and_search_hostname(sw_name):
    with open(sw_name, 'r') as var_openFile:
        var_openFile = [line.rstrip('\n') for line in var_openFile]

        # function variables
        no_match_count = 0
        match_count = 0

        # for loop and iterate through every line
        for line in var_openFile: # iterate through every line (for loop)
            # **TEST** print line # usesd for testing

            if re.search(regex_cisco_hostname, line): # every line will be matched to see if the line matches if statement
                match_hostname = re.search(regex_cisco_hostname, line)
                # **TEST** print "capture group 0 = " + match_hostname.group(0) # print full line in which regex stays
                # **TEST** print "capture group 1 = " + match_hostname.group(1) # prints [capture group 1 only]
                match_count = match_count +1 # should be only one

            else:
                no_match_count = no_match_count +1
                #print "Number of lines that did not match if statment: " + str(c)

        print "Number of lines that matched the regex ^hostname\s+([\w\d\-]*) : " + str(match_count)
        print "Number of lines that did not match if statment: " + str(no_match_count)
        var_output_hostname = match_hostname.group(1)
        return var_output_hostname

        print '----- LAST LINE IN FUNCTION -----'

# Rename file
def def_os_rename_file(sw_name):
    os.rename(sw_name, var_def_regexout_filename_group01 + var_def_open_file_and_search_hostname + '_' + var_def_regexout_filename_group02)

# 1st function that will be ran. This will open the file and use the file name
def def_single_out_sw_filename():
    global var_def_regexout_filename_group01
    global var_def_regexout_filename_group02
    global var_def_open_file_and_search_hostname
    global var_def_os_rename_file

    with open(UI_file_list_of_switches, 'r') as var_open_UI_file_list_of_switches:
        var_open_UI_file_list_of_switches = [line.rstrip('\n') for line in var_open_UI_file_list_of_switches]
    for sw_name in var_open_UI_file_list_of_switches:
        #def_regexout_filename_group01(sw_name)
        var_def_regexout_filename_group01 = def_regexout_filename_group01(sw_name)
        var_def_regexout_filename_group02 = def_regexout_filename_group02(sw_name)
        var_def_open_file_and_search_hostname = def_open_file_and_search_hostname(sw_name)
        var_def_os_rename_file = def_os_rename_file(sw_name)


# test function
def def_example():
    x = os.popen('cat ip_list').readlines() # User enters command
    # **TEST** print x # test
    for line in x:
        line = line.replace('\n', '') #removes return '\n'
        print line

# ~~~~~~~~~~
# User input
# ~~~~~~~~~~
UI_file_list_of_switches = raw_input('Enter filename that list all the switches: ')

# ~~~~~~~~~~
# Call upon functions
# ~~~~~~~~~~
# Returns from functions
def_single_out_sw_filename()


# ~~~~~~~~~~
# Testing area (may need to move in order to test)
# ~~~~~~~~~~
'''
user_in_filename = raw_input

os.rename('filename01.txt', 'filename01_modified.txt')


if re.search(regex_cisco_hostname, "hostname uschicsw01"):
    match = re.search(regex_cisco_hostname, "hostname uschicsw01")
    print "hostname uschicsw01"
    print match
    print "This regex is capture group 0 (matches all) = [" + match.group(0) + "]"
    print "This regex is capture group 1 = [" + match.group(1) + "]"


#match = re.search(regex_cisco_hostname, "hostname usCHIcsw01")
#print "capture group 0 = " + match.group(0) # print [hostname usCHIcsw01]
#print "capture group 1 = " + match.group(1) # prints only [usCHIcsw01]



def return_sum(x,y):
    c = x + y
    return c

res = return_sum(4,5)
print(res)

# result == prints [9]
'''
