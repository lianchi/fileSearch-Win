#-*- coding:utf-8 -*-

import os
import re
import sys
import time
import shutil
from time import clock

reload(sys)
sys.setdefaultencoding('utf-8')

#return the files and directories in the source path
def allFileList(path):
	filelist = []
	direlist = []
	try:
		all_file = os.listdir(path)
	except WindowsError:
		pass
	for items in all_file:
		if os.path.isfile(path + items):
			filelist.append(path + items)
		else:
			direlist.append(path + items + '/')
	return filelist, direlist

#find the file within keyword, then copy them to the destpath
def search(f, keyword, sourcepath, destpath):
	filelist, direlist = allFileList(sourcepath)
	for files in filelist:
		filename = files.split('/')[-1]
		#if filename.find(keyword) > -1:
		if re.search(keyword, filename):
			f.writelines(files + '\n')
			shutil.copy2(files, destpath)
	for direc in direlist:
		#if direc.find(keyword) > -1:
		if re.search(keyword, direc):
			f.writelines(direc + '\n')
			try:
				shutil.copytree(direc, destpath + direc.split('/')[-2])
			except:
				pass
		else:
			search(f, keyword, direc, destpath)

def main():
	sourcePath = 'C:/Users/Administrator/'
	destPath = ''
	timestamp = time.strftime('%Y-%m-%d', time.localtime(time.time()))
	subDestPath = 'CopyFile/fileBYname/' + timestamp + '/'
	keyWord = re.compile(u'(classified)|(confidential)')
	usbDrive = ['D:/', 'E:/', 'F:/', 'G:/', 'H:/', 'I:/', 'J:/', 'K:/', 'L:/', 'M:/', 'N:/', 'O:/'
				, 'P:/', 'Q:/', 'R:/', 'S:/', 'T:/', 'U:/', 'V:/', 'W:/', 'X:/', 'Y:/', 'Z:/']

	if not os.path.exists(subDestPath):
		os.makedirs(subDestPath)
	for drive in usbDrive:
		if os.path.exists(drive + subDestPath):
			destPath = drive + subDestPath
			print "The USB drive is %s" % drive
			print "Please wait......\n"
			break
	if destPath == '':
		print 'No USB drive found!\n'
		return 0

	start = clock()
	logFile = 'CopyFile/fileBYname/' + timestamp +'.txt'
	f = open(logFile, 'w+')
	status = search(f, keyWord, sourcePath, destPath)
	if False == status:
		print 'Sorry, no result found.'
	else:
		print 'The search and copy is done.'
	end = clock()
	costTime = end - start
	print 'Cost time: %f seconds.' % costTime
	f.seek(0)
	filesTotalNum = len(f.readlines())
	filesRealNum = len(os.listdir(destPath))
	msg = ['\nThe number of total files and directories: ', str(filesTotalNum),
		   '.\nThe number of real copied files and directories: ', str(filesRealNum), 
		   '.\nCost time: ', str(costTime), ' seconds.']
	f.writelines(msg)
	f.close()

if __name__ == '__main__':
	main()
