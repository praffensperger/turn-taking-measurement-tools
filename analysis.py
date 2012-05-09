# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Turn-Taking Measurement Tools v0.9 
#
# analysis.py
#
# By Peter Raffensperger 09 May 2012
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



import time
import cPickle

import numpy

import lineplot
from turntakingcalculationtools import *


def summaryStatistics(Ufullsequence, r, start, end):
	tt, ee, ff = tt_e_f_ValuesAtResolution(Ufullsequence, r)
	print "At resolution r=", r
	print "Between t=", start, "and", end
	print "Mean tau tau \t", (numpy.array(tt[start:end])).mean()
	print "Std tau tau  \t", (numpy.array(tt[start:end])).std()
	
	print "Mean efficncy \t", (numpy.array(ee[start:end])).mean()
	print "Std efficncy  \t", (numpy.array(ee[start:end])).std()

	print "Mean fairness \t", (numpy.array(ff[start:end])).mean()
	print "Std fairness  \t", (numpy.array(ff[start:end])).std()

	print "tautau < 0.1  \t", (numpy.array(tt[start:end]) < 0.1).sum()

def GetTauTausFilename(U, upperResolutionLimit):
	hashcode = str(abs(hash(numpy.array(U).tostring())))
	print hashcode
	return "tt_means_stds" + hashcode + "r" + str(upperResolutionLimit) + ".pickle"

def LoadTauTaus(U, upperResolutionLimit):
	tt_means_stds_filename = GetTauTausFilename(U, upperResolutionLimit)
	file = open(tt_means_stds_filename, 'r')
	tautaus = cPickle.load(file)
	return tautaus
	

def calculateTauTaus_vs_resolution(U, upperResolutionLimit, resolution_step_size=1):
	max_resolution = min(len(U[0]), upperResolutionLimit)
	
	print "Calculating", upperResolutionLimit*len(U[0])/resolution_step_size, "ish turn-taking values..."
	tt_means_stds_filename = GetTauTausFilename(U, upperResolutionLimit)
	t1 = time.time()
	tau_x = turntaking_mean_std_cpp(U, max_resolution, resolution_step_size)
	file = open(tt_means_stds_filename, 'w')
	cPickle.dump(tau_x, file)
	t2 = time.time()
	print "Time taking for C++ based implementation:", t2 - t1, "seconds!"

def turnLengthDistribution(UASs):
	def countTurnLengths(UAS):
		lengths = [0]*len(UAS)
		thisTurnLength = 0
		isTurn = False
		for t in range(len(UAS)):
			if UAS[t] == 1:
				thisTurnLength += 1
				if not isTurn:
					isTurn = True
			else:
				if isTurn:
					isTurn = False
					lengths[thisTurnLength] += 1
					thisTurnLength = 0
		return numpy.array(lenghts)
	
	dist = sum([countTurnLengths(UAS) for UAS in UASs])
		
	while sum([dist_elements[-1] for dist_elements in dist]) == 0:
		lengths.pop()
		
	
	return

def createGraphOfMeanTauTau_vs_resolution(U, upperResolutionLimit, recalculate=True, 
	resolution_step_size=1, 
	filename_mean="dipaolo_mean_tautau(t,r)_vs_r_plot.pdf", 
	filename_std="dipaolo_std_tautau(t,r)_vs_r_plot.pdf", upperResolutionLimitDisplayOnly=None, 
	verticalConstructionLine=None):
	
	if upperResolutionLimitDisplayOnly is None:
		upperResolutionLimitDisplayOnly = upperResolutionLimit
	
	max_resolution = min(len(U[0]), upperResolutionLimit)
	
	displayGraphs = True

	if recalculate:
		calculateTauTaus_vs_resolution(U, upperResolutionLimit, resolution_step_size)
	else:
		import warnings
		warnings.warn("Recalculation not done!")

	tau_x = LoadTauTaus(U, upperResolutionLimit)
	
	sigmas = []
	thetas = []	
	rs = []
	for ts in tau_x:
		r, t, s = ts
		if r <= upperResolutionLimitDisplayOnly:
			sigmas.append(s)
			thetas.append(t)
			rs.append(r)
	
	#Calculate local maxima
	first_difference = numpy.array(thetas[1:]) - numpy.array(thetas[:-1])
	#extrema = abs(first_difference) < 1e-4
	increasing = first_difference > 0
	places_decreasing = numpy.nonzero(increasing == False)
	print "First point of decrease in mean tau tau vs resolution graph is at r=", places_decreasing[0][0]
	print places_decreasing
	
	if displayGraphs:		
		#lineplot.lineplot(rs, sigmas,)

		lineplot.lineplot_meantau(rs, thetas, sigmas, 
			r"Mean $\tau\tau(t, r)$ over time vs. resolution, $r$", 
			r'$r$', r'Mean $\tau\tau(t, r)$', 
			filename_mean, verticalConstructionLine)
			
		print "Max std occurs at r=", sigmas.index(max(sigmas))
			
		lineplot.lineplot(rs, sigmas, 
			r"Standard deviation of $\tau\tau(t, r)$ vs. resolution, $r$", 
			r'$r$', r'Standard deviation $\tau\tau(t, r)$', 
			filename_std, verticalConstructionLine)