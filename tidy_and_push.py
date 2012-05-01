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
import re
import datetime

VERSION = "0.1"
DATE = datetime.date.strftime( datetime.date.today(), "%d %B %Y")
FIRST_YEAR = 2012
THIS_YEAR = int(datetime.date.strftime( datetime.date.today(), "%Y"))
if THIS_YEAR > FIRST_YEAR:
	YEARS = str(FIRST_YEAR) + '-' + str(THIS_YEAR)
else:
	YEARS = str(THIS_YEAR)
BANNER = "# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #"
HEADER = BANNER + """
# Turn-Taking Measurement Tools v""" + VERSION + """ 
#
# %filename%
#
# By Peter Raffensperger """ + DATE + """
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
""" + BANNER + """
"""

def add_file_headers_and_do_search_and_replace():
	PYTHON_EXTENSIONS = ['.py']
	EXCEPTIONS = ['tidy_and_push.py']
	SEARCH_AND_REPLACE = {'__version__ =.*?\n': '__version__ = "' + VERSION + '"\n',
		'turntakingmeasurementtoolsversion =.*?\n': 'turntakingmeasurementtoolsversion = "' + VERSION + '"\n'}
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
	os.system('p setup.py sdist --formats=zip')

add_file_headers_and_do_search_and_replace()
run_tests()	
commit()
push_to_google_code()
print "make source distribution?"
answer = raw_input()
if answer == 'y':
	make_source_distribution()