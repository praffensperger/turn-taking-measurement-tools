# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Turn-Taking Measurement Tools v0.91 
#
# createorload.py
#
# By Peter Raffensperger 16 November 2012
# 
# Reference:
# Raffensperger, P. A., Webb, R. Y., Bones, P. J., and McInnes, A. I. (2012). 
# A simple metric for turn-taking in emergent communication. 
# Adaptive Behavior, 20(2):104-116.
# 
# License:
# Turn-Taking Measurement Tools is licensed under a new BSD license. You are
# encouraged to use it in both free and commercial software. If you use this
# library in an academic context, we would appreciate it if you referenced our
# paper.
# 
# Copyright (C) 2012, Peter Raffensperger. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# - Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
# - Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
# - Neither the name of Peter Raffensperger nor the names of other contributors
# may be used to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

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
			SaveObjectToFile(sourceObject, sourceFilename)
	except IOError, OSError:
		mustCreate = True
		SaveObjectToFile(sourceObject, sourceFilename)
	
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
	