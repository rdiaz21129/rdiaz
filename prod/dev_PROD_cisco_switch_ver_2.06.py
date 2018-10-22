#!/usr/bin/python2.7

# By: Ricardo Diaz
# Date: 20180923
# Python2.7
# Name: dev_PROD_cisco_switch_ver_2.06.py
# Referance: https://pynet.twb-tech.com/blog/automation/netmiko-proxy.html

# ~~~~~~~~~~
# Import modules
# ~~~~~~~~~~
from netmiko import ConnectHandler
from getpass import getpass
import re
import os
import time
import datetime

# ~~~~~~~~~~
# Test
# ~~~~~~~~~~
#user_commands_list = ['show clock', 'show interface status | in connected', 'show ip arp', 'show ver | in uptime']

space01 = '# =========='

list_user_commands = []
print "\n" + space01 + "\n" + "Enter up to [5] show commands: \nType the word [done] when complete.\n" + space01 + "\n"
'''
# ==========
Enter up to [5] show commands:
Type the word [done] when complete.
# ==========
'''
def def_manual_user_input():
	list_user_commands_counter = 1
	while True:
		#print list_user_commands_counter # TESTING
		user_commands_list = raw_input("enter show command: : ").lower()

		if user_commands_list == "done" or list_user_commands_counter == 6:
			break

		if user_commands_list != "done" and list_user_commands_counter < 6:
			list_user_commands.append(user_commands_list)
			list_user_commands_counter = list_user_commands_counter + 1


def_manual_user_input()


# ip address should be ip address in the ~/.ssh/config file
'''
/home/rdiaz/.ssh/config

host 10.40.255.21           # Cisco switch at Duracell 135
  user ipsoftnetwork
  hostname 10.40.255.21
  Port 22
  ProxyCommand ssh 172.18.80.118 nc %h %p

host 10.40.255.22           # Cisco switch at Duracell 135
  user ipsoftnetwork
  hostname 10.40.255.22
  Port 22
  ProxyCommand ssh 172.18.80.118 nc %h %p

'''
# ~~~~~~~~~~
# Define variables
# ~~~~~~~~~~
var_current_pwd = os.system("pwd")

var_show_run = 'show run'
var_show_ip_arp = 'show ip arp'
var_show_mac_add = 'show mac address-table'
var_show_vlan_br = 'show vlan brief'
var_show_int_trunk = 'show interface trunk'
var_show_cdp_neigh = 'show cdp neigh'
var_show_clock = 'show clock'
var_show_inventory = 'show inventory'
var_show_int_status = 'show interface status'
var_show_ver_inc_uptime = 'show version | include uptime'
var_show_interface_counters = 'show interface counters'
var_wr_mem = 'write memory'
var_show_run_include_hostname = 'show run | include hostname'
var_show_interface_status = 'show interface status'

var_clear_counters = 'clear counters'

border = '===============\n'
border0 = '===============\n\n'
border1 = '\n===============\n'
border2 = '\n\n===============\n'
space01 = '# =========='

cnt = 0
test01 = '--------------RICARDO TEST----------------'
dict = {}
UI_file_list_of_switches = 'qfilenames.txt'


# ~~~~~~~~~~
# Define regex
# ~~~~~~~~~~
regex_cisco_hostname = r"^hostname\s+([\w\d\-]*)"
regex_ip_address = r"(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})"
regex_sw_backup_filename = r"([A-Z]+_backup_)(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}.txt)"


# ~~~~~~~~~~
# Define Functions
# ~~~~~~~~~~
def def_test_():
    print "TESTING FUNCTION!"
    #exit()

def def_write_filenames_to_file():
    os.chdir(path)
    os.system("ls > qfilenames.txt")

def def_change_directory():
    os.chdir(path)

def def_login_run_command(show_command):
    def_change_directory()
    net_connect = ConnectHandler(**cisco)
	print net_connect
    output_show_command = net_connect.send_command(show_command)
    with open (site + '_backup_' + ip_addr+'.txt', 'a') as var_f_show:
        var_f_show.write(border2) #Appends output to file
        var_f_show.write('COMMAND: ' + show_command + '\n' + border0)
        var_f_show.write(output_show_command + '\n\n') #Appends output to file
        #var_f_show.write(border1) #Appends output to file
    print net_connect.find_prompt()
    print show_command + ' WORKS!'


def def_show_clock():
    def_change_directory()
    net_connect = ConnectHandler(**cisco)
    output_show_clock = net_connect.send_command(var_show_clock)
    with open (site + '_backup_' + ip_addr+'.txt', 'a') as var_f_show_clock:
        var_f_show_clock.write(border2) #Appends output to file
        var_f_show_clock.write('COMMAND: ' + var_show_clock + '\n' + border0)
        var_f_show_clock.write(output_show_clock + '\n\n') #Appends output to file
        #var_f_show_clock.write(border1) #Appends output to file
    print net_connect.find_prompt()
    print var_show_clock + ' WORKS!'

def def_show_uptime():
    def_change_directory()
    net_connect = ConnectHandler(**cisco)
    output_show_uptime = net_connect.send_command(var_show_ver_inc_uptime)
    with open (site + '_backup_' + ip_addr+'.txt', 'a') as var_f_show_uptime:
        var_f_show_uptime.write(border2) #Appends output to file
        var_f_show_uptime.write('COMMAND: ' + var_show_ver_inc_uptime + '\n' + border0)
        var_f_show_uptime.write(output_show_uptime + '\n\n') #Appends output to file
        #var_f_show_uptime.write(border1) #Appends output to file
    print net_connect.find_prompt()
    print var_show_ver_inc_uptime + ' WORKS!'

def def_show_interface_status():
    def_change_directory()
    net_connect = ConnectHandler(**cisco)
    output_show_interface_status = net_connect.send_command(var_show_interface_status)
    with open (site + '_backup_' + ip_addr+'.txt', 'a') as var_f_show_interface_counters:
        var_f_show_interface_counters.write(border2) #Appends output to file
        var_f_show_interface_counters.write('COMMAND: ' + var_show_interface_status + '\n' + border0)
        var_f_show_interface_counters.write(output_show_interface_status + '\n\n') #Appends output to file
        #var_f_show_interface_counters.write(border1) #Appends output to file
    print net_connect.find_prompt()
    print var_show_interface_status + ' WORKS!'

def def_show_interface_counters():
    def_change_directory()
    net_connect = ConnectHandler(**cisco)
    output_show_interface_counters = net_connect.send_command(var_show_interface_counters)
    with open (site + '_backup_' + ip_addr+'.txt', 'a') as var_f_show_interface_counters:
        var_f_show_interface_counters.write(border2) #Appends output to file
        var_f_show_interface_counters.write('COMMAND: ' + var_show_interface_counters + '\n' + border0)
        var_f_show_interface_counters.write(output_show_interface_counters + '\n\n') #Appends output to file
        #var_f_show_interface_counters.write(border1) #Appends output to file
    print net_connect.find_prompt()
    print var_show_interface_counters + ' WORKS!'

def def_show_inventory():
    def_change_directory()
    net_connect = ConnectHandler(**cisco)
    output_show_inventory = net_connect.send_command(var_show_inventory)
    with open (site + '_backup_' + ip_addr+'.txt', 'a') as var_f_show_inventory:
        var_f_show_inventory.write(border + 'COMMAND: ' + var_show_inventory + '\n' + border0)
        var_f_show_inventory.write(output_show_inventory)
        var_f_show_inventory.write(border0 + '\n\n')
    print net_connect.find_prompt()
    print var_show_inventory + ' WORKS!'

def def_show_cdp_neigh():
    def_change_directory()
    net_connect = ConnectHandler(**cisco)
    output_show_cdp_neigh = net_connect.send_command(var_show_cdp_neigh)
    with open (site + '_backup_' + ip_addr+'.txt', 'a') as var_f_cdp_neighbors:
        var_f_cdp_neighbors.write(border + 'COMMAND: ' + var_show_cdp_neigh + '\n' + border0)
        var_f_cdp_neighbors.write(output_show_cdp_neigh + '\n') #Appends output to file
        var_f_cdp_neighbors.write(border0 + '\n\n')
    print net_connect.find_prompt()
    print var_show_cdp_neigh + ' WORKS!'

def def_show_ip_arp():
    def_change_directory()
    net_connect = ConnectHandler(**cisco)
    output_show_ip_arp = net_connect.send_command(var_show_ip_arp)
    # Open file and write to file (show ip arp output)
    with open(site + '_backup_' + ip_addr+'.txt', 'a') as var_f_ip_arp:
        var_f_ip_arp.write(border + 'COMMAND: ' + var_show_ip_arp + '\n' + border0)
        var_f_ip_arp.write(output_show_ip_arp + '\n') #Appends output to file
        var_f_ip_arp.write(border0 + '\n\n')
    print net_connect.find_prompt()
    print var_show_ip_arp + ' WORKS!'

def def_show_mac_add():
    def_change_directory()
    net_connect = ConnectHandler(**cisco)
    output_show_mac_add = net_connect.send_command(var_show_mac_add)
    with open(site + '_backup_' + ip_addr+'.txt', 'a') as var_f_mac_add:
        var_f_mac_add.write(border + 'COMMAND: ' + var_show_mac_add + '\n' + border0)
        var_f_mac_add.write(output_show_mac_add + '\n') #Appends output to file
        var_f_mac_add.write(border0 + '\n\n')
    print net_connect.find_prompt()
    print var_show_mac_add + ' WORKS!'

def def_show_run():
    def_change_directory()
    net_connect = ConnectHandler(**cisco)
    output_show_run = net_connect.send_command(var_show_run)
    with open(site + '_backup_' + ip_addr+'.txt', 'a') as var_f_run:
        var_f_run.write(border + 'COMMAND: ' + var_show_run + '\n' + border0)
        var_f_run.write(output_show_run) #Appends output to file
        var_f_run.write(border0 + '\n\n')
    print net_connect.find_prompt()
    print var_show_run + ' WORKS!'

def def_show_int_trunk():
    def_change_directory()
    net_connect = ConnectHandler(**cisco)
    output_show_int_trunk = net_connect.send_command(var_show_int_trunk)
    with open(site + '_backup_' + ip_addr+'.txt', 'a') as var_f_int_trunk:
        var_f_int_trunk.write(border + 'COMMAND: ' + var_show_int_trunk + '\n' + border0)
        var_f_int_trunk.write(output_show_int_trunk + '\n') #Appends output to file
        var_f_int_trunk.write(border0 + '\n\n')
    print net_connect.find_prompt()
    print var_show_int_trunk + ' WORKS!'

def def_show_vlan_br():
    def_change_directory()
    net_connect = ConnectHandler(**cisco)
    output_show_vlan_br = net_connect.send_command(var_show_vlan_br)
    with open(site + '_backup_' + ip_addr+'.txt', 'a') as var_f_vlan_br:
        var_f_vlan_br.write(border + 'COMMAND: ' + var_show_vlan_br + '\n' + border0)
        var_f_vlan_br.write(output_show_vlan_br + '\n') #Appends output to file
        var_f_vlan_br.write(border0 + '\n\n')
    print net_connect.find_prompt()
    print var_show_vlan_br + ' WORKS!'

def def_show_run_include_hostname():
    def_change_directory()
    net_connect = ConnectHandler(**cisco)
    output_show_vlan_br = net_connect.send_command(var_show_run_include_hostname)
    with open(site + '_backup_' + ip_addr+'.txt', 'a') as var_f_show_run_I_hostname:
        var_f_show_run_I_hostname.write(border + 'COMMAND: ' + var_show_run_include_hostname + '\n' + border0)
        var_f_show_run_I_hostname.write(output_show_vlan_br + '\n') #Appends output to file
        var_f_show_run_I_hostname.write(border0 + '\n\n')
    print net_connect.find_prompt()
    print var_show_run_include_hostname + ' WORKS!'

def def_clear_counters():
    #def_change_directory()
    net_connect = ConnectHandler(**cisco)
    #Clear "show interface" counters on all interfaces [confirm]
    #output_clear_counters = net_connect.send_command(var_clear_counters)
    output_clear_counters = net_connect.send_command_timing("clear counters")
    if '[confirm]' in output_clear_counters:
        output_clear_counters += net_connect.send_command_timing("y")
    print net_connect.find_prompt()
    print var_clear_counters + ' WORKS!'

def def_write_memory():
    net_connect = ConnectHandler(**cisco)
    output_wr_mem = net_connect.send_command(var_wr_mem)
    print net_connect.find_prompt()
    print var_wr_mem + ' WORKS!'

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
        if sw_name == "qfilenames.txt":
            print "FOUND qfilenames.txt file:"
        else:
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

def def_change_directory():
    os.chdir(path)

def def_create_dir_for_backup_files():
    global path
    var_date_yyyymmdd = datetime.datetime.now().strftime("_%Y%m%d") #time into a variable

    print "Going to create a new directory but first user will need to enter full path in which the directory will be created"

    print "\nCURRENT DIRECTORY:\n" + space01
    print os.system("pwd")
    print space01 + "\n"

    UI_path = raw_input('Enter full path: ')

    path = UI_path + site + "_backup" + var_date_yyyymmdd
    try:
        os.mkdir(path) # creates directory. User will enter path in which new dir will be created
        #os.chdir(path) # change directory that was just created
    except OSError:
        print ("FAILED: Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)


def def_question_port_usage():
    global UI_clear_counters
    global UI_clear_counters
    UI_clear_counters = raw_input('Do you want to clear the interface counters? (yes or no): ')
    UI_clear_counters = UI_clear_counters.lower() # makes user input lower case

    # ~~~~~~~~~~
    # Create new directory (call function) | (Seq: 2)
    # ~~~~~~~~~~
    if UI_clear_counters == 'yes':
        print 'Not going to create a new directory...'
    else:
        def_create_dir_for_backup_files()

def def_ask_port_usage():
    ask_user_port_utilization = raw_input('To run port usage program enter "1": ')

    if ask_user_port_utilization == "1":
        def_question_port_usage()
    else:
        print ""



# ~~~~~~~~~~
# MASTER FUNCTIONS THAT CALL ALL FUNCTIONS - CURRENTLY LIMITED TO USING ONLY 5
# ~~~~~~~~~~
#1: Backup script A:
def def_backup_a():
    def_show_clock()
    def_show_inventory()
    def_show_cdp_neigh()
    def_show_int_trunk()
    def_show_vlan_br()
    #def_show_uptime()
    #def_show_interface_counters()

#2: Backup script B:
def def_backup_b():
    def_show_clock()
    def_show_ip_arp()
    def_show_interface_status()
    def_show_mac_add()
    def_show_run()

#3: Port usage:
def def_port_usage():
    def_show_clock()
    def_show_uptime()
    def_show_interface_counters()
    def_show_run_include_hostname()
    #def_show_run()

#4: Save switch configuration (write memory):
def def_save_switch_config():
    def_write_memory()


# ~~~~~~~~~~
# Start of program
# User Input - Define global variables | (Seq: 1)
# ~~~~~~~~~~
print space01 +'\nPick what program you would like to run\n' + space01 + '\n'
print '#1: Backup script A\n#2: Backup script B:\n#3: Port usage:\n#4: Save switch configuration (write memory)\n#5: Manual show commands. User will enter show commands they\'d like to run\n'
'''
# ==========
Pick what program you would like to run
# ==========

#1: Backup script A
#2: Backup script B
#3: Port usage
#4: Save switch configuration (write memory)
#5: Manual show commands. User will enter show commands they'd like to run
'''


UI_number = raw_input('#: ')

site = raw_input('Enter site: ') # User Input - user enters site
file = raw_input('Enter filename that contains switch IPs: ') # User Input - user enters filename
username = raw_input('Enter username: ') # User Input - user enters username
password = getpass() # User Input - user enters password

# ~~~~~~~~~~
# Create new directory (call function) | (Seq: 2)
# ~~~~~~~~~~
#3: Port usage
if UI_number == '3':
    def_question_port_usage() # Create only if we are NOT going to clear the counters. run different function if we are to clear the counters

elif UI_number in ['1','2','5']:
    print '\n' + space01 + '\nIf not already, will need to create directory for backup config files:\n' + space01
    raw_input('Press enter key to continue: ')
    def_create_dir_for_backup_files() # Create directory if not already created

else:
    raw_input('You entered [' + UI_number + '] ' + 'which is NOT 1, 2, 3, or 5:\nPress Enter to continue:')
    print 'TEEEEEEEESSSSSST'
    def_create_dir_for_backup_files()


# ~~~~~~~~~~
# Open file entered by user
# ~~~~~~~~~~
with open(file, 'r') as var_openFile:
    var_openFile = [line.rstrip('\n') for line in var_openFile]

# ~~~~~~~~~~
# Iterate through file entered by user
# ~~~~~~~~~~
for ip in var_openFile:
    ip_addr = ip
    #ip_addr = raw_input("Enter IP Address: ").strip()
    #password = getpass() # User Input - user enters password
    #def_test_print(ip_addr)

    # ~~~~~~~~~~
    # Cisco Dictionary
    # ~~~~~~~~~~
    cisco = {
        'device_type': 'cisco_ios',
        'ip': ip_addr,
        'username': username,
        'password': password,
        'port': 22,
        'ssh_config_file': '~/.ssh/config',
        'verbose': False,
    }

    # ~~~~~~~~~~
    # Call functions (Seq: 3)
    # ~~~~~~~~~~
    if UI_number == '1':
        print space01 + '\nYou selected option 1: Backup script A\n' + space01 + '\n'
        def_backup_a()

    elif UI_number == '2':
        print space01 + '\nYou selected option 2: Backup script B\n' + space01 + '\n'
        def_backup_b()

    elif UI_number == '3':
        if UI_clear_counters == 'yes':
            print '\n' + space01 + '\nLoging into device and clearing interface counters\n' + space01
            def_clear_counters()
        elif UI_clear_counters == 'no':
            print '\n' + space01 + '\nLoging into device and tacking interface counters statistics, and putting them into a file.\n' + space01
            def_port_usage()
        else:
            raw_input(UI_clear_counters + ' IS WHAT THE USER ENTERED, NOT YES OR NO')

    elif UI_number == '4':
        print '\n' + space01 + '\nYou selected option 4: Save switch configuration (write memory)\n' + space01
        #def_test_()
        def_save_switch_config()

	elif UI_number == '5':
		print space01 + '\nYou selected option 5: Manual show commands\n' + space01 + '\n'
		for show_command in list_user_commands:
			def_login_run_command(show_command)

    else:
        print "ERROR"
