#!/usr/local/bin/python3

# By: Ricardo Diaz
# Date: 20181016
# Python3
# Name: pexpect_test_ver_1.08.py
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


# ~~~~~~~~~~
# Define variables
# ~~~~~~~~~~
testline = ('-' * 15 + 'TESTING LINE' + '-' * 15) # --------------TESTING LINE---------------
space01 = ('=' * 15 + '\n')
space02 = ('\n' + '=' * 15 + '\n')
ssh_newkey = ('Are you sure you want to continue connecting')
diffie_hellman_group1_sha1 = ('no matching key exchange method found. Their offer: diffie-hellman-group1-sha1')
#hostname = ('172.16.26.3')
#username = ('rdiaz')
#password = ('Password01$')
enable = ('your enable password')
hashtag = ('#')

#ui_ip_filename = ('ip_file') # TESTING
#ui_command_filename = ('command_file') #TESTING


# ~~~~~~~~~~
# Define functions
# ~~~~~~~~~~
def def_test():
    print ('testing function')
    print (var_hostname)

def def_write_filenames_to_file():
    os.chdir(path)
    os.system("ls > qfilenames.txt")

def def_change_directory():
    os.chdir(path)

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

# Function will open user input (ui) ip list file
def def_open_ip_file():
    global var_open_ui_ip_filename
    with open(ui_ip_filename, 'r') as var_open_ui_ip_filename: # opens file, reads file and store in variable
        var_open_ui_ip_filename = [line.rstrip('\n') for line in var_open_ui_ip_filename]

# Function will open user input (ui) command list file
def def_open_command_file():
    global var_open_ui_command_filename
    with open(ui_command_filename, 'r') as var_open_ui_command_filename: # opens file, reads file and store in variable
        var_open_ui_command_filename = [line.rstrip('\n') for line in var_open_ui_command_filename]

# Function to send show command(s) once logged into device
def def_send_show_command():
    def_change_directory()
    #print ('------------------------------->' + hostname)
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
def def_ssh_new_key():
    global child
    global var_next_device
    var_next_device = (0) # 0 means good. If value is later on changed to 1, will continue with next IP in list
    #print (var_next_device)
    ssh = 'ssh ' + (username) + '@' +(hostname_ip)
    ssh_dh = 'ssh -l ' + (username) + ' -oHostKeyAlgorithms=+ssh-dss -oKexAlgorithms=+diffie-hellman-group1-sha1 ' + (hostname_ip)
    child = pexpect.spawn(ssh) #'ssh ' + (username) + '@' +(hostname_ip)

    i = child.expect([pexpect.TIMEOUT, ssh_newkey, diffie_hellman_group1_sha1, '[Pp]assword: ']) # list/array, count starts from 0, 1, 2
    #i = child.expect([pexpect.TIMEOUT, ssh_newkey, '[Pp]assword: ']) # list/array, count starts from 0, 1, 2
    if i == 0: # Timeout
        print(space01 + 'ERROR!')
        print('SSH could not login. Here is what SSH said:' )
        print(child.before, child.after)
        while i == 0:
            var_next_device = (1)
            #print (var_next_device)
            break
        #sys.exit (1)
    if i == 1: # SSH does not have the public key. Just accept it.
        print (space01 + 'Accepting public SSH key for IP address [' + hostname_ip + ']' + space02)
        child.sendline ('yes')
        child.expect ('[Pp]assword: ')
        child.sendline(password)
        child.expect('#')
    if i == 2: # diffie_hellman_group1_sha1
        print (space01 + 'ERROR!\n[' + hostname_ip + '] No matching key exchange method found. Their offer: diffie-hellman-group1-sha1' + space02)
        child = pexpect.spawn(ssh_dh)
        i = child.expect([pexpect.TIMEOUT, ssh_newkey, diffie_hellman_group1_sha1, '[Pp]assword: ']) # list/array, count starts from 0, 1, 2
        if i == 1: # SSH does not have the public key. Just accept it.
            print (space01 + 'Accepting public SSH key for IP address [' + hostname_ip + ']' + space02)
            child.sendline ('yes')
            child.expect ('[Pp]assword: ')
            child.sendline(password)
            child.expect('#')
    if i == 3:
        print (space01 + 'EXPECTING PASSWORD (already has SSH keys) for IP [' + hostname_ip + ']' + space02)
        child.sendline(password)
        child.expect('#')

# Main function
def def_main():
    global child
    global show_command
    global var_hostname
    global var_re_match_hostname_g1

    # 1.
    # Function to login into devices regardless if devices are not reachable, ssh keys, password
    def_ssh_new_key()


    # 2. Once logged into the device
    if var_next_device == 1:
        print (space01 + 'Moving on to next device/ip in the list/file. Was not able to ssh into [' + hostname_ip + ']' + space02)
        while var_next_device == 1:
            break

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

        #print (testline)
        re_match_hostname = re.search(re_hostname, replace_str_hostname)
        var_re_match_hostname_g0 = re_match_hostname.group(0)
        var_re_match_hostname_g1 = re_match_hostname.group(1)
        #print (var_re_match_hostname_g0) # prints hostname usjol-c870-rtr-lab-01
        #print (var_re_match_hostname_g1) # prints usjol-c870-rtr-lab-01
        #print (testline)
        var_hostname = (var_re_match_hostname_g1 + hashtag)
        #print (var_hostname) # usjol-c870-rtr-lab-01#

        #def_test()

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
ui_ip_filename = input('Enter IP filename: ')
ui_command_filename = input('Enter command filename: ')
'''
Example below of file that is entered:
    Ricardo-Mac:dev rdiaz$ cat command_file
    show run | in hostname
    show clock
    show ip interface brief
    show inventory
'''
username = input('Enter username: ')
password = getpass()

# ~~~~~~~~~~
# Call functions
# ~~~~~~~~~~
def_open_ip_file()
def_open_command_file()
def_create_dir_for_backup_files()

for hostname_ip in var_open_ui_ip_filename:
    def_main()




# ~~~~~~~~~~
# Error messages
# ~~~~~~~~~~
'''
[rdiaz@chil-vm-centosjb-01 python3_scripts]$ ssh -l ipsoft 143.27.42.68
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
Someone could be eavesdropping on you right now (man-in-the-middle attack)!
It is also possible that a host key has just been changed.
The fingerprint for the RSA key sent by the remote host is
SHA256:FBzAlLRt5ykpx6mUEFddgcpIA0w5alNim6eJEHZgob8.
Please contact your system administrator.
Add correct host key in /home/rdiaz/.ssh/known_hosts to get rid of this message.
Offending RSA key in /home/rdiaz/.ssh/known_hosts:16
RSA host key for 143.27.42.68 has changed and you have requested strict checking.
Host key verification failed.




# Heist switches
143.26.239.10
192.168.100.8
192.168.100.9
192.168.100.14

$ ssh -l <USERNAME> -oHostKeyAlgorithms=+ssh-dss -oKexAlgorithms=+diffie-hellman-group1-sha1 <HOST>
ssh -l ipsoft -oHostKeyAlgorithms=+ssh-dss -oKexAlgorithms=+diffie-hellman-group1-sha1 143.26.239.10
ssh -l ipsoft 143.26.239.10
Unable to negotiate with 143.26.239.10 port 22: no matching key exchange method found. Their offer: diffie-hellman-group1-sha1
'''


# ~~~~~~~~~~
# Successful executed python scripts
# ~~~~~~~~~~
'''
Most recent tests
Ricardo-Mac:dev rdiaz$ ./pexpect_test_ver_1.06.py
===============
ERROR!
SSH could not login. Here is what SSH said:
b'' <class 'pexpect.exceptions.TIMEOUT'>
===============
Moving on to next device/ip in the list/file. Was not able to ssh into [172.16.26.4]
===============

===============
Accepting public SSH key for IP address [172.16.26.3]
===============

show run | in hostname
hostname usjol-c870-rtr-lab-01

show clock
00:13:04.185 UTC Mon Oct 15 2018

show ip interface brief
Interface                  IP-Address      OK? Method Status                Protocol
FastEthernet0              unassigned      YES unset  up                    down
FastEthernet1              unassigned      YES unset  up                    down
FastEthernet2              unassigned      YES unset  up                    down
FastEthernet3              unassigned      YES unset  up                    down
FastEthernet4              172.16.26.3     YES NVRAM  up                    up
Vlan1                      unassigned      YES NVRAM  up                    down

show inventory
NAME: "871", DESCR: "871 chassis, Hw Serial#: FHK123222TX, Hw Revision: 0x300"
PID: CISCO871-K9         , VID: V05 , SN: FHK123222TX



===============
EXPECTING PASSWORD (already has SSH keys) for IP [172.16.26.3]
===============

show run | in hostname
hostname usjol-c870-rtr-lab-01

show clock
00:13:07.870 UTC Mon Oct 15 2018

show ip interface brief
Interface                  IP-Address      OK? Method Status                Protocol
FastEthernet0              unassigned      YES unset  up                    down
FastEthernet1              unassigned      YES unset  up                    down
FastEthernet2              unassigned      YES unset  up                    down
FastEthernet3              unassigned      YES unset  up                    down
FastEthernet4              172.16.26.3     YES NVRAM  up                    up
Vlan1                      unassigned      YES NVRAM  up                    down

show inventory
NAME: "871", DESCR: "871 chassis, Hw Serial#: FHK123222TX, Hw Revision: 0x300"
PID: CISCO871-K9         , VID: V05 , SN: FHK123222TX



Ricardo-Mac:dev rdiaz$
'''


'''
# TESTING AREA
#re_hostname = (r"^hostname\s(.*)")
re_hostname = (r"hostname\s([\w|\d|-]+)")
ui_ip_filename = ('ip_file') # TESTING
ui_command_filename = ('command_file') #TESTING
abc = (b'show run | in hostname\r\nhostname usjol-fw-srx-lab-01\r\nusjol-fw-srx-lab-01')
print (abc)
#print (abc.decode('utf-8') + 'YOYOYOYOYOYOYOY')
str_abc = (abc.decode('utf-8'))
print (str_abc)
print ('test')
#print (str_abc.replace('\r', '    ').replace('\n', '    ')) # prints show run | in hostname==========hostname usjol-fw-srx-lab-01==========usjol-fw-srx-lab-01

replace_str_abc = (str_abc.replace('\r', '=====').replace('\n', '====='))
print (replace_str_abc)

re_match_test_hostname = re.search(re_hostname, replace_str_abc)
var_re_match_test_hostname_g0 = re_match_test_hostname.group(0)
var_re_match_test_hostname_g1 = re_match_test_hostname.group(1)
print (var_re_match_test_hostname_g0)
print (var_re_match_test_hostname_g1 + '#')
'''
