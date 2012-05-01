# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Turn-Taking Measurement Tools v0.1 
#
# turntakingmeasurementtools.py
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


__version__ = "0.1"

"""Turn-Taking Measurement Tools

Do you need to measure the quantity of turn-taking present in the behaviour of a
group of agents? This is the software library for you.
Turn-Taking Measurement Tools is a software library that implements a quantitative
metric for turn-taking. A simple turn-taking metric was developed by Peter
Raffensperger, Russell Webb, Phillip Bones and Allan McInnes at the University
of Canterbury in 2009-2012 for research into multi-agent systems and emergent
communication. You may find addition applications for our turn-taking metric in
conversational analysis, spoken dialog systems, medium access control in
computer networks, biology and other areas. The current implementation is in 
Python.

Features:
- Functions for measuring the quantity of turn-taking at different time
  resolutions in binary-valued usage attempt sequences of arbitrary lengths with
  any number of agents
- Functions for fairness and efficient metrics
- Estimation routines for the turn-taking of random agents
- Examples

If you use Turn-Taking Measurement Tools in an academic project, we invite you
to reference the original publication:
Raffensperger, P. A., Webb, R. Y., Bones, P. J., and McInnes, A. I. (2012). 
A simple metric for turn-taking in emergent communication. 
Adaptive Behavior, 20(2):104-116.

Paper abstract for "A simple metric for turn-taking in emergent communication":
To facilitate further research in emergent turn-taking, we propose a metric for
evaluating the extent to which agents take turns using a shared resource. Our
measure reports a turn-taking value for a particular time and a particular
timescale, or "resolution," in a way that matches intuition. We describe how to
evaluate the results of simulations where turn-taking may or may not be present
and analyze the apparent turn-taking that could be observed between random
independent agents. We illustrate the use of our turn-taking metric by
reinterpreting previous work on turn-taking in emergent communication and by
analyzing a recorded human conversation.
"""

import math
import sys
import os
import cPickle as pickle
import random

import numpy


# Metric functions

def tautau(U, t, r):
	"""
	Compute the quantity of turn-taking present in the usage attempt sequence U, at time t and 
	resolution r, using the block of time steps [t, t+r-1].
	
	Parameters:
	U -- a binary valued usage attempt sequence of shape (A, l), where A is the number of agents 
		 and l is the length. (As either a numpy array or a list of lists)
	t -- the time at which to calculate the turn-taking measure
	r -- the 'resolution' or window length, with l <= t+r
	
	Return value:
	A real value in [0, 1] representing the quantity of turn-taking in U in the range [t, t+r-1]
	
	See Eqs. 4 and 5 in:
	Raffensperger, P. A., Webb, R. Y., Bones, P. J., and McInnes, A. I. (2012). 
	A simple metric for turn-taking in emergent communication. 
	Adaptive Behavior, 20(2):104-116.	
	"""
	W = _pick_window(U, t, r)
	return _tautau_of_window(W)

def allocation(U, t, r):
	"""
	Compute the quantity of turn-taking present in the usage attempt sequence U, at time t and 
	resolution r, using the block of time steps [t, t+r-1].
	
	Parameters:
	U -- a binary valued usage attempt sequence of shape (A, l), where A is the number of agents 
		 and l is the length. (As either a numpy array or a list of lists)
	t -- the time at which to calculate the agent allocations
	r -- the 'resolution' or window length, with l <= t+r
	
	Return value:
	A vector of length A representing turn allocations of each agent
	
	See Eq. 1 in:
	Raffensperger, P. A., Webb, R. Y., Bones, P. J., and McInnes, A. I. (2012). 
	A simple metric for turn-taking in emergent communication. 
	Adaptive Behavior, 20(2):104-116.	
	"""
	W = _pick_window(U, t, r)
	return _allocation_of_window(W)
	
def f_turn(U, t, r):
	"""
	Compute the Iizuka and Ikegami turn-taking fitness value present in the usage attempt sequence U, 
	at time t and resolution r, using the block of time steps [t, t+r-1].
	
	Parameters:
	U -- a binary valued usage attempt sequence of shape (2, l), this measure is only defined for 
		 pairs of agents, where l is the length. (As either a numpy array or a list of lists)
	t -- the time at which to calculate the turn-taking measure
	r -- the 'resolution' or window length, with l <= t+r
	
	Return value:
	A real value in [0, r*r/4] representing the quantity of turn-taking in U in the range [t, t+r-1]
	
	See Eqs. 8 and 9 in:
	Iizuka, H. and Ikegami, T. (2004). 
	Adaptability and diversity in simulated turn-taking behavior. 
	Artificial Life, 10(4):361-378.	
	"""
	W = _pick_window(U, t, r)
	assert(W.shape[0] == 2)	
	return 1.0*W[0].sum()*W[1].sum()

def fairness_min(U, t, r):
	"""
	Compute the fairness of the turn allocation in the usage attempt sequence U, at time t and 
	resolution r, using the block of time steps [t, t+r-1].
	
	Parameters:
	U -- a binary valued usage attempt sequence of shape (A, l), where A is the number of agents 
		 and l is the length. (As either a numpy array or a list of lists)
	t -- the time at which to calculate the fairness measure
	r -- the 'resolution' or window length, with l <= t+r
	
	Return value:
	A real value in [0, 1] representing the fairness of the turn allocation in U in the range [t, t+r-1]
	
	See Eq. 2 in:
	Raffensperger, P. A., Webb, R. Y., Bones, P. J., and McInnes, A. I. (2012). 
	A simple metric for turn-taking in emergent communication. 
	Adaptive Behavior, 20(2):104-116.	
	"""
	W = _pick_window(U, t, r)
	A = len(W)
	sumalloc = _allocation_of_window(W).sum()
	if sumalloc == 0:
		return 0.0
	return 1.0*A*_allocation_of_window(W).min()/sumalloc
	
def fairness_jain(U, t, r, exponent=2.0):
	"""
	Compute the Jain fairness of the turn allocation in the usage attempt sequence U, at time t and 
	resolution r, using the block of time steps [t, t+r-1].
	
	Parameters:
	U -- a binary valued usage attempt sequence of shape (A, l), where A is the number of agents 
		 and l is the length. (As either a numpy array or a list of lists)
	t -- the time at which to calculate the fairness measure
	r -- the 'resolution' or window length, with l <= t+r
	
	Return value:
	A real value representing the Jain fairness of the turn allocation in U in the range [t, t+r-1]
	
	See:
	Jain, R., Chiu, D., & Hawe, W. (1984). 
	A quantitative measure of fairness and discrimination for resource allocation in shared computer systems
	Tech. Report, Hudson, MA: Digital Equipment Corporation.
	"""
	W = _pick_window(U, t, r)
	allocs = _allocation_of_window(W)
	num = (allocs.sum()/len(allocs))**exponent
	den = ((allocs**exponent)/len(allocs)).sum()
	if den != 0.0:
		return num/den
	return 0.0

def efficiency(U, t, r):
	"""
	Compute the efficiency of the turn allocation in the usage attempt sequence U, at time t and 
	resolution r, using the block of time steps [t, t+r-1].
	
	Parameters:
	U -- a binary valued usage attempt sequence of shape (A, l), where A is the number of agents 
		 and l is the length. (As either a numpy array or a list of lists)
	t -- the time at which to calculate the efficiency measure
	r -- the 'resolution' or window length, with l <= t+r
	
	Return value:
	A real value in [0, 1] representing the efficiency of the turn allocation in U in the range [t, t+r-1]
	
	See Eq. 3 in:
	Raffensperger, P. A., Webb, R. Y., Bones, P. J., and McInnes, A. I. (2012). 
	A simple metric for turn-taking in emergent communication. 
	Adaptive Behavior, 20(2):104-116.	
	"""
	W = _pick_window(U, t, r)
	return 1.0*_allocation_of_window(W).sum() / r

def _pick_window(U, t, r):
	"""
	Picks out the time range [t, t+r-1] from U
	"""
	Un = numpy.array(U)
	if len(Un.shape) != 2:
		raise ValueError("The usage attempt sequence must be two dimensional")
	if Un.shape[0] < 2:
		raise ValueError("The usage attempt sequence must include values for at least two agents")
	if Un.shape[1] < (t+r):
		raise ValueError("The usage attempt sequence must have at least t + r time steps")
	if t < 0:
		raise ValueError("t must be zero or postive")
	if r < 0:
		raise ValueError("r must be zero or postive")
	if not ((Un == 0) | (Un == 1)).all():
		raise ValueError("The usage attempt sequence should be binary valued")
	W = [U[i][t:(t+r)] for i in range(len(U))]
	return numpy.array(W)

def _allocation_of_window(W):
	"""
	Compute the turn allocation present in the whole usage attempt sequence W. 
	
	Return value:
	A vector of length W.shape[0]  representing turn allocations of each agent
	
	See Eq. 1 in:
	Raffensperger, P. A., Webb, R. Y., Bones, P. J., and McInnes, A. I. (2012). 
	A simple metric for turn-taking in emergent communication. 
	Adaptive Behavior, 20(2):104-116.	
	"""
	alloc = numpy.zeros(W.shape[0])
	for i, WX in enumerate(W):
		Wpart = WX.copy()
		for j, WY in enumerate(W):
			if j != i:
				Wpart *= 1 - WY
		alloc[i] = Wpart.sum()
	return alloc

def _tautau_of_window(W):
	"""
	See Eq. 5 in:
	Raffensperger, P. A., Webb, R. Y., Bones, P. J., and McInnes, A. I. (2012). 
	A simple metric for turn-taking in emergent communication. 
	Adaptive Behavior, 20(2):104-116.	
	"""
	r = W.shape[1]
	A = W.shape[0]
	return 1.0*A/r*_allocation_of_window(W).min() 

# Random turn-taking functions

def generate_random_usage_attempt_sequence(numAgents, length, pu):
	"""
	Generate a random, binary-valued usage attempt sequence with a particular usage 
	attempt probability
	
	Parameters:
	numAgents -- the desired number of agents in the random usage attempt sequence
	length -- the number of time steps of the usage attempt sequence
	pu -- the probability that a bit in the usage attempt sequence will be 1
	
	Return value:
	A random binary-valued usage attempt sequence as a numpy array of shape (numAgents, length)
	
	See Section 3 of:
	Raffensperger, P. A., Webb, R. Y., Bones, P. J., and McInnes, A. I. (2012). 
	A simple metric for turn-taking in emergent communication. 
	Adaptive Behavior, 20(2):104-116.	
	"""
	assert(numAgents > 0)
	assert(length > 0)
	assert(pu >= 0.0)
	assert(pu <= 1.0)
	if pu < 1.0:
		x = 0.5/(1.0 - pu)
		W = x * numpy.random.rand(numAgents, length)
	else:
		W = numpy.ones((numAgents, length))
	W = W.round()
	return numpy.clip(W, 0.0, 1.0)
	
def generate_random_turn_taking_values(numAgents, r, pu, samples):
	"""
	Generate a population of random turn-taking values given the usage attempt
	probability of the agents 
	
	Parameters:
	numAgents -- the desired number of probabilistic agents to include
	r -- the turn-taking resolution
	pu -- the probability that a bit in each usage attempt sequence will be 1
	samples -- the number of random turn-taking values to generate
	
	Return value:
	A list of random turn-taking values
	
	See Section 3 of:
	Raffensperger, P. A., Webb, R. Y., Bones, P. J., and McInnes, A. I. (2012). 
	A simple metric for turn-taking in emergent communication. 
	Adaptive Behavior, 20(2):104-116.	
	"""
	tautaus = []
	for i in xrange(samples):
		tt = _tautau_of_window(generate_random_usage_attempt_sequence(numAgents, r, pu))
		tautaus.append(tt)
	return tautaus

TT_DISTRIBUTION_FILE_EXTENSION = '.ttdist'
TT_DISTRIBUTION_FILE_PREFIX = 'tt_dist'

def clean_up_tt_distribution_files():
	"""
	Deletes files in the local directory that are of extension type TT_DISTRIBUTION_FILE_EXTENSION and have names starting with TT_DISTRIBUTION_FILE_PREFIX
	"""
	for f in os.listdir('.'):
		if f.startswith(TT_DISTRIBUTION_FILE_PREFIX) and os.path.splitext(f)[1] == TT_DISTRIBUTION_FILE_EXTENSION:
			os.remove(f)

def get_tt_distribution_filename(numAgents, r, pu, samples):
	"""
	Gets standardised file name for turn-taking probability distribution files
	"""
	return TT_DISTRIBUTION_FILE_PREFIX + '_A' + str(numAgents) + '_r' + str(r) + '_P' + str(pu) + '_samples' + str(samples) + TT_DISTRIBUTION_FILE_EXTENSION
	
def save_random_tt_distribution(numAgents, r, pu, samples, verbose=False):
	"""
	Save a file with a population of random turn-taking values given the usage 
	attempt probability of the agents 
	
	Parameters:
	numAgents -- the desired number of probabilistic agents to include
	r -- the turn-taking resolution
	pu -- the probability that a bit in each usage attempt sequence will be 1
	samples -- the number of random turn-taking values to generate
	Keyword arguments:
	verbose -- set to True to make this function print out its status to stdin as it goes
	
	See Section 3 of:
	Raffensperger, P. A., Webb, R. Y., Bones, P. J., and McInnes, A. I. (2012). 
	A simple metric for turn-taking in emergent communication. 
	Adaptive Behavior, 20(2):104-116.	
	"""	
	filename = get_tt_distribution_filename(numAgents, r, pu, samples)
	try:
		os.remove(filename)
	except OSError:
		pass
	file = open(filename, 'w')
	if verbose: print "Generating", samples, "turn taking values for", numAgents, "agents, with P=", pu, 'with r=', r
	tautaus = generate_random_turn_taking_values(numAgents, r, pu, samples)
	if verbose: print "Sorting..."
	tautaus.sort()
	if verbose: print "Saving..."
	pickle.dump(tautaus, file)
	if verbose: print "Done!!"
	
def load_random_tt_distribution(numAgents, r, pu, samples):
	"""
	Load a file with a population of random turn-taking values, assuming that it exists
	
	Parameters:
	numAgents -- the desired number of probabilistic agents to include
	r -- the turn-taking resolution
	pu -- the probability that a bit in each usage attempt sequence will be 1
	samples -- the number of random turn-taking values to generate
	
	See Section 3 of:
	Raffensperger, P. A., Webb, R. Y., Bones, P. J., and McInnes, A. I. (2012). 
	A simple metric for turn-taking in emergent communication. 
	Adaptive Behavior, 20(2):104-116.	
	"""	
	filename = get_tt_distribution_filename(numAgents, r, pu, samples)
	file = open(filename, 'r')
	return pickle.load(file)
	
	
def estimate_tt_mean_and_variance(numAgents, r, pu, samplesize=20000, persistentData=False):
	"""
	Estimate the mean and variance of the turn-taking value for a group of 
	random agents with the given usage attempt probability.
	
	Parameters:
	numAgents -- the desired number of probabilistic agents to include
	r -- the turn-taking resolution
	pu -- the probability that a bit in each usage attempt sequence will be 1
	Keyword arguments:
	samplesize -- the number of independent turn-taking value samples to include
	persistentData -- set to True to save the turn-taking value distribution 
	   to disk for future use
	
	See Section 3 of:
	Raffensperger, P. A., Webb, R. Y., Bones, P. J., and McInnes, A. I. (2012). 
	A simple metric for turn-taking in emergent communication. 
	Adaptive Behavior, 20(2):104-116.	
	"""	
	tautaus = []
	if persistentData:
		try:
			tautaus = load_random_tt_distribution(numAgents, r, pu, samplesize)
		except (IOError, EOFError):
			save_random_tt_distribution(numAgents, r, pu, samplesize)
			tautaus = load_random_tt_distribution(numAgents, r, pu, samplesize)
	else:
		tautaus = generate_random_turn_taking_values(numAgents, r, pu, samplesize)
		
	tautaus_np = numpy.array(tautaus)
	m = tautaus_np.mean()
	v = tautaus_np.std()**2	
	return m, v

def estimate_probability_of_tt_due_to_chance(numAgents, r, samplesize, target_tt_value, persistentData=False, verbose=False):
	"""
	Estimate the probability that a particular turn-taking value is produced by
	random processes, assuming the worst case usage attempt probabilities for 
	all the agents
	
	Parameters:
	numAgents -- the desired number of probabilistic agents to include
	r -- the turn-taking resolution
	samplesize -- the number of independent turn-taking value samples to include

	Keyword arguments:
	persistentData -- set to True to save the turn-taking value distribution 
	   to disk for future use
	verbose -- set to True  
	
	See Section 3 of:
	Raffensperger, P. A., Webb, R. Y., Bones, P. J., and McInnes, A. I. (2012). 
	A simple metric for turn-taking in emergent communication. 
	Adaptive Behavior, 20(2):104-116.	
	"""		
	p = 1.0 / numAgents

	tautaus = []
	if persistentData:
		try:
			tautaus = load_random_tt_distribution(numAgents, r, p, samplesize)
		except IOError:
			save_random_tt_distribution(numAgents, r, p, samplesize)
			tautaus = load_random_tt_distribution(numAgents, r, p, samplesize)
	else:
		tautaus = generate_random_turn_taking_values(numAgents, r, p, samplesize)
	if verbose: print "Loaded!"
	tautaus_np = numpy.array(tautaus)
	if verbose: 
		print "Standard deviation of tautau(" + str(r) + ", t) is ", tautaus_np.std()
		print "Mean of tautau(" + str(r) + ", t) is ", tautaus_np.mean()
		print "Variance of tautau(" + str(r) + ", t) is ", tautaus_np.std()**2
	#import histogram
	#histogram.quickhistogram(tautaus, 20)
	def calc_prop(x):
		def estimateP_TautauAtLeastX(x, tautau, samples):
			count = 0
			for tt in tautau:
				if tt > x:
					count += 1
			return 1.0 * count / samples, count
		prob, count = estimateP_TautauAtLeastX(x, tautaus, samplesize)
		if verbose: 
			print "----------------------------"
			print "Probability of having tautau(" + str(r) + ", t) >= " + str(x) + " is ", prob
			print "Sample size is", samplesize, " count is ", count
		return prob
	
	return calc_prop(target_tt_value)
	
