#!/usr/local/bin/python3

# By: Ricardo Diaz
# Date: 20181013
# Python3
# Name: pexpect_test_ver_1.02.py
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


# ~~~~~~~~~~
# Define variables
# ~~~~~~~~~~
space01 = ('=' * 15 + '\n')
space02 = ('\n' + '=' * 15 + '\n')

hostname = ('172.16.26.3')
username = ('rdiaz')
password = ('Password01$')
enable = ('your enable password')

# ~~~~~~~~~~
# Define functions
# ~~~~~~~~~~
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
    child.sendline(show_command)
    child.expect('#')
    output =  child.before
    output = output.decode("utf-8")
    print (output)

# Function to login into device (ssh)
def def_login_to_device():
    global child
    global show_command
    ssh = 'ssh ' + (username) + '@' +(hostname)
    child = pexpect.spawn(ssh) #'ssh ' + (username) + '@' +(hostname)
    child.expect('word')
    child.sendline(password)
    print (space01 + 'Logged into device ' + hostname + space02)
    child.expect('#')

    #def_send_command()
    for show_command in var_open_ui_command_filename:
        def_send_show_command()


# ~~~~~~~~~~
# Start program here
# User input
# ~~~~~~~~~~
#ui_filename = input('Enter filename: ')
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
def_open_command_file()
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
