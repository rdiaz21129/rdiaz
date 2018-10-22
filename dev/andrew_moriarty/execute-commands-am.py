import paramiko
import datetime
import time
import string
import csv
import socket
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('devices', help='Required: CSV file list of devices. Format: device_IP,username,password')
parser.add_argument('commands',help="Required: commands to be executed")
args = parser.parse_args()
# print (args.devices)
# print (args.commands)


#   Send a list of commands from the text file commands.txt
# 	to each router in routers.txt
#	format of router.txt is ip_address,username,password
#	command.txt is as per cisco syntax.

class SSH_Cisco():

	def __init__ (self):
		pass

	def SendCommand(self,host,username,password,command):

		try:
			remote_conn_pre = paramiko.SSHClient()
			remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			remote_conn_pre.connect(host, username=username, password=password, look_for_keys=False, allow_agent=False)
			print("SSH connection established to " + host)
			output = ("====SSH connection established to " + host + '\n')
			remote_conn = remote_conn_pre.invoke_shell()
			remote_conn.send('terminal len 0')
			remote_conn.send("\n")
			remote_conn.send(command)
			remote_conn.send("\n")
			time.sleep(5)
			output += str(remote_conn.recv(50000))


		except paramiko.AuthenticationException:
			print (host + '=== Bad credentials')
			output = ('\n'+ '===== Bad credentials'+ host +  '\n')

		except paramiko.SSHException:
			print (host + '=== Issues with ssh service')
			output = ('\n'+ '==== Issues with ssh service'+  host + '\n')

		except socket.error:
			print(host + '=== Device unreachable')
			output = ('\n'+ '==== Device unreachable'+ host + '\n')

		return (output)


outputs = ''
r_commands = ''

with open(args.devices, 'r') as f_devices:
  device_username_pw = csv.reader(f_devices)
  devices = list(device_username_pw)

with open(args.commands,'r')as f_commands:
	for line in f_commands.readlines():
		r_commands += str(line)

try:
	for ip,user,password in devices:
		conn1 = SSH_Cisco()
		outputs += conn1.SendCommand(ip,user,password,r_commands)

except:
	pass

f_devices.close()
f_commands.close()
print ('done')


# for line in outputs.split("\\r\\n"):  # Note the 'double \\ to escape to a literal'
	# print(line)

with open('output.txt', 'w') as f_output:

	for line in outputs.split("\\r\\n"):  # Note the 'double \\ to escape to a literal'
		# print(line)
		f_output.write(line)
		f_output.write('\n')

	f_output.close()
