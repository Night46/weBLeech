#!/usr/bin/env python

# ##############################################################################
#
#	All imports
#
# ##############################################################################

import requests
import sqlite3

# ##############################################################################
#
#	Main class
#
# ##############################################################################

class spiderMain:
	def __init__(self):
		pass

class webMgmt(spiderMain):
	def webConnect(self):
		db_resources = dataAndFiles.dbRead(self)
		list_length = len(db_resources)
		n = 0
		while n < list_length:
			resource = db_resources[n]
			current_user = db_resources[n+1]
			current_pass = db_resources[n+2]
			n = n + 3
			if current_user and current_pass in ['None', '']:
				r_get = requests.get(resource)
				r_get.status_code

			elif current_user and current_pass not in ['None', '']:
				r_get = requests.get(resource, auth=(current_user, current_pass))
				r_get.status_code


	def webCrawl(self):
		pass


	def webDownload(self):
		pass


class dataAndFiles(spiderMain):
	def dbRead(self):
		db = sqlite3.connect('resourceDB')
		db.row_factory = sqlite3.Row
		cursor = db.cursor()
		cursor.execute('SELECT name FROM sqlite_master WHERE type="table"')
		finale_resource = []
		for table_row in cursor.fetchall():
			table = table_row[0]
			db_data = cursor.execute('SELECT url, credentials, username, password, filename, filetype, status FROM \"'+table+'\"')
			for row in db_data:
				tmpDict = {'URL':row[0], 'CREDENTIALS':row[1], 'USERNAME':row[2], 'PASSWORD':row[3], 'FILENAME':row[4], 'FILETYPE':[5], 'STATUS':row[6]}
				if tmpDict['CREDENTIALS'] == 'False':
					current_resource = tmpDict['URL']
					current_user = 'None'
					current_pass = 'None'
					# print ''
					# print current_resource
					resource = [current_resource, current_user, current_pass]
					finale_resource.extend(resource)
				elif tmpDict['CREDENTIALS'] == 'True':
					current_resource = tmpDict['URL']
					current_user = tmpDict['USERNAME']
					current_pass = tmpDict['PASSWORD']
					# print ''
					# print current_resource, current_user, current_pass
					resource = [current_resource, current_user, current_pass]
					finale_resource.extend(resource)
		db.close()
		return finale_resource


	def dbWrit(self):
		pass

	def dbUpdate(self):
		# dataAndFiles.dbRead(self)
		# db = sqlite3.connect('resourceDB')
		# cursor = db.cursor()
		# cursor.execute('UPDATE \"'+tmpDict['URL']+'\" SET STATUS=YDY',)
		# db.commit()
		# db.close()
		pass

	def folderCheck(self):
		pass

class spiderRun(spiderMain, dataAndFiles, webMgmt):
	def readFromDB(self):
		pass

	def chooseAction(self):
		pass

	def execute(self):
		webMgmt.webConnect(self)


if __name__ == '__main__':
	try:
		spider = spiderRun()
		run = spider.execute()
	except KeyboardInterrupt:
		print ''
		print ''
		print '~!  ###############################################  !~'
		print 'you are blessd by the gooDLeech, keep information free.'
		print '~!  ###############################################  !~'
		print ''
		quit()
