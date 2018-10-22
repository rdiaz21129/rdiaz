#!/usr/local/bin/python3

# By: Ricardo Diaz
# Date: 20181013
# Python3
# Name: pexpect_test_ver_1.03.py
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
# Define regex
# ~~~~~~~~~~
re_hostname = (r"^hostname\s(.*)")

# ~~~~~~~~~~
# Define variables
# ~~~~~~~~~~
space01 = ('=' * 15 + '\n')
space02 = ('\n' + '=' * 15 + '\n')
#hostname = ('172.16.26.3')
username = ('rdiaz')
password = ('Password01$')
enable = ('your enable password')
hashtag = ('#')
test_hostname = ('hostname 181-chicago-core-01')

# ~~~~~~~~~~
# Define functions
# ~~~~~~~~~~
def def_test():
    print ('test function')
    print (var_hostname)
    print (var_hostname + '----->')
    print ('----->' + var_hostname)
    print ('test function')

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
    #child.expect('#')
    child.expect(hostname + hashtag)
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
    xyz = child.before
    xyz = xyz.decode('utf-8')
    #print (xyz)
    #if re.search(re_hostname, xyz):
    
    re_match_hostname = re.search(re_hostname, test_hostname)
    var_re_match_hostname_g0 = re_match_hostname.group(0)
    var_re_match_hostname_g1 = re_match_hostname.group(1)
    print (var_re_match_hostname_g0)
    print (var_re_match_hostname_g1)

    # Test below
    #h_name = child.before # prints the folloiwng ----> b'\r\nusjol-c870-rtr-lab-01'
    #print (h_name)
    #h1_name = h_name.decode('utf-8')
    #print (h1_name)

    ##hostname = h_name.lstrip() # Removes the \r\n
    #hostname = hostname.decode('utf-8') # Convert to string from bytes. Removes the "b"
    ##print (hostname + hashtag)
    #var_hostname = (hostname + hashtag)
    #print (var_hostname)
    # Test above

    #def_test()

    '''
    for show_command in var_open_ui_command_filename:
        def_send_show_command()
    '''

# ~~~~~~~~~~
# Start program here
# User input
# ~~~~~~~~~~
ui_ip_filename = input('Enter IP filename: ')
ui_command_filename = input('Enter command filename: ')
'''
Example below of file that is entered:
    Ricardo-Mac:dev rdiaz$ cat command_file
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

