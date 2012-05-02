# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Turn-Taking Measurement Tools v0.1 
#
# example2.py
#
# By Peter Raffensperger 02 May 2012
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

import sys
import cPickle as pickle
import fpformat

import numpy

import lineplot
import createorload
import conversation_usage_attempt_sequences
try:
	import turntakingmeasurementtools
except ImportError:
	sys.path.append('..')
	import turntakingmeasurementtools


def GetOverallUsage(uas):
	uasT = numpy.array(uas).transpose()
	overallUsage = []
	for u in uasT:
		if u.sum() == 0:
			overallUsage.append(0)
		elif u.sum() == 1:
			overallUsage.append(1)
		elif u.sum() > 1:
			overallUsage.append(2)
		else:
			assert(False)
	return overallUsage

def enter_to_continue():
	print '[Press ENTER to continue]'
	blah = raw_input()

forceRecalculation = False

cpickleversionfile = open('cpickleversion', 'r')
if pickle.__version__ != cpickleversionfile.read():
	print "Detected a different version of cPickle than the one used to make the data files."
	print "You will have to recalculate some values which might have otherwise been cached."
	forceRecalculation = True
	cpickleversionfile.close()
	cpickleversionfile = open('cpickleversion', 'w')
	cpickleversionfile.write(pickle.__version__)
cpickleversionfile.close()	

decimationFactor = 441 #	* 2

maxTimeStep = 6000

audioDisplayRelativeScale = 1
displayDecimationRatio = decimationFactor * audioDisplayRelativeScale
dt = 0.01
dt_audio = dt / audioDisplayRelativeScale
resolution = 500
resolutionsStepSize = 250
maxTestResolution = maxTimeStep
testResolutions = [100, 250, resolution, 1000, 1500, 2000, 3000, 4000, 5000]
numAgents = 4

print """This example parallels Section 5 of 
Raffensperger, P. A., Webb, R. Y., Bones, P. J., and McInnes, A. I. (2012). 
A simple metric for turn-taking in emergent communication. 
Adaptive Behavior, 20(2):104-116.

Here we will examine the quantity of turn-taking present in a record human
conversation, taken from the COnversational Speech In Noisy Environments 
(COSINE) corpus created by:
Stupakov, A., Hanusa, E., Bilmes, J., & Fox, D. (2009). 
COSINE - a corpus of multi-party COnversational Speech In Noisy Environments. 
In IEEE International Conference on Acoustics, Speech and Signal Processing, 
2009, (ICASSP 2009) (pp. 4153-4156). IEEE.

See also:
Stupakov, A., Hanusa, E., Vijaywargi, D., Fox, D., & Bilmes, J. (2012). 
The design and collection of COSINE, a multi-microphone in situ speech corpus 
recorded in noisy environments. Computer Speech & Language, 26(1), 52-66.

The data here are from a conversation from Session 2 of the COSINE corpus, 
starting at 7 minutes 47.5 seconds into the session and lasting 1 minute.
The original audio was filtered with a one-pole high pass filter with a
cutoff frequency of 478 Hz, followed by an envelop follower, then thresholded.
The resulting usage attempt sequences were decimated from 44100 Hz down to 
100 Hz."""
uasStandardForm = [[], [], [], []]
uasCompressed = conversation_usage_attempt_sequences.uasCompressed
for usageStep in uasCompressed:
	for i in range(4):
		uasStandardForm[i].append((usageStep/(2**i)) % 2)
enter_to_continue()

print """The usage attempt sequences reveal when the four participants in the
conversation are talking. Sometimes no one is talking and the conversational 
floor goes 'unused,' other times more than one person is talking and there is
a 'collision.' Out of the """ + str(maxTimeStep) + """ time steps, we have
these statistics:"""
overallUsage = createorload.CreateOrLoadByObject(uasStandardForm, GetOverallUsage, 'overallusage_uas', 
	forceCreation=forceRecalculation)
print "Total time steps unused    :", (numpy.array(overallUsage) == 0).sum()
print "Total time steps single use:", (numpy.array(overallUsage) == 1).sum()
print "Total time steps collision :", (numpy.array(overallUsage) == 2).sum()	

print """If you have Gnuplot or matplotlib installed, you can look at these 
data on a graph."""

x = numpy.arange(0.0, len(overallUsage) / 100.0, dt)
graph = lineplot.plotxy(x, overallUsage, 'overall usage', 't (seconds)', '0-unused, 1-single, 2-collision')
enter_to_continue()
del graph

print """We have to choose a resolution which we will use to measure the turn-taking.
There is a time between about 25 seconds and 30 seconds when the third agent talks
while the others are mostly quiet. (If you have a graphing package you can see this
in the next graph.) To discriminate this low turn-taking period, we will chose a
resolution of r = """ + str(resolution/dt) + """ seconds. Given our sample rate of """ + str(1.0/dt) + """ Hz, this means 
r = """ + str(resolution) + """ samples.
"""

labels = ['$S_{M4}(t)$', '$S_{F3}(t)$', '$S_{M2}(t)$', '$S_{F1}(t)$']
graph = lineplot.humanTTturnrecord(labels, uasStandardForm, dt)
enter_to_continue()
del graph

print """Just to check that we aren't missing anything, we'll have a look at the
mean turn-taking at a variety of resolutions. 
"""

ttValuesWereComputed = False

def get_mean_tts_and_tts_at_resolution(testResolutions):
	global ttValuesWereComputed
	ttValuesWereComputed = True
	print "Computing mean turn-taking values... (this may take a while)"
	meanTTs = []
	ttsAtResolution = []
	for r in testResolutions:
		ttSum = 0.0
		ttCount = 0
		for t in range(0, maxTimeStep-r):
			tt = turntakingmeasurementtools.tautau(uasStandardForm, t, r)
			if r == resolution:
				ttsAtResolution.append(tt)
			ttSum += tt
			ttCount +=1
		if ttCount > 0:
			meanTTs.append(ttSum/ttCount)
		print "r =", r, " => mean tautau =", meanTTs[-1]
	assert(len(ttsAtResolution) > 0)
	return meanTTs, ttsAtResolution

meanTTs, ttsAtResolution = createorload.CreateOrLoadByObject(testResolutions, get_mean_tts_and_tts_at_resolution, 'mean_turn_taking_values_and_tts_at_resolution', 
	forceCreation=forceRecalculation)

if not ttValuesWereComputed:
	print "Loaded mean turn-taking values from a file!"
	for r, mtt in zip(testResolutions, meanTTs):
		print "r =", r, " => mean tautau =", mtt
		
print """Notice that the mean turn-taking mostly increases with increasing resolution.
This is to be expected. See Section 2.3 of 
Raffensperger, P. A., Webb, R. Y., Bones, P. J., and McInnes, A. I. (2012). 
A simple metric for turn-taking in emergent communication. 
Adaptive Behavior, 20(2):104-116.
"""
graph = lineplot.plotxy(testResolutions, meanTTs, 'Mean turn-taking as a function of resolution', 'r (seconds)', r'Mean $\tau\tau(t, r)$')
enter_to_continue()
del graph

samplesize = 10000

print """Now that we have chosen a resolution, we can look at the turn-taking as a 
function of time. But first, we'd like to know if the agents have produced turn-taking
better than the best possible random agents. So we'll estimated the mean turn-taking
of the worst-case probabilistic agents, which is agents that attempt to use the shared
resource with a probability pu = 1.0 / A, where A is the number of agents.
For four random agents, at a resolution of """ + str(resolution) +  """ we estimated
this mean value with a sample of """ + str(samplesize) + """ random usage attempt sequences as:
"""
if forceRecalculation:
	save_random_tt_distribution(numAgents, resolution, 1.0/numAgents, samplesize)
randomAgentsMeantt, randomAgentsVariancett = turntakingmeasurementtools.estimate_tt_mean_and_variance(numAgents, resolution, 1.0/numAgents, samplesize=samplesize, persistentData=True)
print randomAgentsMeantt
print """
The turn-taking over time can be visualised with respect to his value with the following graph.
The horizontal line is the expected turn-taking of random agents.
Sometimes, the four participants in the conversation take turns worse than random agents!
"""
x = numpy.arange(0.0, len(ttsAtResolution) / 100.0, dt)
graph = lineplot.plotxy_hline(x, ttsAtResolution, 'Turn-taking as a function of time at r = ' + str(resolution), 't (seconds)', r'$\tau\tau(t, r)$', randomAgentsMeantt)
enter_to_continue()
del graph
print """If you have no graphing package, then you can see the values printed as a table:"""
displayResolution = 50
for i, t, tt in zip(range(len(x)), x, ttsAtResolution):
	if i % displayResolution == 0:
		print "t =", fpformat.fix(t, 2), " tautau(t, " + str(resolution) + ") =", fpformat.fix(tt, 3), "E(tautau)|Random agents =", fpformat.fix(randomAgentsMeantt, 4)
		if (i/displayResolution) % 20 == 19:
			enter_to_continue()
