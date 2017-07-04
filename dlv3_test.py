import os
import logging
import logging.handlers
import driveLibraryV3
import socket

log_folderId =  "0BwEMWPU5Jp9SN0cyM0N6ZWN1Wk0"		#// log directory
exec_folderId = "0BwEMWPU5Jp9SNExlMFdXdkdEZUE"		#// remote execution log directory
cam_folderId  = "0BwEMWPU5Jp9SZDNEOEdaeWJrQjA"		#// captured image file directory
tn_folderId   = "0BwEMWPU5Jp9SVkp5V3Q5bjhxVkE"		#// captured image thumbnail file directory


#logging.basicConfig(format='%(asctime)s %(levelname)s %(funcName)s %(message)s', filename='/tmp/python.log',level=logging.DEBUG)

# setup root logger
logger = logging.getLogger("")
logger.setLevel(logging.DEBUG)

h1 = logging.StreamHandler()
h1.setLevel(logging.DEBUG)
h1.setFormatter(logging.Formatter('%(asctime)s : %(levelname)s [ %(funcName)s ] %(message)s'))
logger.addHandler(h1)

h2 = logging.handlers.SysLogHandler()
h2.setLevel(logging.DEBUG)
h2.setFormatter(logging.Formatter('%(levelname)s [ %(funcName)s ] %(message)s'))
logger.addHandler(h2)

# setup module logger
logger = logging.getLogger(__name__)

gd = driveLibraryV3.driveLibrary(logger)

logger.warn("test---test")

service = gd.GD_createService()

files = gd.GD_searchFiles(service, "up", log_folderId)

if not files:
	print('No file found.')
else:
	for item in files:
		print('id: {0} name: {1}'.format(item['id'], item['name']))

localFile = os.path.expanduser('~/projects/driveLibrary/driveLibraryV3.py')
print localFile

gd.GD_uploadFile(service, 'testfile', log_folderId, 'It is a test.', 'text/plain', localFile)

content = gd.GD_downloadFile(service, 'testfile', log_folderId)

targetFile = os.path.expanduser('~/projects/driveLibrary/test/test_result.txt')
fhandle = open(targetFile, 'w')
fhandle.write(content)
fhandle.close()

gd.GD_renameFile(service, log_folderId, "testfile", "testFile_2")


