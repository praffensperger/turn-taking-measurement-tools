Turn-Taking Measurement Tools
+++++++++++++++++++++++++++++

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

Features:
---------
- Functions for measuring the quantity of turn-taking at different time
resolutions in binary-valued usage attempt sequences of arbitrary lengths with
any number of agents
- Functions for fairness and efficient metrics
- Estimation routines for the turn-taking of random agents
- Python doc strings for all key functions
- Examples (run examples/main.py)

Dependencies:
-------------
- numpy
- matplotlib or pyGnuplot for examples (optional)

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

License:
--------
Turn-Taking Measurement Tools is licensed under a new BSD license. You are
encouraged to use it in both free and commercial software. If you use this
library in an academic context, we would appreciate it if you referenced our
paper.

Copyright (C) 2012, Peter Raffensperger. All rights reserved.
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
- Redistributions of source code must retain the above copyright notice, this
list of conditions and the following disclaimer.
- Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation
and/or other materials provided with the distribution.
- Neither the name of Peter Raffensperger nor the names of other contributors
may be used to endorse or promote products derived from this software without
specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
