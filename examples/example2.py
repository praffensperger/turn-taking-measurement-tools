# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Turn-Taking Measurement Tools v0.1 
#
# example2.py
#
# By Peter Raffensperger 01 May 2012
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



try:
	import turntakingmeasurementtools
except ImportError:
	import sys
	sys.path.append('..')
	import turntakingmeasurementtools

import sys
import cPickle as pickle

import numpy

import lineplot
#import turntakingcalculationtools
import createorload
import conversation_usage_attempt_sequences


def Decimate(waveform, ratio):
	waveform = numpy.array(waveform)
	nsamplesOld = len(waveform)
	assert((nsamplesOld % ratio) == 0)
	nsamplesNew = nsamplesOld / ratio
	waveform.shape = (nsamplesNew, ratio)
	waveform = waveform.T
	return waveform.flatten()[0:nsamplesNew]
	
def SmartDisplayDecimate(waveformIn, ratio):
	waveform = numpy.array(waveformIn)
	nsamplesOld = len(waveform)
	assert((nsamplesOld % ratio) == 0)
	nsamplesNew = nsamplesOld / ratio
	waveform.shape = (nsamplesNew, ratio)
	waveformMax = []
	waveformMin = []
	for w in waveform:
		waveformMax.append(max(w))
		waveformMin.append(min(w))
	return numpy.array(waveformMax), numpy.array(waveformMin)

def GetTTVsR(uasDecimated):
	#uasDecimated = createorload.GetObjectFromFile(uasDecimatedFilename)
	turntakingvalues_str = turntakingcalculationtools.get_cpp_tt_raw_multiagent([str(x) for x in uasDecimated], len(uasDecimated), start_r=100, resolution_step_size=100, num_agents=4, dry_run=False)
	
	resolutions = []
	mean_tts = []
	std_tts = []
	for l in turntakingvalues_str.split('\n')[:-1]:
		r, mean, std = l.split(' ')
		resolutions.append(int(r))
		mean_tts.append(float(mean))
		std_tts.append(float(std))
		
	records = resolutions, mean_tts, std_tts
	return records

def GetAllocationsAndTTs(uas):
	resolutions = [500, 1000, 3000]
	ttValuesAtResolutions = []
	allocationsAtResolutions = []
	efficiencies = []
	fairnesses = []
	for r in resolutions:
		tts = turntakingcalculationtools.turntakingValuesAtResolution(uas, r)
		allocations = turntakingcalculationtools.allocationsAtResolution(uas, r)
		efficiencies.append([sum(a) for a in numpy.array(allocations).transpose()])
		fairness = []
		for a in numpy.array(allocations).transpose():
			if sum(a) > 0:
				x = len(uas) * min(a) / sum(a)
			else:
				x = 0
			fairness.append(x)
	
		assert(len(fairness) == len(tts))
		fairnesses.append(fairness)
		ttValuesAtResolutions.append(tts)
		allocationsAtResolutions.append(allocations)

	return resolutions, ttValuesAtResolutions, allocationsAtResolutions, fairnesses, efficiencies

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

if __name__ == '__main__':
	forceRecalcuation = False
	
	decimationFactor = 441 #	* 2

	maxTimeStep = 6000
	
	audioDisplayRelativeScale = 1
	dispalyDecimationRatio = decimationFactor * audioDisplayRelativeScale

	uasStandardForm = [[], [], [], []]
	uasCompressed = conversation_usage_attempt_sequences.uasCompressed
	for usageStep in uasCompressed:
		for i in range(4):
			uasStandardForm[i].append((usageStep/(2**i)) % 2)
	
	overallUsage = createorload.CreateOrLoadByObject(uasStandardForm, GetOverallUsage, 'overallusage_uas', 
		forceCreation=forceRecalcuation)
	print "Total timesteps unused    :", (numpy.array(overallUsage) == 0).sum()
	print "Total timesteps single use:", (numpy.array(overallUsage) == 1).sum()
	print "Total timesteps collision :", (numpy.array(overallUsage) == 2).sum()	

	dt = 0.01
	dt_audio = dt / audioDisplayRelativeScale
	x = numpy.arange(0.0, len(overallUsage) / 100.0, dt)
	g = lineplot.quickplot(overallUsage)
	lineplot.lineplot(x, overallUsage, 'overall usage', 't (seconds)', '0-unused, 1->single, 2->collision', 'overallusage.pdf')
	
	resolutions, mean_tts, std_tts = records
	lineplot.lineplot_meantau(resolutions, mean_tts, std_tts, '', '$r$ (seconds)', r'Mean $\tau\tau(t, r)$', 'tt_vs_r.pdf', resolutionDivisionFactor=100, showStd=True)
	
	#assert(decimationFactor == dispalyDecimationRatio)

	speakerNames = ['M7321 (Gary)', 'F1777 (Alisha)', 'M2828 (Daniel)', 'F0622 (Angela)']
	labels = ['$S_{M4}(t)$', '$S_{F3}(t)$', '$S_{M2}(t)$', '$S_{F1}(t)$']
	lineplot.humanTTturnrecord(labels, uasStandardForm, speakerWaveformPlotInformation, dt, dt_audio,
		'waveforms_and_turnrecords.pdf')
	lineplot.humanTTturnrecord(labels, uasStandardForm, speakerWaveformPlotInformation, dt, dt_audio,
		'waveforms_and_turnrecords.png')

	
	resolutions, ttValuesAtResolutions, allocationsAtResolutions, fairnesses, efficiencies = createorload.CreateOrLoadByObject(uasStandardForm, 
		GetAllocationsAndTTs, 'allocations_and_tts_all_agents', forceCreation=forceRecalcuation)
	#CreateOrLoad(uasFilename, GetAllocationsAndTTs, forceCreation=True)
	assert(len(resolutions) > 0)
	assert(len(ttValuesAtResolutions) > 0)

	#lineplot.lineplotmulti(range(len(uasStandardForm[0])), uasStandardForm, 't', [s[:5] for s in speakerNames], 'turnrecords.pdf', [1.1 for s in speakerNames])
	
	ttOfFourRandomAgents = {500: 0.362815664, 1000: 0.38001052, 3000: 0.397595329334} #Computed from 10^6 random usage attempt sequences
	ttOfFourRandomAgents_std = {500: 0.0344489173741, 1000: 0.0247301516641, 3000: 0.0144640861557}
	
	for r, allocations, tts, fairness, efficiency in zip(resolutions, allocationsAtResolutions, ttValuesAtResolutions, fairnesses, efficiencies):
		#x = range(6000)
		#import pdb; pdb.set_trace()
		#allocations = allocations + ([0] * (6000 - len(allocations)))
		#tts = tts + ([0] * (6000 - len(tts)))
		#lineplot.lineplotmulti(range(len(allocations[0])),
		#	allocations, 't', 
		#	[s[:5] for s in speakerNames], 'allocations' + '_' + str(r) + '.pdf', [allocations.max() for s in speakerNames])
		#print len(allocations[0]), len(tts)
		x = numpy.arange(0.0, len(tts) / 100.0, dt)
		assert(len(x) == len(tts))
		lineplot.lineplot_tt_over_time(x, 
			tts, '', '$t$ (seconds)', r'$\tau\tau(t, ' + str(r/100) + 's)$', 'all4_tt' + str(r) + '.pdf', ttOfFourRandomAgents[r], xmax=maxTimeStep/100.0)
		lineplot.lineplot(x, fairness, '', 't (seconds)', 'fairness', 'fairness' + str(r) + '_all4.pdf')
		print "r=", r
		print "Mean fairness", sum(fairness) / len(fairness)
		lineplot.lineplot(x, efficiency, '', 't (seconds)', 'efficiency', 'efficiency' + str(r) + '_all4.pdf')
		print "Mean efficiency", sum(efficiency) / len(efficiency)
	
	print "Now with just three agents in the picture"
	uasStandardFormJustThree = uasStandardForm[0:2] 
	uasStandardFormJustThree.append(uasStandardForm[3])
	lineplot.lineplotmulti(range(len(uasStandardFormJustThree[0])), uasStandardFormJustThree, 't', ['a', 'b', 'c'], 'turnrecords_just3.pdf', [1.1, 1.1, 1.1, ])
	assert(len(uasStandardFormJustThree) == 3)
	resolutions, ttValuesAtResolutions, allocationsAtResolutions, fairnesses, efficiencies = createorload.CreateOrLoadByObject(uasStandardFormJustThree, 
		GetAllocationsAndTTs, 'allocations_and_tts_just3_agents', forceCreation=forceRecalcuation)
	
	ttOfThreeRandomAgents = {500: 0.400968246, 1000: 0.413663778, 3000: 0.426638539} #Computed from 10^6 random usage attempt sequences
	ttOfThreeRandomAgents_std = {500: 0.0321125947828, 1000: 0.0229164133486, 3000: 0.0133680182131}
	
	for r, allocations, tts in zip(resolutions, allocationsAtResolutions, ttValuesAtResolutions):
		x = numpy.arange(0.0, len(tts) / 100.0, dt)
		assert(len(x) == len(tts))
		lineplot.lineplot_tt_over_time(x, 
			tts, '', '$t$ (seconds)', r'$\tau\tau(t, ' + str(r/100) + r's)$ (3 agents)', 'just3_tt' + str(r) + '.pdf', ttOfThreeRandomAgents[r], xmax=maxTimeStep/100.0)

	print "Now with just two agents in the picture, first and last"
	uasStandardFormJustTwo = [uasStandardForm[0], uasStandardForm[3]]
	lineplot.lineplotmulti(range(len(uasStandardFormJustTwo[0])), uasStandardFormJustTwo, 't', ['a', 'b', 'c'], 'turnrecords_just2.pdf', [1.1, 1.1, 1.1, ])
	resolutions, ttValuesAtResolutions, allocationsAtResolutions, fairnesses, efficiencies = createorload.CreateOrLoadByObject(uasStandardFormJustTwo, 
		GetAllocationsAndTTs, 'allocations_and_tts_just2_agents', forceCreation=forceRecalcuation)
	
	ttOfTwoRandomAgents = {500: 0.474734268, 1000: 0.482170214, 3000: 0.489685685334} #Computed from 10^6 random usage attempt sequences
	ttOfTwoRandomAgents_std = {500: 0.0289842857167, 1000: 0.0205423406455, 3000: 0.0119255780415}
	
	for r, allocations, tts in zip(resolutions, allocationsAtResolutions, ttValuesAtResolutions):
		x = numpy.arange(0.0, len(tts) / 100.0, dt)
		assert(len(x) == len(tts))
		lineplot.lineplot_tt_over_time(x, 
			tts, '', '$t$ (seconds)', r'$\tau\tau(t, ' + str(r/100) + r's)$ (2 agents)', 'just2_tt' + str(r) + '.pdf', ttOfTwoRandomAgents[r], xmax=maxTimeStep/100.0)

	print "Now with just two agents in the picture, first and third"
	uasStandardFormJustTwo = [uasStandardForm[0], uasStandardForm[2]]
	lineplot.lineplotmulti(range(len(uasStandardFormJustTwo[0])), uasStandardFormJustTwo, 't', ['a', 'b', 'c'], 'turnrecords_just2.pdf', [1.1, 1.1, 1.1, ])
	resolutions, ttValuesAtResolutions, allocationsAtResolutions, fairnesses, efficiencies = createorload.CreateOrLoadByObject(uasStandardFormJustTwo, 
		GetAllocationsAndTTs, 'allocations_and_tts_just2_agents13', forceCreation=forceRecalcuation)
	

	for r, allocations, tts in zip(resolutions, allocationsAtResolutions, ttValuesAtResolutions):
		x = numpy.arange(0.0, len(tts) / 100.0, dt)
		assert(len(x) == len(tts))
		lineplot.lineplot_tt_over_time(x, 
			tts, '', '$t$ (seconds)', r'$\tau\tau(t, ' + str(r/100) + r's)$ (2 agents 1n3)', 'just2_13_tt' + str(r) + '.pdf', ttOfTwoRandomAgents[r], xmax=maxTimeStep/100.0)



	
