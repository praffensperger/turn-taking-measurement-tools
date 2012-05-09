.. Turn-Taking Measurement Tools documentation master file, created by
   sphinx-quickstart on Wed May  9 11:31:38 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Turn-Taking Measurement Tools documentation
=========================================================

Do you need to measure the quantity of turn-taking present in the behaviour of
a group of agents? This is the software library for you.
Turn-Taking Measurement Tools is a software library that implements a
quantitative metric for turn-taking. A simple turn-taking metric was developed
by Peter Raffensperger, Russell Webb, Phillip Bones and Allan McInnes at the
University of Canterbury in 2009-2012 for research into multi-agent systems
and emergent communication. You may find addition applications for our
turn-taking metric in conversational analysis, spoken dialog systems, medium
access control in computer networks, biology and other areas. The current
implementation is in Python.

If you use Turn-Taking Measurement Tools in an academic project, we invite you
to reference the original publication:
Raffensperger, P. A., Webb, R. Y., Bones, P. J., and McInnes, A. I. (2012). 
A simple metric for turn-taking in emergent communication. 
Adaptive Behavior, 20(2):104-116.

Paper abstract for "A simple metric for turn-taking in emergent
communication":
To facilitate further research in emergent turn-taking, we propose a metric
for evaluating the extent to which agents take turns using a shared resource.
Our measure reports a turn-taking value for a particular time and a particular
timescale, or "resolution," in a way that matches intuition. We describe how
to evaluate the results of simulations where turn-taking may or may not be
present and analyze the apparent turn-taking that could be observed between
random independent agents. We illustrate the use of our turn-taking metric by
reinterpreting previous work on turn-taking in emergent communication and by
analyzing a recorded human conversation.

Features
---------
- Functions for measuring the quantity of turn-taking at different time resolutions in binary-valued usage attempt sequences of arbitrary lengths with any number of agents
- Functions for fairness and efficient metrics
- Estimation routines for the turn-taking of random agents
- Python doc strings for all key functions
- Examples (run examples/main.py)

Dependencies
-------------
- numpy
- matplotlib or pyGnuplot for examples (optional)

Contents
---------

.. toctree::
   :maxdepth: 2
   
   turntakingmeasurementtools
   license


