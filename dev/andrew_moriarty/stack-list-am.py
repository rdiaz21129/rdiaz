import csv
import re
import os

#   Print a list of stacked switches, their model number, serial number, and mac-address


devices =[]
device_type = []
os.chdir('H:\duracel\switches')
files = (os.listdir())
with open('output_stacks.txt', 'w') as f_output_config:
	f_output_config.close()

f_output=''


for file in files:
	mac_address = []
	switch_model = []
	switch_sn = []
	with open(file, 'r') as f_device:
		for line in f_device.readlines():
			if 'Master' in line or 'Member' in line or 'Active' in line or 'Standby' in line:
				# Match -  2       Member ecc8.8224.b980     10     0       Ready
				# Don't match -  5       Member 0000.0000.0000     0      0       Provisioned
				if 'Provisioned' not in line:
					s_mac=re.search('[a-fA-F0-9]{4}.[a-fA-F0-9]{4}.[a-fA-F0-9]{4}',line)
				if s_mac:
					mac_address.append(s_mac.group(0))
					s_mac=''
			if 'PID' in line:
				# Match - PID: WS-C3750V2-48PS-S , VID: V05, SN: FDO1441X2GC
				# Match - PID: WS-C3850-24P      , VID: V07  , SN: FCW2010D19W
				s_model=re.search('WS[-][\w\-]+',line)
				if s_model:
					s_sn=re.search('[\w]{3}[\d]{4}[\w]{4}',line)
					switch_model.append(s_model.group(0))
					switch_sn.append(s_sn.group(0))

		try:
			if mac_address:
				h_name = file.replace('output-1672697-','')
				h_name = h_name.replace('.txt','')
				with open('output_stacks.txt', 'a') as f_output_config:
					f_output_config.write('\n')
					f_output_config.write(h_name)
					f_output_config.write('\n')
					loop = 0
					for line in mac_address:
						if mac_address[loop] and switch_model[loop]:
							out_line = (switch_model[loop] + '\t' + switch_sn[loop] + '\t' + mac_address[loop])
							f_output_config.write(out_line)
							f_output_config.write('\n')
						loop+=1
				f_output_config.close()

		except:
			print ('=======Issues with ', file, ' Check output')

	f_device.close()
