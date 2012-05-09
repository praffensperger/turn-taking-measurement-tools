#!/opt/local/Library/Frameworks/Python.framework/Versions/2.7/Resources/Python.app/Contents/MacOS/Python
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Turn-Taking Measurement Tools
#
# Tidy and push -- adds headers to source files.
# By Peter Raffensperger 2012
# 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
import sys
import os

from projectinfo import *

def add_file_headers_and_do_search_and_replace():
	PYTHON_EXTENSIONS = ['.py']
	EXCEPTIONS = ['tidy_and_push.py']
	SEARCH_AND_REPLACE = {'__version__ =.*?\n': '__version__ = "' + VERSION + '"\n',
		'turntakingmeasurementtoolsversion =.*?\n': 'turntakingmeasurementtoolsversion = "' + VERSION + '"\n',
	}
	for root, dirs, files in os.walk('.'):
		for f in files:
			fpath = os.path.join(root, f)
			extension = os.path.splitext(f)[1]
			if extension in PYTHON_EXTENSIONS and f not in EXCEPTIONS:
				print "Modifying", fpath
				ff = open(fpath, 'r')
				contents = ff.read()
				ff.close()
				endOfHeader = contents.rfind(BANNER)
				header = HEADER
				header = header.replace('%filename%', f)
				if endOfHeader > 0:
					contents = header + '\n' +  contents[endOfHeader+len(BANNER)+2:]
				else:
					contents = header + '\n' + contents
				for key in SEARCH_AND_REPLACE:
					contents = re.sub(key, SEARCH_AND_REPLACE[key], contents)
	
				ff = open(fpath, 'w')
				ff.write(contents)
				ff.close()

def run_tests():
	print "Running test suite..."
	execfile('test/testall.py')

def commit():
	print "Enter a commit message"
	msg = raw_input()
	os.system('git commit -am "' + msg + '"')

def push_to_google_code():
	print "Pushing changes to Google code git respository..."
	os.system('git push https://code.google.com/p/turn-taking-measurement-tools/ master')

def make_source_distribution():
	print "Making source distribution file..."
	os.system('python2.7 setup.py sdist --formats=zip')

add_file_headers_and_do_search_and_replace()
run_tests()	
commit()
push_to_google_code()
print "make source distribution? (press ENTER for no, or 'y' then ENTER for yes)"
answer = raw_input()
if answer == 'y':
	make_source_distribution()