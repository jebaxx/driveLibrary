#
# Google Drive Connector Service
#

import os
import io
import logging
import httplib2
import apiclient
import oauth2client

from oauth2client import client
from oauth2client import tools

from apiclient.http import MediaIoBaseDownload
#from googleapiclient.discovery_cache import file_cache
####	'file_cache' module cannot work with current version of oauth2 library

import argparse
flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()

CLIENT_SECRET_FILE = '/home/pi/projects/google_credentials_py/client_secret.json'

APPLICATION_NAME = 'webMonitor2'

SCOPES = 'https://www.googleapis.com/auth/drive'

class driveLibrary:

	def __init__(self, logger):
	    self.log_a = logger

	#
	# retrieve stored credential or authenticate if needed
	#
	@staticmethod
	def GD_getCredentials():

	    home_dir = os.path.expanduser('~')
	    credential_dir = os.path.join(home_dir, 'projects/google_credentials_py')

	    if not os.path.exists(credential_dir):
	        os.makedirs(credential_dir)

	    credential_path = os.path.join(credential_dir, 'google_drive-credential.json')

	    store = oauth2client.file.Storage(credential_path)
	    credentials = store.get()

	    if not credentials or credentials.invalid:
	        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
	        flow.user_agent = APPLICATION_NAME
	        credentials = tools.run_flow(flow, store, flags)

	    return credentials


	#
	# Create GoogleDrive Service instance
	#
	def GD_createService(self):

	    logger = self.log_a.getChild(__name__)

	    credentials = driveLibrary.GD_getCredentials()

#	    cache = file_cache()

	    service = apiclient.discovery.build('drive', 'v3', http=credentials.authorize(httplib2.Http()))

	    return service

	#
	# Acquire specified files from Google Drive 
	#
	def GD_acquireFiles(self, service, targetName, parentFolderId):

	    logger = self.log_a.getChild(__name__)

	    condition = "(trashed != true) and (name = '" + targetName + "') and ('" + parentFolderId + "' in parents)"

	    results = service.files().list(pageSize=10, q=condition, fields="files(id, name)").execute()

	    return results.get('files', [])

	#
	# Search file from Google Drive Storage matches the specified condition
	#
	def GD_searchFiles(self, service, targetName, parentFolderId):

	    logger = self.log_a.getChild(__name__)

	    condition = "(trashed != true) and (name contains '" + targetName + "') and ('" + parentFolderId + "' in parents)"

	    results = service.files().list(pageSize=10, q=condition, fields="files(id, name)").execute()

	    return results.get('files', [])


	#
	# download a file from Google Drive Storage
	#
	def GD_downloadFile(self, service, targetName, parentFolderId):

	    logger = self.log_a.getChild(__name__)

	    fileItems = self.GD_acquireFiles(service, targetName, parentFolderId)

	    if not fileItems:
		logger.info("Specified file is not exist.")
		return null

	    req = service.files().get_media(fileId=fileItems[0]['id'])
	    h = io.BytesIO()
	    downloader = MediaIoBaseDownload(h, req)

	    done = False
	    while done is False:
		status, done = downloader.next_chunk()

	    return h.getvalue()

	#
	# upload a file to Google Drive Storage as a New File
	# 
	def GD_uploadNewFile(self, service, targetName, parentFolderId, description, mimeType, localFile):

	    logger = self.log_a.getChild(__name__)

	    if ( not os.path.exists(localFile) ):
		logger.error("Specified file not exist.")
		return

	    if ( os.path.getsize(localFile) == 0 ):
		logger.error("Specified file size is Zero.")
		return

	    body = {
		'name': targetName,
		'mimeType': mimeType,
		'parents': [parentFolderId],
		'description': description,
	    }

	    media = apiclient.http.MediaFileUpload(localFile, mimeType)

	    service.files().create(body=body, media_body=media).execute()


	#
	# upload a file to Google Drive Storage
	# 
	def GD_uploadFile(self, service, targetName, parentFolderId, description, mimeType, localFile):

	    logger = self.log_a.getChild(__name__)

	    if ( not os.path.exists(localFile) ):
		logger.error("Specified file not exist.")
		return

	    fileItems = self.GD_acquireFiles(service, targetName, parentFolderId)

	    if (not fileItems):
		return self.GD_uploadNewFile(service, targetName, parentFolderId, description, mimeType, localFile)

	    body = {
		'name': targetName,
		'mimeType': mimeType,
		'description': description,
	    }

	    media = apiclient.http.MediaFileUpload(localFile, mimeType)

	    service.files().update(fileId=fileItems[0]['id'], body=body, media_body=media).execute()


	#
	# rename the Google Drive file
	# 
	def GD_renameFile(self, service, parentFolderId, oldName, newName):

	    logger = self.log_a.getChild(__name__)

	    fileItems = self.GD_acquireFiles(service, oldName, parentFolderId)

	    if (not fileItems):
		logger.error("Specified file not exist.")
		return

	    body = { 'name': newName }

	    service.files().update(fileId=fileItems[0]['id'], body=body).execute()

