# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Turn-Taking Measurement Tools v0.9 
#
# lineplot.py
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


#Python 2.6.4
import cPickle
import os

import numpy
library = ''
try:
	import matplotlib
	import matplotlib.pyplot as plt
	library = 'matplotlib'
	#raise ImportError #Uncomment this line to make Gnuplot take priority over matplotlib
except ImportError:
	try:
		import Gnuplot
		library = 'Gnuplot'
	except ImportError:
		pass

def plotxy(x, y, title, xlabel, ylabel):
	pass

def humanTTturnrecord(labels, uasStandardForm, dt):
	pass
	
def plotxy_hline(x, y, title, xlabel, ylabel, hlinepos):
	pass

if library == 'matplotlib':
	def plotxy(x, y, title, xlabel, ylabel):
		verticalConstructionLine = None
		tex_fontsize = 18
		title_fontsize = 24
		axis_label_fontsize = 20
		
		matplotlib.rc('text', usetex=True)
		matplotlib.rc('font', family='serif')
		
		matplotlib.rcParams['xtick.direction'] = 'out'
		matplotlib.rcParams['ytick.direction'] = 'out'
		
		plt.figure()
		
		plt.plot(x, y, color='black')
	
		plt.title(title, fontsize=title_fontsize)
		plt.xlabel(xlabel, fontsize=axis_label_fontsize)
		plt.ylabel(ylabel, fontsize=axis_label_fontsize)

		ax = plt.gca()
		for tick in ax.xaxis.get_major_ticks():
			tick.label1.set_fontsize(tex_fontsize)
		for tick in ax.yaxis.get_major_ticks():
			tick.label1.set_fontsize(tex_fontsize)

		#ax.xaxis.set_major_locator(plt.FixedLocator(range(0, range_, r*2)))
	
		plt.show()
	def plotxy_hline(x, y, title, xlabel, ylabel, hlinepos):
		tex_fontsize = 18
		title_fontsize = 24
		axis_label_fontsize = 20
		
		matplotlib.rc('text', usetex=True)
		matplotlib.rc('font', family='serif')
		
		matplotlib.rcParams['xtick.direction'] = 'out'
		matplotlib.rcParams['ytick.direction'] = 'out'
		
		plt.figure()
		
		plt.plot(x, y, color='black')
		plt.plot([x[0], x[-1]], [hlinepos, hlinepos], color='black', linestyle=':')
		plt.title(title, fontsize=title_fontsize)
		plt.xlabel(xlabel, fontsize=axis_label_fontsize)
		plt.ylabel(ylabel, fontsize=axis_label_fontsize)

		ax = plt.gca()
		for tick in ax.xaxis.get_major_ticks():
			tick.label1.set_fontsize(tex_fontsize)
		for tick in ax.yaxis.get_major_ticks():
			tick.label1.set_fontsize(tex_fontsize)
	
		plt.show()

	def humanTTturnrecord(labels, uasStandardForm, dt):
		def plotLinesGrayBlack(x, y, linestyle='-'):
			plt.plot(x, y, color='0.65', linewidth=1, linestyle=linestyle)
			plt.plot(x, y, color='black', linewidth=0, marker='.', linestyle=linestyle)
		tex_fontsize = 18
		title_fontsize = 24
		axis_label_fontsize = 20
		
		matplotlib.rc('text', usetex=True)
		matplotlib.rc('font', family='serif')
		
		matplotlib.rcParams['xtick.direction'] = 'out'
		matplotlib.rcParams['ytick.direction'] = 'out'
		
		plt.figure(figsize=(8, 6))
		
		pos_left = 0.17
		pos_bottom = 0.2
		pos_width = 0.79
		pos_height = 0.65
		plt.axes([pos_left, pos_bottom, pos_width, pos_height])
	
		plt.title('Usage attempt sequences for four speakers', fontsize=title_fontsize)
		plt.xlabel('$t$ (seconds)', fontsize=axis_label_fontsize)
	
		#plt.ylabel(r'$U_1(t)$ \quad \quad \quad \quad $U_2(t)$', fontsize=axis_label_fontsize)
		plt.text(-11.5, 0.5, labels[0], fontsize=axis_label_fontsize, verticalalignment='center',)
		plt.text(-11.5, 2.8, labels[1], fontsize=axis_label_fontsize, verticalalignment='center',)
		plt.text(-11.5, 4.9, labels[2], fontsize=axis_label_fontsize, verticalalignment='center',)
		plt.text(-11.5, 7.3, labels[3], fontsize=axis_label_fontsize, verticalalignment='center',)
		
		visual_buffer = 0.1
		U2_offset = 1
		
		yAxisTickMarks = {}
		
		
		waveformOffset = 0.0
		verticalOffset = 0.0
		scales = [0.7, 0.5, 0.8, 0.7]
		for U, scale in zip(uasStandardForm, scales):
			yAxisTickMarks[verticalOffset] = '0'
			yAxisTickMarks[verticalOffset + 1] = '1'
			
			x = numpy.arange(0.0, dt * len(U), dt)
			assert(len(x) == len(U))
			plotLinesGrayBlack(x, numpy.array(U) + verticalOffset)
			verticalOffset += 2.0+2*visual_buffer
	
		ax = plt.gca()
		ax.yaxis.set_major_locator(plt.FixedLocator( yAxisTickMarks.keys() ))
		class TTFormatter(plt.Formatter):
			def __call__(self, x, pos=None):
				try:
					return yAxisTickMarks[x]
				except KeyError:
					return ''
				
		ax.yaxis.set_major_formatter(TTFormatter())
	
		ax = plt.gca()
		for tick in ax.xaxis.get_major_ticks():
			tick.label1.set_fontsize(tex_fontsize)
		for tick in ax.yaxis.get_major_ticks():
			tick.label1.set_fontsize(tex_fontsize)

		plt.show()

elif library == 'Gnuplot':
	def plotxy(x, y, title, xlabel, ylabel):
		xlabel = xlabel.replace('\\', '')
		xlabel = xlabel.replace('$', '')
		ylabel = ylabel.replace('\\', '')
		ylabel = ylabel.replace('$', '')
		g = Gnuplot.Gnuplot()
		g('set terminal x11')
		g('set title ' + '"' + title + '"')
		g('set xlabel ' + '"' + xlabel + '"')
		g('set ylabel ' + '"' + ylabel + '"')
		D = Gnuplot.Data(x, y, with_='linespoints')
		g.plot(D)
		return g

	def plotxy_hline(x, y, title, xlabel, ylabel, hlinepos):
		xlabel = xlabel.replace('\\', '')
		xlabel = xlabel.replace('$', '')
		ylabel = ylabel.replace('\\', '')
		ylabel = ylabel.replace('$', '')
		g = Gnuplot.Gnuplot()
		g('set terminal x11')
		g('set title ' + '"' + title + '"')
		g('set xlabel ' + '"' + xlabel + '"')
		g('set ylabel ' + '"' + ylabel + '"')
		D = Gnuplot.Data(x, y, with_='linespoints')
		E = Gnuplot.Data([x[0], x[-1]], [hlinepos, hlinepos], with_='linespoints')
		g.plot(D)
		return g	
	def humanTTturnrecord(labels, uasStandardForm, dt):
		for i in range(len(labels)): 
			labels[i] = labels[i].replace('\\', '')
			labels[i] = labels[i].replace('$', '')
		g = Gnuplot.Gnuplot()
		g('set terminal x11')
		x = numpy.arange(0.0, dt * len(uasStandardForm[0]), dt)
		A = Gnuplot.Data(x, uasStandardForm[0], with_='linespoints')
		B = Gnuplot.Data(x, uasStandardForm[1], with_='linespoints')
		C = Gnuplot.Data(x, uasStandardForm[2], with_='linespoints')
		D = Gnuplot.Data(x, uasStandardForm[3], with_='linespoints')		
		g('set multiplot')
		g('set size 1,0.25')
		g('set origin 0.0,0.75')
		g('set ylabel ' + '"' + labels[3] + '"')		
		g('set title ' + '"Usage attempt sequences for four speakers"')
		g.plot(D)
		g('set origin 0.0,0.5')
		g('set ylabel ' + '"' + labels[2] + '"')		
		g('unset title')		
		g.plot(C)
		g('set origin 0.0,0.25')
		g('set ylabel ' + '"' + labels[1] + '"')		
		g.plot(B)
		g('set origin 0.0,0.0')
		g('set ylabel ' + '"' + labels[0] + '"')		
		g('set xlabel ' + '"t (seconds)"')
		g.plot(A)

		g('unset multiplot')
		
		return g	