#!/usr/local/bin/python3

# By: Ricardo Diaz
# Date: 20181014
# Python3
# Name: pexpect_test_ver_1.04.py
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
import re

# ~~~~~~~~~~
# Testing area
# ~~~~~~~~~~
'''
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
#hostname = ('172.16.26.3')
username = ('rdiaz')
password = ('Password01$')
enable = ('your enable password')
hashtag = ('#')
# Testing variables below
test_hostname = ('hostname 181-chicago-core-01')
ui_ip_filename = ('ip_file') # TESTING
ui_command_filename = ('command_file') #TESTING


# ~~~~~~~~~~
# Define functions
# ~~~~~~~~~~
def def_test():
    print ('testing function')
    print (var_hostname)

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
    print (output)

# Function to login into device (ssh)
def def_login_to_device():
    global child
    global show_command
    global var_hostname #TESTING
    ssh = 'ssh ' + (username) + '@' +(hostname_ip)
    child = pexpect.spawn(ssh) #'ssh ' + (username) + '@' +(hostname_ip)
    child.expect('word')
    child.sendline(password) # Send password
    #print (space01 + 'Logged into device ' + hostname_ip + space02)
    child.expect('#')

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
#ui_username = input('Enter username: ')
#ui_password = input('Enter password: ')


# ~~~~~~~~~~
# Call functions
# ~~~~~~~~~~
def_open_ip_file()
def_open_command_file()

for hostname_ip in var_open_ui_ip_filename:
    def_login_to_device()


# ~~~~~~~~~~
# Successful executed python scripts
# ~~~~~~~~~~
'''
# FIRST TIME RUNNING SUCESSFUL
Ricardo-Mac:dev rdiaz$ python3 pexpect_test_ver_1.04.py
Enter IP filename: ip_file
Enter command filename: command_file
show run | in hostname
hostname usjol-c870-rtr-lab-01

show clock
14:54:29.806 UTC Sun Oct 14 2018

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
# ~~~~~~~~~~
# Glynmore code
# ~~~~~~~~~~

print pexpect.run('ls -l')
child = pexpect.spawn('ssh gsibal@198.18.19.114')
i=child.expect([ssh_newkey,'password:',pexpect.EOF,'$'])

print(i)
if i==0:
    print "I say yes"
    child.sendline('yes')
    i=child.expect([ssh_newkey,'password:',pexpect.EOF])
if i==1:
    print "I give password",
    child.sendline("mypassword")
    child.expect(pexpect.EOF)
if i==3:
        print(child.after)
elif i==2:
    print "I either got key or connection timeout"
    pass
print child.before # print out the result
child.logfile = sys.stdout
#print('testing')
#sys.stdout = open('log.txt','w')
#print(child.logfile)
#sys.stdout.close()

'''
