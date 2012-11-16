# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Turn-Taking Measurement Tools v0.91 
#
# testall.py
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

import numpy

try:
	from turntakingmeasurementtools import *
except ImportError:
	import sys
	sys.path.append('..')
	from turntakingmeasurementtools import *

TWO_AGENTS_PERFECT_TT_4_STEPS = [[0, 1, 0, 1], [1, 0, 1, 0]]

assert(tautau([[0, 1], [1, 0]], 0, 2) == 1.0)
assert(tautau(TWO_AGENTS_PERFECT_TT_4_STEPS, 0, 2) == 1.0)
assert(tautau(TWO_AGENTS_PERFECT_TT_4_STEPS, 1, 2) == 1.0)
assert(tautau(TWO_AGENTS_PERFECT_TT_4_STEPS, 2, 2) == 1.0)
assert(tautau(TWO_AGENTS_PERFECT_TT_4_STEPS, 0, 4) == 1.0)
assert(f_turn(TWO_AGENTS_PERFECT_TT_4_STEPS, 0, 4) == 4.0)
assert(fairness_min(TWO_AGENTS_PERFECT_TT_4_STEPS, 0, 3) == 2.0/3)
assert(fairness_jain(TWO_AGENTS_PERFECT_TT_4_STEPS, 0, 3) == 0.9)
assert((allocation([[0, 1], [1, 0]], 0, 2) == numpy.array([1.0, 1.0])).all())
for t, r in zip([0,1], [1, 2, 3]):
	assert(efficiency(TWO_AGENTS_PERFECT_TT_4_STEPS, t, r) == 1)
for A, l in zip(range(1, 5), range(1, 5)):
	assert(generate_random_usage_attempt_sequence(A, l, 0.5).shape == (A, l))
	assert(generate_random_usage_attempt_sequence(A, l, 0.0).sum() == 0.0)	
	assert(generate_random_usage_attempt_sequence(A, l, 1.0).sum() == A*l)
	assert(len(generate_random_turn_taking_values(A, l, 0.5, 10)) == 10)
	assert((numpy.array(generate_random_turn_taking_values(A, l, 0.5, 10)) <= 1.0).all())	
	assert((numpy.array(generate_random_turn_taking_values(A, l, 0.5, 10)) >= 0.0).all())	
	assert(isinstance(get_tt_distribution_filename(A, l, 0.5, 10), str))
	save_random_tt_distribution(A, l, 0.5, 2)
	assert(len(load_random_tt_distribution(A, l, 0.5, 2)) == 2)
	m, v = estimate_tt_mean_and_variance(A, l, 0.5, samplesize=2, persistentData=True)
	assert(m <= 1.0)
	assert(m >= 0.0)
	assert(v >= 0.0)
	m, v = estimate_tt_mean_and_variance(A, l, 0.5, samplesize=2, persistentData=False)
	assert(m <= 1.0)
	assert(m >= 0.0)
	assert(v >= 0.0)
	p = estimate_probability_of_tt_due_to_chance(A, l, 2, 0.5, persistentData=False)
	assert(p >= 0.0)
	assert(p <= 1.0)
	p = estimate_probability_of_tt_due_to_chance(A, l, 2, 0.5, persistentData=True)
	assert(p >= 0.0)
	assert(p <= 1.0)
clean_up_tt_distribution_files()
print "All tests passed!"