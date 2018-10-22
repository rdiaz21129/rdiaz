#!/usr/local/bin/python3

# By: Ricardo Diaz
# Date: 20181010
# Python3
# Name: pexpect_test_ver_1.00.py
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
ssh_newkey = 'Are you sure you want to continue connecting'
test01 = ('=' * 10)
router = ('172.16.26.3')
username = ('rdiaz')
passwd = ('Password01$')

# ~~~~~~~~~~
# Test area
# ~~~~~~~~~~

child = pexpect.spawn('ssh %s@%s' % (username, router)) # ssh to router
child.expect('Password:') # expect the following prompt [Password:]
child.sendline(passwd) # send password (variable)
child.expect('#')
child.sendline('\n')

print ('I AM LOGGED IN')

child.sendline('show ip int br\n')
print ('Send line [show ip int br]')

print (child.read())
child.expect('#')

h = child.before # prints the folloiwng ---->  b'\r\nusjol-c870-rtr-lab-01'
hostname = h.lstrip() # Removes the \r\n
hostname = hostname.decode("utf-8") # Convert to string from bytes. Removes the "b"
#print ("Connected to " + hostname)

print (hostname)

child.logfile = sys.stdout
print (child.logfile) # prints <_io.TextIOWrapper name='<stdout>' mode='w' encoding='UTF-8'>



'''
===============
child = pexpect.spawn('ssh %s@%s' % (username, router)) # ssh to router
child.expect('Password:') # expect the following prompt [Password:]
child.sendline(passwd) # send password (variable)
child.expect('#')
child.sendline('\n')

print ('I AM LOGGED IN')

child.sendline('show ip int br\n')
print ('Send line [show ip int br]')

print (child.read())
child.expect('#')

h = child.before # prints the folloiwng ---->  b'\r\nusjol-c870-rtr-lab-01'
hostname = h.lstrip() # Removes the \r\n
hostname = hostname.decode("utf-8") # Convert to string from bytes. Removes the "b"
#print ("Connected to " + hostname)

print (hostname)

child.logfile = sys.stdout
print (child.logfile) # prints <_io.TextIOWrapper name='<stdout>' mode='w' encoding='UTF-8'>




rdiaz@Ricardo-Mint ~/Documents/bitbucket/netchil33t/rdiaz/dev $ python3 pexpect_test_ver_1.00.py
I AM LOGGED IN
Send line [show ip int br]
Traceback (most recent call last):
  File "/usr/lib/python3/dist-packages/pexpect/expect.py", line 97, in expect_loop
    incoming = spawn.read_nonblocking(spawn.maxread, timeout)
  File "/usr/lib/python3/dist-packages/pexpect/pty_spawn.py", line 452, in read_nonblocking
    raise TIMEOUT('Timeout exceeded.')
pexpect.exceptions.TIMEOUT: Timeout exceeded.

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "pexpect_test_ver_1.00.py", line 47, in <module>
    print (child.read())
  File "/usr/lib/python3/dist-packages/pexpect/spawnbase.py", line 407, in read
    self.expect(self.delimiter)
  File "/usr/lib/python3/dist-packages/pexpect/spawnbase.py", line 315, in expect
    timeout, searchwindowsize, async)
  File "/usr/lib/python3/dist-packages/pexpect/spawnbase.py", line 339, in expect_list
    return exp.expect_loop(timeout)
  File "/usr/lib/python3/dist-packages/pexpect/expect.py", line 104, in expect_loop
    return self.timeout(e)
  File "/usr/lib/python3/dist-packages/pexpect/expect.py", line 68, in timeout
    raise TIMEOUT(msg)
pexpect.exceptions.TIMEOUT: Timeout exceeded.
<pexpect.pty_spawn.spawn object at 0x7fd7a0cdb470>
command: /usr/bin/ssh
args: ['/usr/bin/ssh', 'rdiaz@172.16.26.3']
searcher: None
buffer (last 100 chars): b'igned      YES NVRAM  up                    down    \r\nusjol-c870-rtr-lab-01#\r\nusjol-c870-rtr-lab-01#'
before (last 100 chars): b'igned      YES NVRAM  up                    down    \r\nusjol-c870-rtr-lab-01#\r\nusjol-c870-rtr-lab-01#'
after: <class 'pexpect.exceptions.TIMEOUT'>
match: None
match_index: None
exitstatus: None
flag_eof: False
pid: 9031
child_fd: 5
closed: False
timeout: 30
delimiter: <class 'pexpect.exceptions.EOF'>
logfile: None
logfile_read: None
logfile_send: None
maxread: 2000
ignorecase: False
searchwindowsize: None
delaybeforesend: 0.05
delayafterclose: 0.1
delayafterterminate: 0.1
===============

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
