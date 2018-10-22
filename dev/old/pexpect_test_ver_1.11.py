#!/usr/local/bin/python3

# By: Ricardo Diaz
# Date: 20181019
# Python3
# Name: pexpect_test_ver_1.11.py
# Requires: user input files: ip_file and ui_command_filename
'''
1: ip_file == file with list of ip addresses
2. command_file == file with show commands
Ricardo-Mac:dev rdiaz$ cat command_file
show run | in hostname
show clock
show ip interface brief
show inventory
'''

# Referance:
# https://pexpect.readthedocs.io/en/stable/
# http://pexpect.sourceforge.net/doc/
# https://stackoverflow.com/questions/31143811/pexpect-login-to-cisco-device-grab-just-the-hostname-from-the-config
# https://www.electricmonk.nl/log/2014/07/26/scripting-a-cisco-switch-with-python-and-expect/
# https://stackoverflow.com/questions/35585158/python-pexpect-regex-match-is-encased-in-b

# ~~~~~~~~~~
# Import modules
# ~~~~~~~~~~
import os
import sys
import pexpect
import time
import datetime
import re
from getpass import getpass

# ~~~~~~~~~~
# Testing area
# ~~~~~~~~~~


# ~~~~~~~~~~
# Define regex
# ~~~~~~~~~~
re_hostname = (r"hostname\s([\w|\d|-]+)") #will be regex following line | 'show run | in hostname==========hostname usjol-fw-srx-lab-01==========usjol-fw-srx-lab-01'
re_ip = (r"^(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})")

# ~~~~~~~~~~
# Define variables
# ~~~~~~~~~~
testline = ('-' * 15 + 'TESTING LINE' + '-' * 15) # --------------TESTING LINE---------------
space01 = ('=' * 15 + '\n')
space02 = ('\n' + '=' * 15 + '\n')
ssh_newkey = ('Are you sure you want to continue connecting')
diffie_hellman_group1_sha1 = ('no matching key exchange method found. Their offer: diffie-hellman-group1-sha1')
ssh_key_fail = ('Host key verification failed.')
#username = ('rdiaz')
#password = ('Password01$')
#enable = ('your enable password')
hashtag = ('#')

ui_ip_filename = ('ip_file') # TESTING
ui_command_filename = ('command_file') #TESTING


# ~~~~~~~~~~
# Define functions
# ~~~~~~~~~~
def def_test():
    print ('testing function')
    #print (var_hostname)

def def_write_filenames_to_file():
    os.chdir(path)
    os.system("ls > qfilenames.txt")

def def_change_directory():
    os.chdir(path)

def def_wrong_creds():
    global var_next_device
    var_next_device = (0)
    print ('***ERROR: Bad credentials for IP [' + hostname_ip + ']***')
    while True:
        var_next_device = (1)
        break

def def_expect_hash_tag():
    print ('hitting def_expect_hash_tag function. GOOD')
    child.expect('#')

def def_create_dir_for_backup_files():
    global path
    var_date_yyyymmdd = datetime.datetime.now().strftime("_%Y%m%d") #time into a variable

    print ("Going to create a new directory but first user will need to enter full path in which the directory will be created")

    print ("\nCURRENT DIRECTORY:\n" + space01)
    print (os.system("pwd"))
    print (space01 + "\n")

    ui_path = input('Enter full path: ')

    path = ui_path + ui_site + "_backup" + var_date_yyyymmdd
    try:
        os.mkdir(path) # creates directory. User will enter path in which new dir will be created
        #os.chdir(path) # change directory that was just created
    except OSError:
        print ("FAILED: Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)


# Function will open user input (ui) ip list file and add IP addresses to a list/array [ip_file_ips]
def def_open_ip_file():
    global ip_file_ips
    ip_file_ips = [] #Create empty directory, will append ip addresses once regex
    with open(ui_ip_filename, 'r') as var_open_ui_ip_filename: # opens file, reads file and store in variable
        var_open_ui_ip_filename = [line.rstrip('\n') for line in var_open_ui_ip_filename]
        # Below is new code
        for line in var_open_ui_ip_filename:
            re_match_ip = re.search(re_ip, line)
            var_re_match_ip_g0 = re_match_ip.group(0)
            var_re_match_ip_g1 = re_match_ip.group(1)
            ip_file_ips.append(var_re_match_ip_g0)


# Function will open user input (ui) command list file
def def_open_command_file():
    global var_open_ui_command_filename
    with open(ui_command_filename, 'r') as var_open_ui_command_filename: # opens file, reads file and store in variable
        var_open_ui_command_filename = [line.rstrip('\n') for line in var_open_ui_command_filename]


def def_verify_password():
    ssh_expect_list = child.expect([pexpect.TIMEOUT, ssh_newkey, diffie_hellman_group1_sha1, ssh_key_fail, '[Pp]assword: ', '#'])
    if ssh_expect_list == 5: # expecting '#'
        print ('***Loging into IP [' + hostname_ip + ']***')
    if ssh_expect_list == 4: # expecting 'Password', meaning that the password was incorrect
        def_wrong_creds()


# Function to send show command(s) once logged into device
def def_send_show_command():
    #def_change_directory() #UNCOMMENT WHEN DONE TESTING

    child.sendline(show_command)
    #child.expect('#') # run into issue if the output has "#" in the first line (example is [show inventory])
    # EXAMPLE BELOW
    '''
    usjol-c870-rtr-lab-01#show inventory
    NAME: "871", DESCR: "871 chassis, Hw Serial#: FHK123222TX, Hw Revision: 0x300"
    PID: CISCO871-K9         , VID: V05 , SN: FHK123222TX


    usjol-c870-rtr-lab-01#
    '''
    child.expect(var_hostname)
    output =  child.before
    output = output.decode("utf-8")

    print (output) # prints out all output of the show commands
    with open (ui_site + '_' + ui_describe_file + '_' + var_re_match_hostname_g1 + '_' + hostname_ip + '.txt', 'a') as var_write_to_file:
            var_write_to_file.write(space01 + 'COMMAND: ' + show_command + space02)
            var_write_to_file.write(output)
            var_write_to_file.write('\n')


# Function to login into devices regardless if devices are not reachable, ssh keys, password
def def_ssh_to_host():
    global child
    global var_next_device
    var_next_device = (0) # 0 means good. If value is later on changed to 1, will continue with next IP in list

    ssh = 'ssh ' + (username) + '@' +(hostname_ip)
    ssh_dh = 'ssh -l ' + (username) + ' -oHostKeyAlgorithms=+ssh-dss -oKexAlgorithms=+diffie-hellman-group1-sha1 ' + (hostname_ip)

    child = pexpect.spawn(ssh) #'ssh ' + (username) + '@' +(hostname_ip)

    i = child.expect([pexpect.TIMEOUT, ssh_newkey, diffie_hellman_group1_sha1, ssh_key_fail, '[Pp]assword: ', '#']) # list/array, count starts from 0, 1, 2, 3
    #0 - pexpect.TIMEOUT
    #1 - ssh_newkey
    #2 - diffie_hellman_group1_sha1
    #3 - ssh_key_fail
    #4 - [Pp]assword
    #5 - #

    if i == 0: # Timeout
        print(space01 + 'ERROR!')
        print('SSH could not login. Here is what SSH said:' )
        print(child.before, child.after)
        while i == 0:
            var_next_device = (1)
            break

    if i == 1: # SSH does NOT have the public key. Just accept it.
        print ('***Accepting public SSH key for IP address [' + hostname_ip + ']***')
        child.sendline ('yes')
        child.expect ('[Pp]assword: ')
        child.sendline(password)
        def_verify_password()

    if i == 2: # diffie_hellman_group1_sha1
        print (space01 + 'ERROR!\n[' + hostname_ip + '] No matching key exchange method found. Their offer: diffie-hellman-group1-sha1' + space02)
        child = pexpect.spawn(ssh_dh) #'ssh -l '+(username)+' -oHostKeyAlgorithms=+ssh-dss -oKexAlgorithms=+diffie-hellman-group1-sha1 '+(hostname_ip)

        i2 = child.expect([pexpect.TIMEOUT, ssh_newkey, diffie_hellman_group1_sha1, ssh_key_fail, '[Pp]assword: ', '#'])
        if i2 == 4: # expecting 'PASSWORD'
            # Run if the the local host has the public key
            child.sendline(password)
            def_verify_password()
        elif i2 == 1: # SSH does not have the public key. Just accept it.
            print ('Accepting public SSH key for IP address [' + hostname_ip + ']')
            child.sendline ('yes')
            child.expect ('[Pp]assword: ')
            child.sendline(password)
            def_verify_password()

    # NEED TO ADDRESS THE BELOW.
    if i == 3: # Host key verification failed.
        print ('i == 3')
        print (space01 + 'Host key verification fail for [' + hostname_ip + ']')
        while i == 3:
            var_next_device = (1)
            break

    if i == 4: # Expecting '[Pp]assword: '
        print (space01 + 'Expecting password (This host already has SSH keys) for IP [' + hostname_ip + ']' + space02)
        child.sendline(password)
        def_verify_password()


# Main function
def def_main():
    global child
    global show_command
    global var_hostname
    global var_re_match_hostname_g1

    # 1.
    # Function to login into devices regardless if devices are not reachable, ssh keys, password
    def_ssh_to_host()
    #print (testline)
    #print (var_next_device) #TESTING

    # 2. If there are issues ssh into device (timeout, not online or host key verification failed)
    if var_next_device == 1:
        print (space01 + 'Moving on to next device/ip in the list/file. Was not able to ssh into [' + hostname_ip + ']' + space02)
        while var_next_device == 1:
            break

    # 3. Once logged into the device
    if var_next_device == 0:
        # Get hostname of the switch/router
        child.sendline('show run | in hostname')
        child.expect('#')
        byte_hostname = child.before # b'show run | in hostname\r\nhostname usjol-c870-rtr-lab-01\r\nusjol-c870-rtr-lab-01'
        #print (byte_hostname) # TEST prints b'show run | in hostname\r\nhostname usjol-c870-rtr-lab-01\r\nusjol-c870-rtr-lab-01'

        str_hostname = byte_hostname.decode('utf-8') # decoding bytes to string
        #print (str_hostname) # TEST prints the string as well as newlines \n and carriage \r (dont want this)
        '''
        show run | in hostname
        hostname usjol-c870-rtr-lab-01
        usjol-c870-rtr-lab-01
        '''
        replace_str_hostname = (str_hostname.replace('\r', '=====').replace('\n', '====='))
        #print (replace_str_hostname) # show run | in hostname==========hostname usjol-c870-rtr-lab-01==========usjol-c870-rtr-lab-01

        # Regex for hostname (group 1)
        re_match_hostname = re.search(re_hostname, replace_str_hostname)
        #var_re_match_hostname_g0 = re_match_hostname.group(0)
        var_re_match_hostname_g1 = re_match_hostname.group(1)
        #print (var_re_match_hostname_g0) # prints hostname usjol-c870-rtr-lab-01
        #print (var_re_match_hostname_g1) # prints usjol-c870-rtr-lab-01
        var_hostname = (var_re_match_hostname_g1 + hashtag)
        #print (var_hostname) # usjol-c870-rtr-lab-01#

        # FOR loop: for every show command found in file (var_open_ui_command_filename), call the FUNCTION [def_send_show_command()]
        for show_command in var_open_ui_command_filename:
            def_send_show_command()


# ~~~~~~~~~~
# Start program here
# User input
# ~~~~~~~~~~
ui_site = input("Enter site: ")
print ('[example: backup|interfaces|cdp_neighbors]')
ui_describe_file = input('Describe type of file: ')
#ui_ip_filename = input('Enter IP filename: ')
#ui_command_filename = input('Enter command filename: ')
username = input('Enter username: ')
password = getpass()

# ~~~~~~~~~~
# Call functions
# ~~~~~~~~~~
def_open_ip_file()
def_open_command_file()
#def_create_dir_for_backup_files()

for hostname_ip in ip_file_ips:
    def_main()




# ~~~~~~~~~~
# Error messages
# ~~~~~~~~~~
