#!/usr/bin/env python

#TODO
# add text colors and decorations

# ##############################################################################
#
#	Prerequisites
#
# ##############################################################################

#

# ##############################################################################
#
#	All imports
#
# ##############################################################################

import spider
import sys
import os
import getpass
import sqlite3
from itertools import chain
from ConfigParser import SafeConfigParser

# ##############################################################################
#
#	Main class
#
# ##############################################################################

class weBLeech:
	def __init__(self):
		self.resourcelist_location = os.getcwd()
		self.resourcelist_filename = 'resourcelist.ini'

		self.db_location = os.getcwd()
		self.db_filename = 'resourceDB'

		self.resourcelist_dictionary = {}

		self.stdout_orig = sys.stdout

class userInput(weBLeech):
	def URLresource(self):
		print '''
Please provide a recource in the form of a FQDN (e.g http://www.google.com)

[!] make sure to enter a protocol prefix (i.e HTTP/HTTPS) [!]
'''
		resource = raw_input()
		print 'Is the spelling correct for: ' +resource+ ' (Y/n)'
		resourceYN = raw_input().lower

		while resourceYN() not in ['y', 'Y', 'n', 'N', '']:
			print '[!] Please choose only "y", "n" or leave blank for default'
			resourceYN = raw_input().lower
		if resourceYN() in ['y','Y', '']:
			pass
		elif resourceYN() == 'n':
			userInput.URLresource(self)
		else:
			print 'You broke me :/'
			quit()

		print ''
		print '[?] Does this resource requires login? (y/N)'
		requiresUP = raw_input().lower

		while requiresUP() not in ['y', 'Y', 'n', 'N', '']:
			print '[!] Please choose only "y", "n" or leave blank for default'
			requiresUP = raw_input().lower
		if requiresUP() in ['n', '']:
			print '[-] No credentials needed, moveing on..'
			username = 'None'
			password = 'None'
		else:
			print ''
			print '[-] Please type your username for the resource: '
			username = raw_input()
			print ''
			print 'Is the spelling correct for: ' +username+ ' (Y/n)'
			usernameYN = raw_input().lower

			while usernameYN() not in ['y', 'Y', 'n', 'N', '']:
				print '[!] Please choose only "y", "n" or leave blacnk for default'
				usernameYN = raw_input().lower
			while usernameYN() in ['n', 'N']:
				print '[-] Please retype the usernmae for the resource: '
				username = raw_input()
				print 'Is this correct for: ' +username+ ' (Y/n)'
				usernameYN = raw_input().lower
			if usernameYN() in ['y', 'Y', '']:
				print ''
				print '[-] Please type your password for the resource: '
				password = getpass.getpass()
				print '[-] Please retype your password for the resource:'
				passwordRT = getpass.getpass()

				while password != passwordRT:
					print ''
					print '[!] the passwords didn\'t match'
					print '[-] Please type your password for the resource: '
					password = getpass.getpass()
					print '[-] Please retype your password for the resource:'
					passwordRT = getpass.getpass()
				else:
					pass

		self.resourcelist_dictionary.update({"resource":resource,"username":username, "password":password})

		for i in str(resource_number):
			n = resource_number
			f = open(self.resourcelist_location+"/"+self.resourcelist_filename, 'a')
			sys.stdout = f
			print '[resource'+str(n)+']'
			n = n+1
			for i in self.resourcelist_dictionary.keys():
				print i +' = '+ self.resourcelist_dictionary[i]
			print ''
			sys.stdout = self.stdout_orig
			f.close()


	def Uresourcefile(self):
		print '[-] Please provide a full path for the resourcelist.ini file:'
		Uresourcelist_location = raw_input()
		global userFilePath
		userFilePath = Uresourcelist_location
		if os.path.isfile(Uresourcelist_location+"/"+self.resourcelist_filename) == True:
			userInteraction.resourcelist_read(self)
		else:
			userInteraction.resourcelist_find(self)


class manageDB(weBLeech, userInput):
	def findDB(self):
		if os.path.isfile(self.db_location+"/"+self.db_filename) == False:
			manageDB.createDB(self)
		elif os.path.isfile(self.db_location+"/"+self.db_filename) == True:
			pass
		else:
			print '''
[!] There was a problem finding / creating the DB file.
please scheck that the user running weBLeech has appropriate permissions and start over'''
			quit()

	def createDB(self):
		db = sqlite3.connect(self.db_location+self.db_filename)
		db.close()

	def writeToDB(self):
		if os.path.isfile(self.resourcelist_location+"/"+self.resourcelist_filename) == True:
			print ''
			print '[-] Checking if resource already exists in the DB.'
			conf = SafeConfigParser()
			conf.read(self.resourcelist_location+"/"+self.resourcelist_filename)
			for section_name in conf.sections():
				resource_URL = conf.get(section_name, 'resource')
				resource_user = conf.get(section_name, 'username')
				resource_pass = conf.get(section_name, 'password')
				db = sqlite3.connect('resourceDB')
				cursor = db.cursor()
				cursor.execute('SELECT * FROM sqlite_master WHERE type="table"')
				tables_list = cursor.fetchall()
				tables_exsist = resource_URL in chain.from_iterable(tables_list)

				if tables_exsist != True:
					if resource_user in ['None', ''] and resource_pass in ['None', '']:
						cursor.execute('CREATE TABLE IF NOT EXISTS \"'+resource_URL+'\" (url text, credentials text, username text, password text, filename text, filetype text, status text)')
						print '[-] Added recource '+resource_URL+'  from default resource list to DB.'
						cursor.execute('INSERT INTO \"'+resource_URL+'\" VALUES (\"'+resource_URL+'\", "False", \"'+resource_user+'\", \"'+resource_pass+'\", "filename", "filetype", "NDY" )')	#NODY = NotDownloadedYet
						print '[-] Added recource credentials from default resource list location to table.'
						db.commit()
					else:
						cursor.execute('CREATE TABLE IF NOT EXISTS \"'+resource_URL+'\" (url text, credentials text, username text, password text, filename text, filetype text, status text)')
						print '[-] Added recource '+resource_URL+'  from default resource list to DB.'
						cursor.execute('INSERT INTO \"'+resource_URL+'\" VALUES (\"'+resource_URL+'\", "True", \"'+resource_user+'\", \"'+resource_pass+'\", "filename", "filetype", "NDY" )')	#NODY = NotDownloadedYet
						print '[-] Added recource credentials from default resource list location to table.'
						db.commit()
				elif tables_exsist == True:
					print ''
					print '[!] Recource '+resource_URL+' already exsits in DB.'
					print '[-] Checking if any update is requiered.'
				db.close()


		elif os.path.isfile(userFilePath+"/"+self.resourcelist_filename) == True:
			print ''
			print '[-] Checking if resource already exists in the DB.'
			conf = SafeConfigParser()
			conf.read(self.resourcelist_location+"/"+self.resourcelist_filename)
			for section_name in conf.sections():
				resource_URL = conf.get(section_name, 'resource')
				resource_user = conf.get(section_name, 'username')
				resource_pass = conf.get(section_name, 'password')
				db = sqlite3.connect('resourceDB')
				cursor = db.cursor()
				cursor.execute('SELECT * FROM sqlite_master WHERE type="table"')
				tables_list = cursor.fetchall()
				tables_exsist = resource_URL in chain.from_iterable(tables_list)

				if tables_exsist != True:
					if resource_user in ['None', ''] and resource_pass in ['None', '']:
						cursor.execute('CREATE TABLE IF NOT EXISTS \"'+resource_URL+'\" (url text, credentials text, username text, password text, filename text, filetype text, status text)')
						print '[-] Added recource '+resource_URL+'  from user resource list to DB.'
						cursor.execute('INSERT INTO \"'+resource_URL+'\" VALUES (\"'+resource_URL+'\", "False", \"'+resource_user+'\", \"'+resource_pass+'\", "filename", "filetype", "NDY" )')	#NODY = NotDownloadedYet
						print '[-] Added recource credentials from user resource list to table.'
						db.commit()
					else:
						cursor.execute('CREATE TABLE IF NOT EXISTS \"'+resource_URL+'\" (url text, credentials text, username text, password text, filename text, filetype text, status text)')
						print '[-] Added recource '+resource_URL+' from user resource list to DB.'
						cursor.execute('INSERT INTO \"'+resource_URL+'\" VALUES (\"'+resource_URL+'\", "True", \"'+resource_user+'\", \"'+resource_pass+'\", "filename", "filetype", "NDY" )')	#NODY = NotDownloadedYet
						print '[-] Added recource credentials from user resource list to table.'
						db.commit()
				elif tables_exsist == True:
					print ''
					print '[!] Recource '+resource_URL+' already exsits in DB.'
				db.close()

	def readTablesFromDB(self):
		db = sqlite3.connect('resourceDB')
		db.row_factory = sqlite3.Row
		cursor = db.cursor()
		cursor.execute('SELECT name FROM sqlite_master WHERE type="table"')
		for table_row in cursor.fetchall():
			table = table_row[0]
			print '	[-] '+table
			print ''
		db.close()

	def readTablesDataFromDB(self):
		db = sqlite3.connect('resourceDB')
		db.row_factory = sqlite3.Row
		cursor = db.cursor()
		cursor.execute('SELECT name FROM sqlite_master WHERE type="table"')
		for table_row in cursor.fetchall():
			table = table_row[0]
			print '	[-] '+table
			print ''
			db_data = cursor.execute('SELECT url, credentials, username, password, filename, filetype, status FROM \"'+table+'\"')
			for row in db_data:
			   print 'URL 			= ', row[0]
			   print 'CREDENTIALS 		= ', row[1]
			   print 'USERNAME 		= ', row[2]
			   print 'PASSWORD 		= ', row[3]
			   print 'FILENAME 		= ', row[4]
			   print 'FILETYPE 		= ', row[5]
			   print 'STATUS 			= ', row[6]
			   print ''
		db.close()

	def readSingleTableData(self):
		db = sqlite3.connect('resourceDB')
		db.row_factory = sqlite3.Row
		cursor = db.cursor()
		cursor.execute('SELECT name FROM sqlite_master WHERE type="table"')
		chosen_table = cursor.fetchall()
		self.user_table_selection = raw_input().lower
		try:
			print ' [-] '+self.user_table_selection()
			print ''
			db_data = cursor.execute('SELECT url, credentials, username, password, filename, filetype, status FROM \"'+self.user_table_selection()+'\"')
			for row in db_data:
			   print 'URL 			= ', row[0]
			   print 'CREDENTIALS 		= ', row[1]
			   print 'USERNAME 		= ', row[2]
			   print 'PASSWORD 		= ', row[3]
			   print 'FILENAME 		= ', row[4]
			   print 'FILETYPE 		= ', row[5]
			   print 'STATUS 			= ', row[6]
			   print ''
		except:
			print '[!] Could not find the requested table'
			print ''
			db.close()
			userInteraction.wellcome_options(self)

	def editTableData(self):
		dataField = raw_input().lower

		while dataField() not in ['', 'no', 'none', 'ur', 'url', 'us', 'username', 'pa', 'password']:
			print '[!] Please choos only "none", "url", "username", "password" or leave blank for default'
			dataField = raw_input().lower
		if dataField() in ['ur', 'url']:
			print '[-] please type in the new URL value'
			new_url = raw_input().lower
			db = sqlite3.connect('resourceDB')
			cursor = db.cursor()
			cursor.execute('UPDATE \"'+self.user_table_selection()+'\" SET url=?',(new_url(),))
			db.commit()
			db.close()
		elif dataField() in ['us', 'username']:
			print '[-] Please type in the new USERNAME value'
			new_username = raw_input()
			db = sqlite3.connect('resourceDB')
			cursor = db.cursor()
			cursor.execute('UPDATE \"'+self.user_table_selection()+'\" SET username=?',(new_username,))
			db.commit()
			db.close()
		elif dataField() in ['pa', 'password']:
			print '[-] Please type in the new PASSWORD value'
			new_password = getpass.getpass()
			db = sqlite3.connect('resourceDB')
			cursor = db.cursor()
			cursor.execute('UPDATE \"'+self.user_table_selection()+'\" SET password=?',(new_password,))
			db.commit()
			db.close()
		elif dataField() in ['', 'no', 'none']:
			print 'you chose to no edit anything, mooving on..'
		else:
			print 'You broke me :/'
			quit()

	def deleteResourceFromDB(self):
		delete_table = raw_input().lower

		while delete_table() == '':
			print '[!] Table name can\'t be left blank'
			print ''
			print '[-] Please select which table you would like to delete'
			delete_table = raw_input().lower

		db = sqlite3.connect('resourceDB')
		cursor = db.cursor()
		cursor.execute('SELECT * FROM sqlite_master WHERE type="table"')
		tables_list = cursor.fetchall()
		tables_exsist = delete_table() in chain.from_iterable(tables_list)

		if tables_exsist == True:
			cursor.execute('DROP TABLE IF EXISTS \"'+delete_table()+'\"')
			db.commit()
			print '[!] Done, check status with DB full data view'
		elif tables_exsist != True:
			print '[!] Could not find the table in the DB'

		db.close()


class userInteraction(weBLeech, userInput, manageDB):
	def wellcome(self):
		print ''
		print ''
		print '~! Wellcome to weBLeech !~'.center(75)
		print '''
                               ___  _
                    _    _ __ |   | |    __  __  __ _
                    \    /|__||---  |   |__||__||   |__
                     \/\/ |__ |___| |__||__ |__ |__ |  |
'''
		print '''
This small crawler will be more then happy to priodically fatch your favorite file based resources.

weBLeech will save and remember your links and credentials encrypted in a DB
and reuse them when ever it's suposed to run and fetch your new reading materials.

Just follow the instructions to get started..
'''
		print '[?] Would you like to read the help file before we begin? (Y/n)'
		pHelp = raw_input().lower

		while pHelp() not in ['y', 'Y', 'n', 'N', '']:
			print '[!] Please choose only "y", "n" or leave blank for default'
			pHelp = raw_input().lower

		if pHelp() in ['y', 'Y', '']:
			userInteraction.helpFile(self)
		elif pHelp() == 'n':
			userInteraction.wellcome_options(self)
		else:
			print 'You broke me :/'
			quit()

	def wellcome_options(self):
		print '''
[?] What would you like to do?
	[1] Provide resources for leeching

	[2] Read available resources from DB

	[3] Update DB resources

	[4] Delete resources from DB

	[5] Unleesh the spiders on available resources

	[6] Quit
		'''

		base_option = raw_input().lower
		while base_option() not in ['1', '2', '3', '4', '5', '6']:
			print '[!] Please choone only from the available options 1-6'
			base_option = raw_input().lower
		if base_option() == '1':
			userInteraction.guide(self)
			manageDB.findDB(self)
			manageDB.writeToDB(self)
			# RESET MUST STAY LAST
			userInteraction.resourcelist_reset_Q(self)
			userInteraction.wellcome_options(self)
		elif base_option() == '2':
			print ''
			print '''
[?] Would you like to list all the resources in you\'re DB? (N/tb/fd)
Choose N - No, tb - Tables list, fd - Full data or leave black for default
'''
			listDB = raw_input().lower

			while listDB() not in ['n', 'N', '', 'tb', 'TB', 'fd', 'FD']:
				print '[!] Please choose only "n", "tb", "fd" or leave blank for default'
				listDB = raw_input().lower

			if listDB() in ['tb', 'TB']:
				manageDB.readTablesFromDB(self)
				userInteraction.wellcome_options(self)

			elif listDB() in ['fd', 'FD']:
				manageDB.readTablesDataFromDB(self)
				userInteraction.wellcome_options(self)

			elif listDB() in ['n', 'N', '']:
				userInteraction.wellcome_options(self)
			else:
				print 'You broke me :/'
				quit()
		elif base_option() == '3':
			print '[?] What resource would you like to update?'
			manageDB.readTablesFromDB(self)
			print '[-] Please type in the name of the table you would like to edit'
			print ''
			manageDB.readSingleTableData(self)
			print '[-] Please choose which value would you like to edit NONE, URL, USERNAME or PASSWORD (NO/ur/us/pa) or leave black for default'
			print ''
			manageDB.editTableData(self)
			userInteraction.wellcome_options(self)
		elif base_option() == '4':
			print '[!!] MAKE SURE TO TAKE COUSION WITH THIS OPTION, NO COMEING BACK FROM HERE [!!]'
			print ''
			print '[-] Please select which table you would like to delete'
			manageDB.deleteResourceFromDB(self)
			userInteraction.wellcome_options(self)
		elif base_option() == '5':
			#TODO uleesh spiders
			print 'uleesh spiders'
			userInteraction.wellcome_options(self)
		elif base_option() == '6':
			userInteraction.quit(self)


	def quit(self):
		print ''
		print '~!  ###############################################  !~'
		print 'you are blessd by the gooDLeech, keep information free.'
		print '~!  ###############################################  !~'
		print ''
		quit()

	def helpFile(self):
		print '~! weBLeech helpfile !~'.center(75)
		print '''
For weBLeech to work properly you'll need to supply some basic data:

[*] - resource 		-	Is the URL in an FQDN format from which you would like to download different files.
						keep in mind that weBLeech supports only HTTP/S resources and that you don't need to
						provide any protocol prefix, weBLeech will figure it out on its own.

[*] - number of 	-	If you wnat to provide multiple resources just let weBLeesch know how may are you
	  resources			going to provide

[*] - resourcelist 	-	If you prefere you can provide all the configuration needed in a condig file which is
						super self explenatory instead useing the guided run.
						just edit resourcelist.ini

						If you choose to use the resourcelist.ini file to supply weBLeech input, keep in mind that
						!!! after each tun the config file resets to it's default !!! in order to prevent credentials beeing
						saved in clear text.
'''

	def resourcelist_reset_Q(self):
		print ''
		print '''
######################################################################################
######################################################################################

weBLeech is about to reset the resourcelist.ini file to it\'s default content
so that it won\'t contain any clear text credentials.

if there is any reason why you would like to keep the resourcelist.ini file as is
please choose "n", otherwise the default behaviour will be to reset the file content

######################################################################################
######################################################################################
'''
		print '[?] Would you like to cancle the content rest? (y/N)'
		content_resetYN = raw_input().lower

		while content_resetYN() not in ['y', 'Y', 'n', 'N', '']:
			print '[!] Please choose only "y", "n" or leave blacnk for default'
			content_resetYN = raw_input().lower
		if content_resetYN() in ['n', 'N', '']:
			userInteraction.resourcelist_reset(self)
			print '[!] Reset seccuessful'
		else:
			print '[!] Reset aborted'

	def guide(self):
		print ''
		print '[?] Would you like to use the resourcelist.ini file instead of the guided run? (y/N)'
		resourcelistYN = raw_input().lower

		while resourcelistYN() not in ['y', 'Y', 'n', 'N', '']:
			print '[!] Please choose only "y", "n" or leave blacnk for default'
			resourcelistYN = raw_input().lower
		if resourcelistYN() in ['y', 'Y']:
			print ''
			print '[-] Looking for resourcelist.ini'
			userInteraction.resourcelist_find(self)
		else:
			print ''
			print '[-]Moveing forward with guided run.'

			userInteraction.resourcelist_clear(self)

			print ''
			print '[?] How many resources would you like to add?'
			global resource_number
			resource_number = raw_input()
			while not resource_number.isdigit():
				print '[!] Please only use numbers.'
				print '[?] How many resources would you like to add?'
				resource_number = raw_input()

			resource_number = int(resource_number)
			if resource_number in range (1,6):
				for resource_number in range(resource_number):
					userInput.URLresource(self)
			elif resource_number in range (6,11):
				print '[?] ' +str(resource_number)+ ' Is a large number, are you sure you\'re going to add ' +str(resource_number)+ ' resources? (y/N)'
				resourceNumYN = raw_input().lower
				while resourceNumYN() not in ['y', 'Y', 'n', 'N', '']:
					print '[!] Please choose only "y", "n" or leave blank for default'
					resourceNumYN = raw_input().lower
				if resourceNumYN() in ['y','Y']:
					for resource_number in range(resource_number):
						userInput.URLresource(self)
				elif resourceNumYN() in ['n', 'N', '']:
					userInteraction.guide(self)
			elif resource_number < 1:
				print ''
				print '[!] Since you\'re not adding any resources, manually or via the resourcelist.ini file i\'ll be quiting now'
				print ''
				pass
			else:
				print ''
				print '[!] For so manny resources please use the resourcelist.ini'
				print '[!] the default location should be: ' +self.resourcelist_location
				quit()

	def resourcelist_find(self):
		if os.path.isfile(self.resourcelist_location+"/"+self.resourcelist_filename) == False:
			print '[!] weBLeech could not find the resourcelist.ini file in it\'s default location'
			print ''
			print '[?] Would you like to provide the Full Path for the resourcelist.ini file'
			print 'or would you perffere going back to the Guided Run? (FP/gr)'
			fpgr = raw_input().lower

			while fpgr() not in ['fp', 'FP', 'gr', 'GR', '']:
				print '[!] Please choose only "fp" for Full Path or "gr" for Guided Run or leave blank for default (FP)'
				fpgr = raw_input().lower

			if fpgr() in ['fp', 'FP', '']:
				userInput.Uresourcefile(self)
			elif fpgr() in ['gr', 'GR']:
				userInteraction.guide(self)
		else:
			userInteraction.resourcelist_read(self)

	def resourcelist_read(self):
		if os.path.isfile(self.resourcelist_location+"/"+self.resourcelist_filename) == True:
			print ''
			print '[-] Found resourcelist.ini.'
		elif os.path.isfile(userFilePath+"/"+self.resourcelist_filename) == True:
			print ''
			print '[-] Found resourcelist.ini.'
		else:
			pass

	def resourcelist_reset(self):
		try:
			resourcelist = open(self.resourcelist_location+"/"+self.resourcelist_filename, 'w', 0)
			original_resourcelist = '''
[resource0]
resource = https://example1.com
username = username
password = password

[resource1]
resource = http://example2.com
username = None
password = None
'''
			resourcelist.write(original_resourcelist)
			resourcelist.close()
		except:
			resourcelist = open(userFilePath+"/"+self.resourcelist_filename, 'w', 0)
			original_resourcelist = '''
[resource0]
resource = https://example1.com
username = username
password = password

[resource1]
resource = http://example2.com
username = None
password = None
'''
			resourcelist.write(original_resourcelist)
			resourcelist.close()

	def resourcelist_clear(self):
		resourcelist = open(self.resourcelist_location+"/"+self.resourcelist_filename, 'w', 0)
		clear_content = ''
		resourcelist.write(clear_content)
		resourcelist.close()




if __name__ == '__main__':
	try:
		UI = userInteraction()
		wellcome = UI.wellcome()
	except KeyboardInterrupt:
		print ''
		print ''
		print '~!  ###############################################  !~'
		print 'you are blessd by the gooDLeech, keep information free.'
		print '~!  ###############################################  !~'
		print ''
		quit()
