# By: Ricardo Diaz
# Date: 20180106
# Python3.6
# Name: mac_address_converter.py

import re

# Functions
def windowsMacDef(userMacAdd):
    #print ("testing windows function")
    print ("\nNow converting [" + userMacAdd + "] Windows format")
    regexMAC = (re.findall(r'[0-9,A-Z,a-z].',userMacAdd))
    print ("Below is the printed regex output")
    print (regexMAC)

    #Converting Regex output (in an array/list) to a string
    str_regexMAC = "".join(regexMAC)
    #TESTprint (str_win_regexMAC)

    # Create variables for each individual groups (AA-BB-CC-DD-EE-FF)
    win_mac_pair_1 = (str_regexMAC[:2].upper())
    win_mac_pair_2 = (str_regexMAC[2:4].upper())
    win_mac_pair_3 = (str_regexMAC[4:6].upper())
    win_mac_pair_4 = (str_regexMAC[6:8].upper())
    win_mac_pair_5 = (str_regexMAC[8:10].upper())
    win_mac_pair_6 = (str_regexMAC[10:12].upper())

    # Putting it all together by connecting the mac address groups to output windows mac address
    print ("\n" + "===" * 4)
    print ("Below is the windows MAC address format")
    print (win_mac_pair_1 + "-" + win_mac_pair_2 + "-" + win_mac_pair_3 + "-" + win_mac_pair_4 + "-" + win_mac_pair_5 + "-" + win_mac_pair_6)
    print ("\n" + "===" * 4)

def linuxMacDef(userMacAdd):
    #TESTprint ("testing linux function")
    print ("\nNow converting [" + userMacAdd + "] to Linux format")
    regexMAC = (re.findall(r'[0-9,A-Z,a-z].',userMacAdd))
    print ("Below is the printed regex output")
    print (regexMAC)

    #Converting Regex output (in an array/list) to a string
    str_regexMAC = "".join(regexMAC)
    #TESTprint (str_win_regexMAC)

    # Create variables for each individual groups (AA-BB-CC-DD-EE-FF)
    linux_mac_pair_1 = (str_regexMAC[:2].lower())
    linux_mac_pair_2 = (str_regexMAC[2:4].lower())
    linux_mac_pair_3 = (str_regexMAC[4:6].lower())
    linux_mac_pair_4 = (str_regexMAC[6:8].lower())
    linux_mac_pair_5 = (str_regexMAC[8:10].lower())
    linux_mac_pair_6 = (str_regexMAC[10:12].lower())

    # Putting it all together by connecting the mac address groups to output Linux mac address
    print ("\n" + "===" * 4)
    print ("Below is the Linux MAC address format")
    print (linux_mac_pair_1 + ":" + linux_mac_pair_2 + ":" + linux_mac_pair_3 + ":" + linux_mac_pair_4 + ":" + linux_mac_pair_5 + ":" + linux_mac_pair_6)
    print ("\n" + "===" * 4)

def ciscoMacDef(userMacAdd):
    #TESTprint ("testing cisco function")
    print ("\nNow converting [" + userMacAdd + "] to Cisco format")
    regexMAC = (re.findall(r'[0-9,A-Z,a-z].',userMacAdd))
    print ("Below is the printed regex output")
    print (regexMAC)

    #Converting Regex output (in an array/list) to a string
    str_regexMAC = "".join(regexMAC)
    #TESTprint (str_win_regexMAC)

    # Create variables for each individual group (i.e mac add = 1234.5678.90ab | 1234 - group 1 | 5678 - group 2 |.. etc )
    mac_group_1 = (str_regexMAC[:4].lower())
    mac_group_2 = (str_regexMAC[4:8].lower())
    mac_group_3 = (str_regexMAC[8:12].lower())

    # Putting it all together by connecting the mac address groups with a "."
    print ("\n" + "===" * 4)
    print("Below is the Cisco MAC address format")
    print (mac_group_1 + "." + mac_group_2 + "." + mac_group_3)
    print ("===" * 4)

def userMacDef_lower(userMacAdd):
    #TESTprint ("user mac address lower case function")
    print ("\nNow converting [" + userMacAdd + "] to lowercase user format")
    regexMAC = (re.findall(r'[0-9,A-Z,a-z].',userMacAdd))
    print ("Below is the printed regex output")
    print (regexMAC)
    print ("\n" + "===" * 4)
    print("Below is the lowercase user format")

    #Converting Regex output (in an array/list) to a string
    str_regexMAC = "".join(regexMAC)
    print (str_regexMAC.lower())
    print ("===" * 4)

def userMacDef_UPPER(userMacAdd):
    #TESTprint ("user mac address UPPER case function")
    print ("\nNow converting [" + userMacAdd + "] to UPPERCASE user format")
    regexMAC = (re.findall(r'[0-9,A-Z,a-z].',userMacAdd))
    print ("Below is the printed regex output")
    print (regexMAC)
    print ("\n" + "===" * 4)
    print("Below is the UPPERCASE user format")

    #Converting Regex output (in an array/list) to a string
    str_regexMAC = "".join(regexMAC)
    print (str_regexMAC.upper())
    print ("===" * 4)

def user_decisionDef(userMacAdd):
    print ("\n" + "===" * 4)
    print ("You have selected Manual with mac [" + userMacAdd + "]")
    user_decision = input("Mac address output in uppercase? (y/n): ")
    if user_decision in ['n', 'N', 'no', 'No', 'NO']:
        userMacDef_lower(userMacAdd)
    elif user_decision in ['y', 'Y', 'Yes', 'yes', 'YES']:
        userMacDef_UPPER(userMacAdd)
    else:
        print ("INVALID INPUT")


# Explaining the purpose of the program
print ("\n# READ ME")
print ("Purpose of this program is to convert any mac address (regardless of format) and convert it to a specific vendor mac address format")

# Examples/list of mac address formats
print ("\n# MAC address format examples per vendor\nw. D8-FC-93-7B-67-7C - Windows\nl. 8c:85:90:1a:87:c5 - Linux\nc. d8fc.937b.677c - Cisco\nu. D8FC937B677C or d8fc937b677c - Manual User\n")

# User input | ask user for desired mac address output
userLetterSelection = input("From the above list, please select the desired MAC address output: ")
print ("[" + userLetterSelection + "] is what you have selected")

# User input | user to enter mac address in any format
userMacAdd = input ("\nEnter MAC address(regardless of format): ")
#TESTprint (userMacAdd)


# If statements
if userLetterSelection in ['w', 'W']:
    print ("\n" + "===" * 4)
    print ("\n" + "You have selected Windows")
    windowsMacDef(userMacAdd)
elif userLetterSelection in ['l', 'L']:
    print ("\n" + "===" * 4)
    print ("You have selected Linux")
    linuxMacDef(userMacAdd)
elif userLetterSelection in ['c', 'C']:
    print ("\n" + "===" * 4)
    print ("You have selected Cisco")
    ciscoMacDef(userMacAdd)
elif userLetterSelection in ['u', 'U']:
    user_decisionDef(userMacAdd)
    #userMacDef(userMacAdd)
else:
    print ("INVALID SELECTION")
