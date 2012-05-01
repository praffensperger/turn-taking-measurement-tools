
try:
	import turntakingmeasurementtools
except ImportError:
	import sys
	sys.path.append('..')
	import turntakingmeasurementtools

usageAttemptSequences = [[0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1], 
						 [1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0], 
						 [0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0]]

def print_uas():
	print """Time    """,
	for t in range(len(usageAttemptSequences[0])):
		gap = '  '
		if len(str(t)) == 2:
			gap = ' '
		print str(t) + gap,
	for a in [0, 1, 2]:
		print
		print "Agent " + str(a+1) + ' ',
		for t in range(len(usageAttemptSequences[a])):
			print str(usageAttemptSequences[a][t]) + '  ',
	print

print """Consider a situation where we have a 3 agents who share a common
resource that can only be used by one of the agents at a time. If two agents
try to use the resource at the same time, then neither agent gets usage of the
resource at that time.

Suppose that the agents try to use the shared resource through time as:"""
print_uas()
print """where 1 represents the agent trying to use the shared resource at time t
and 0 represents the agent not trying to use the resource.

To what degree are the agents taking turns using the shared resource?

[Press ENTER to continue]"""
blah = raw_input()
print """To answer this question, we need a quantitative metric for turn-taking.
This software package implements tau-tau, a simple turn-taking metric
developed by Peter Raffensperger, Russell Webb, Phillip Bones and Allan
McInnes at the University of Canterbury in 2009-2012 for research into
multi-agent systems and emergent communication. You may find addition
applications for our turn-taking metric in conversational analysis, spoken
dialog systems, medium access control in computer networks, biology and other
areas.

The original research reference is:
Raffensperger, P. A., Webb, R. Y., Bones, P. J., and McInnes, A. I. (2012). 
A simple metric for turn-taking in emergent communication. 
Adaptive Behavior, 20(2):104-116.

[Press ENTER to continue]"""
blah = raw_input()
print """Abstract:
To facilitate further research in emergent turn-taking, we propose a metric
for evaluating the extent to which agents take turns using a shared resource.
Our measure reports a turn-taking value for a particular time and a particular
timescale, or "resolution," in a way that matches intuition. We describe how
to evaluate the results of simulations where turn-taking may or may not be
present and analyze the apparent turn-taking that could be observed between
random independent agents. We illustrate the use of our turn-taking metric by
reinterpreting previous work on turn-taking in emergent communication and by
analyzing a recorded human conversation.

[Press ENTER to continue]"""
blah = raw_input()
print """Back to our agents."""
print_uas()
print """The turn-taking depends on time, and on the *resolution*, or the 
window length that we examine. Suppose we're just interested in the turn-
taking value of the entire sequence, starting at time 0 and with a 
resolution of 12, the whole length. Then:
tautau(usageAttemptSequences, 0, 12) = """ + str(turntakingmeasurementtools.tautau(usageAttemptSequences, 0, 12))
print """How does this work? tautau is defined as the product of the fairness
and the efficiency of the agents' turn allocations. The agents' turn
allocations are (for t = 0 and r = 12):
allocations(usageAttemptSequences, 0, 12) = """ + str(turntakingmeasurementtools.allocation(usageAttemptSequences, 0, 12))
print """That is, each agent gets a chance to use the shared resource 3 times without another 
agent simultaneously butting in.
[Press ENTER to continue]"""
blah = raw_input()
print """The fairness is calculated as the agent with the minimum allocation
divided by the sum of the agents' allocations, normalised into the range [0, 1]:
fairness_min(usageAttemptSequences, 0, 12) = """ + str(turntakingmeasurementtools.fairness_min(usageAttemptSequences, 0, 12))
print """And the efficiency is the sum of the agents' allocations, normalised into the range [0, 1]:
efficiency(usageAttemptSequences, 0, 12) = """ + str(turntakingmeasurementtools.efficiency(usageAttemptSequences, 0, 12))
