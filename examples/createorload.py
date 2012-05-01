import cPickle as pickle
import os
import time
import re

def SaveObjectToFile(object, filename):
	f = open(filename, 'w')
	pickle.dump(object, f, pickle.HIGHEST_PROTOCOL) #Could also use gzip
	f.close()	

def GetObjectFromFile(filename):
	f = open(filename, 'r')
	obj = pickle.load(f)
	f.close()
	return obj 

def GetDestinationFilename(sourceFilename, creationRoutine, id=None):
	if id is None:
		id = re.match('<function (.*?) at 0x.*', str(creationRoutine)).groups()[0]
	destinationFilename = sourceFilename + str(id) + '.pickle'	
	return destinationFilename

def CreateOrLoadByObject(sourceObject, creationRoutine, id, forceCreation=False):
	mustCreate = forceCreation
	sourceFilename = id + '.pickle'
	destinationFilename = GetDestinationFilename(sourceFilename, creationRoutine)
	try:
		sourceObjectDiskCopy = GetObjectFromFile(sourceFilename)
		if sourceObjectDiskCopy != sourceObject:
			mustCreate = True
	except IOError, OSError:
		mustCreate = True
	
	if not mustCreate:
		try:
			destination = GetObjectFromFile(destinationFilename)
			return destination
		except IOError, OSErorr:
			mustCreate = True

	assert(mustCreate)
	destination = creationRoutine(sourceObject)
	SaveObjectToFile(destination, destinationFilename)
	return destination
	

def CreateOrLoad(sourceFilename, creationRoutine, kwargs={}, id=None, verbose=False, forceCreation=False, returnDestinationFilename=False):
	destinationFilename = GetDestinationFilename(sourceFilename, creationRoutine, id)
	try:
		destinationModifiedTime = os.stat(destinationFilename).st_mtime
	except OSError:
		destinationModifiedTime = 0
		
	sourceModifiedTime = os.stat(sourceFilename).st_mtime

	if verbose:
		print 'Source filename', sourceFilename, ' Destination filename', destinationFilename
		print 'Source modified at', time.ctime(sourceModifiedTime), ' Destination modified at', time.ctime(destinationModifiedTime)
	if (sourceModifiedTime >= destinationModifiedTime) or forceCreation:
		destination = creationRoutine(sourceFilename, **kwargs)
		SaveObjectToFile(destination, destinationFilename)
		if verbose:	print "created file"
	else:
		destination = GetObjectFromFile(destinationFilename)
		if verbose:	print "loaded file"
	
	if returnDestinationFilename:
		return destination, destinationFilename
	return destination
	
if __name__ == '__main__':
	def Create(sourceFilename):
		return 'This is ' + sourceFilename
		
	myString = CreateOrLoad('test.txt', Create, verbose=True)
	print myString
	