#!/usr/bin/python

# ~ Script has been configured to read auth.log from /var/log.
# ~ Use either 'python LA.py' or './LA.py' without quotes to run the script.

import re

# ~ Function to ask for user input. If the input is invalid, loop the function by calling it again.
def oinput():
	
	print('Options: ')
	print('1. Print command usage only.')
	print('2. Print parsed log.')
	userin = input('Please choose an option (1 or 2): ')
	print()
	
	if userin != '1' and userin != '2':
		
		print('Invalid input! Please provide a valid input! (1 or 2)')
		print()
		userin = oinput()
		
	return userin

# ~ Function tstampformat is used to verify the format of the time stamp in auth.log.
# ~ Currently the function is only able to detect the complete time stamp if it has the time in 
# ~ the format XX:XX:XX in its last field.
def tstampformat():
	
	index = 0
	
	for chk in word:
		
		if re.search("([0-9]{2}:){2}[0-9]{2}", chk):
			
			return index
			break
			
		else:
			
			index += 1

# ~ Using the information from tstampformat, this function then adds the time stamp to a string and returns it.
def printtstamp():
	
	tstamp = ''
	
	for tcount in range(tformat + 1):
		
		tstamp += word[tcount] + ' '
	
	tstamp = tstamp.strip()
	
	return tstamp
	
# ~ This function is used add the commands used to a string and return it to the main script.
def usedcom():
	
	command = ''
	
	for cword in word:
		
		if 'COMMAND' in cword or 'COMMAND' in command:
			
			command += cword + ' '
			
	command = command.strip()
		
	return command
	
# ~ Get user input
uinput = int(oinput())

# ~ Opening auth.log from /var/log and reading it into a list variable.
with open('/var/log/auth.log', 'r') as file:
	
	data = file.readlines()
	
# ~ Main part of the script that prints out the required logs.
for line in data:
	
	cleanline = line.strip()
	word = cleanline.split()			
	tformat = tstampformat()
	
	# ~ Print sudo usage.
	if 'sudo' in word[tformat + 2] and 'TTY' in word[tformat + 5]:
		
		print(printtstamp(), 'User', '\'' + word[tformat + 3] + '\'', 'used sudo on command:', usedcom())
		
	# ~ Print failed sudo attempts.
	elif 'sudo' in word[tformat + 2] and 'NOT' in word[tformat + 6]:
		
		print(printtstamp(),'ALERT! User', '\'' + word[tformat + 3] + '\'', 'failed to use sudo! The attempted command was:', usedcom())
	
	# ~ Print parsed log.
	if uinput == 2:
	
		# ~ Print added users.
		if 'useradd' in word[tformat + 2]:
			
			userdata = word[tformat + 5].split('=')
			username = userdata[1].split(',')
			print(printtstamp(), 'New user', '\'' + username[0] + '\'', 'has been added.')
			
		# ~ Print deleted users.
		elif 'userdel' in word[tformat + 2] and 'delete' in word[tformat + 3]:
			
			print(printtstamp(), 'User', word[tformat + 5], 'was deleted.')
			
		# ~ Print password changes.
		elif 'passwd' in word[tformat + 2] and 'changed' in word[tformat + 5]:
			
			print(printtstamp(), 'Password was changed for user', '\'' + word[-1] + '\'.')
			
		# ~ Print su usage.
		elif 'su:' in word[tformat + 2] and 'su:session' in word[tformat + 3]:
			
			user1 = word[-1].split('(')
			user2 = word[-3].split('(')
			
			print(printtstamp(), 'User', '\'' + user1[0] + '\'', 'used su to switch to user', '\'' + user2[0] + '\'.')
			
		# ~ Print failed su attempts.
		elif 'su:' in word[tformat + 2] and 'FAILED' in word[tformat + 3]:
			
			user1 = word[tformat + 6].split(')')
			print(printtstamp(), 'User', '\'' + word[-3] + '\'', 'failed su to user', '\'' + user1[0] + '\'.')
			
