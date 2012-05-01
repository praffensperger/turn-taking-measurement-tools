# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Turn-Taking Measurement Tools v0.1 
#
# lineplot.py
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

#Python 2.6.4
import cPickle
import os

import numpy

try:
	import Gnuplot
	import matplotlib #Version 0.99.1.1
	import matplotlib.pyplot as plt
except ImportError:
	import warnings
	warnings.warn("Greetings grasshopper, you're trying to run a script on a platform that's missing key librarys for graphing. Don't worry unless you're actually gonna try and create a graph!")
except RuntimeError as e:
	print "Caught RuntimeError:", e
	print "Grasshopper, maybe you've SSH'd into a computer and you don't have a GUI..."

from textualsymbols import USAGE_ATTEMPT_SEQUENCE_SYMBOL

def getTurnTakingMeansAndStds():
	import warnings
	warnings.warn("There may be booboos here, grasshopper!")
	
	tt_means_stds_filename = "tt_means_stds.pickle"
	file = open(tt_means_stds_filename, 'r')
	tau_x = cPickle.load(file)
	
	sigmas = []
	thetas = []	
	rs = []
	for ts in tau_x:
		r, t, s = ts
		sigmas.append(s)
		thetas.append(t)
		rs.append(r)
	return rs, thetas, sigmas

def quickplot(x, title=''):
	g = Gnuplot.Gnuplot()
	g('set terminal x11')
	D = Gnuplot.Data(x, with_='linespoints')
	g('set title "' + title + '"')
	g.plot(D)
	return g
	
def GPlotXY(x, y, title=''):
	g = Gnuplot.Gnuplot()
	g('set terminal x11')
	g('set title ' + '"' + title + '"')
	D = Gnuplot.Data(x, y, with_='linespoints')
	g.plot(D)
	return  g	

def lineplot_dipaolo_V_vs_t(V, x, 	xlabel, ylabel, filename, figsize = None):
	#title = r"Mean $\tau\tau(t, r)$ over time against resolution, $r$"
	#xlabel = r'$r$'
	#ylabel = r'Mean $\tau\tau(t, r)$'
	contour_fontsize = 17
	tex_fontsize = 18
	title_fontsize = 24
	axis_label_fontsize = 20
	
	matplotlib.rc('text', usetex=True)
	matplotlib.rc('font', family='serif')
	
	matplotlib.rcParams['xtick.direction'] = 'out'
	matplotlib.rcParams['ytick.direction'] = 'out'
	
	plt.figure(figsize=figsize)
	
	plt.plot(x, numpy.array(V[0]), color='black', linestyle='--')
	plt.plot(x, numpy.array(V[1]), color='black', linestyle='-')
	#plt.plot([277.0, 277.0], [0, 7], color='black', linestyle='-')
	#plt.plot([450.0, 450.0], [0, 7], color='black', linestyle='-')
	#plt.plot([581.0, 581.0], [0, 7], color='black', linestyle='-')
	

	#plt.title(title, fontsize=title_fontsize)
	plt.xlabel(xlabel, fontsize=axis_label_fontsize)
	plt.ylabel(ylabel, fontsize=axis_label_fontsize)
	
	#plt.plot(0.5, 0.5, color='black', marker='+')
	#plt.text(0.51, 0.51, '0.5', fontsize=contour_fontsize)
	
	#axis_ranges = plt.axis()
	#plt.axis([axis_ranges[0], axis_ranges[1], 0.0, 1.0])

	tt_axes(tex_fontsize)

	save_and_display(filename)	

def multidotplot(x_star, y_star, x_plus, y_plus, x_cross, y_cross, xlabel, ylabel, filename):

	tex_fontsize = 18
	title_fontsize = 24
	axis_label_fontsize = 20
	
	matplotlib.rc('text', usetex=True)
	matplotlib.rc('font', family='serif')
	
	matplotlib.rcParams['xtick.direction'] = 'out'
	matplotlib.rcParams['ytick.direction'] = 'out'
	
	fig = plt.figure()
	markersize = 5.0
	color = 'black'
	plt.plot(x_star, y_star, '.', color=color, markersize=markersize)
	plt.plot(x_plus, y_plus, '+', color=color, markersize=markersize)
	plt.plot(x_cross, y_cross, 'x', color=color, markersize=markersize)

	#plt.xlabel(xlabel, fontsize=axis_label_fontsize)
	#plt.ylabel(ylabel, fontsize=axis_label_fontsize)
	
	#for tick in ax.xaxis.get_major_ticks():
	#	tick.label1.set_fontsize(tex_fontsize)
	#for tick in ax.yaxis.get_major_ticks():
	#	tick.label1.set_fontsize(tex_fontsize)
	
	#plt.plot(0.5, 0.5, color='black', marker='+')
	#plt.text(0.51, 0.51, '0.5', fontsize=contour_fontsize)
	plt.axes().set_aspect(1, adjustable='box')#, 'datalim')
	plt.xticks([]); plt.yticks([])
	#plt.axes().set_visible(False)
	#import pdb; pdb.set_trace()

	plt.axis("off")

	#import matplotlib.axes as ax
	#for direction in ["left", "right", "bottom", "top"]:
	#	fig.axis[direction].set_visible(False)


	
	#
	#plt.axis([axis_ranges[0], axis_ranges[1], 0.0, 1.0])

	tt_axes(tex_fontsize)

	save_and_display(filename)

def dotplot(x, y, xlabel, ylabel, filename):
	tex_fontsize = 18
	title_fontsize = 24
	axis_label_fontsize = 20
	
	matplotlib.rc('text', usetex=True)
	matplotlib.rc('font', family='serif')
	
	matplotlib.rcParams['xtick.direction'] = 'out'
	matplotlib.rcParams['ytick.direction'] = 'out'
	
	plt.figure()
	
	plt.plot(x, y, '-', color='black')

	plt.xlabel(xlabel, fontsize=axis_label_fontsize)
	plt.ylabel(ylabel, fontsize=axis_label_fontsize)
	
	#for tick in ax.xaxis.get_major_ticks():
	#	tick.label1.set_fontsize(tex_fontsize)
	#for tick in ax.yaxis.get_major_ticks():
	#	tick.label1.set_fontsize(tex_fontsize)
	
	#plt.plot(0.5, 0.5, color='black', marker='+')
	#plt.text(0.51, 0.51, '0.5', fontsize=contour_fontsize)
	#plt.axes().set_aspect('equal')#, 'datalim')
	
	#axis_ranges = plt.axis()
	#plt.axis([axis_ranges[0], axis_ranges[1], 0.0, 1.0])

	tt_axes(tex_fontsize)

	save_and_display(filename)

def lineplot(x, y, title, xlabel, ylabel, filename, verticalConstructionLine=None):
	#title = r"Mean $\tau\tau(t, r)$ over time against resolution, $r$"
	#xlabel = r'$r$'
	#ylabel = r'Mean $\tau\tau(t, r)$'
	contour_fontsize = 17
	tex_fontsize = 18
	title_fontsize = 24
	axis_label_fontsize = 20
	
	matplotlib.rc('text', usetex=True)
	matplotlib.rc('font', family='serif')
	
	matplotlib.rcParams['xtick.direction'] = 'out'
	matplotlib.rcParams['ytick.direction'] = 'out'
	
	plt.figure()
	
	plt.plot(x, y, color='black')
	
	do_verticalConstructionLines(verticalConstructionLine)
	
	#plt.plot(resolutions, sigmas, color='gray')

	#plt.title(title, fontsize=title_fontsize)
	plt.xlabel(xlabel, fontsize=axis_label_fontsize)
	plt.ylabel(ylabel, fontsize=axis_label_fontsize)
	
	#for tick in ax.xaxis.get_major_ticks():
	#	tick.label1.set_fontsize(tex_fontsize)
	#for tick in ax.yaxis.get_major_ticks():
	#	tick.label1.set_fontsize(tex_fontsize)
	
	#plt.plot(0.5, 0.5, color='black', marker='+')
	#plt.text(0.51, 0.51, '0.5', fontsize=contour_fontsize)
	#plt.axes().set_aspect('equal')#, 'datalim')
	
	#axis_ranges = plt.axis()
	#plt.axis([axis_ranges[0], axis_ranges[1], 0.0, 1.0])

	tt_axes(tex_fontsize)

	save_and_display(filename)	

def lineplotmulti(x, ys, xlabel, ylabels, filename, ylimits):
	tex_fontsize = 18
	title_fontsize = 24
	axis_label_fontsize = 20
	
	matplotlib.rc('text', usetex=True)
	matplotlib.rc('font', family='serif')
	
	matplotlib.rcParams['xtick.direction'] = 'out'
	matplotlib.rcParams['ytick.direction'] = 'out'
	
	plt.figure(figsize=(8, 6))
	
	for i, y, ylabel in zip(range(len(ys)), ys, ylabels):
		plt.subplot(100 * len(ys) + 11 + i)
		plt.plot(x, y, color='black')
		plt.ylabel(ylabel, fontsize=axis_label_fontsize)
		axis_ranges = plt.axis()
		plt.axis([axis_ranges[0], axis_ranges[1], 0.0, ylimits[i]]) #Limits y axis to [0, 1]
	
	#plt.plot(resolutions, sigmas, color='gray')

	#plt.title(title, fontsize=title_fontsize)
	plt.xlabel(xlabel, fontsize=axis_label_fontsize)
	
	
	#for tick in ax.xaxis.get_major_ticks():
	#	tick.label1.set_fontsize(tex_fontsize)
	#for tick in ax.yaxis.get_major_ticks():
	#	tick.label1.set_fontsize(tex_fontsize)
	
	#plt.plot(0.5, 0.5, color='black', marker='+')
	#plt.text(0.51, 0.51, '0.5', fontsize=contour_fontsize)
	#plt.axes().set_aspect('equal')#, 'datalim')
	
	#

	tt_axes(tex_fontsize)

	save_and_display(filename)	

def lineplot_tt_vs_threshold(x, y, xlabel, ylabel, filename, dash_line_level):
	#title = r"Mean $\tau\tau(t, r)$ over time against resolution, $r$"
	#xlabel = r'$r$'
	#ylabel = r'Mean $\tau\tau(t, r)$'
	contour_fontsize = 17
	tex_fontsize = 18
	title_fontsize = 24
	axis_label_fontsize = 20
	
	matplotlib.rc('text', usetex=True)
	matplotlib.rc('font', family='serif')
	
	matplotlib.rcParams['xtick.direction'] = 'out'
	matplotlib.rcParams['ytick.direction'] = 'out'
	
	plt.figure(figsize=(8, 4))
	
	pos_left = 0.12
	pos_bottom = 0.2
	pos_width = 0.83
	pos_height = 0.7
	ax = plt.axes([pos_left, pos_bottom, pos_width, pos_height])
	
	plt.plot(x, y, color='black')
	rtt_line = plt.plot(x, [dash_line_level]*len(x), linestyle='--', color='black')
	#plt.plot(resolutions, sigmas, color='gray')

	axis_ranges = plt.axis()
	plt.axis([axis_ranges[0], axis_ranges[1], 0.0, 1.0])

	#plt.title(title, fontsize=title_fontsize)
	plt.xlabel(xlabel, fontsize=axis_label_fontsize)
	plt.ylabel(ylabel, fontsize=axis_label_fontsize)
	
	for tick in ax.xaxis.get_major_ticks():
		tick.label1.set_fontsize(tex_fontsize)
	for tick in ax.yaxis.get_major_ticks():
		tick.label1.set_fontsize(tex_fontsize)
	
	#plt.plot(0.5, 0.5, color='black', marker='+')
	#plt.text(0.51, 0.51, '0.5', fontsize=contour_fontsize)
	#plt.axes().set_aspect('equal')#, 'datalim')
	
	#axis_ranges = plt.axis()
	#plt.axis([axis_ranges[0], axis_ranges[1], 0.0, 1.0])

	tt_axes(tex_fontsize)

	save_and_display(filename)

def lineplot_tt_over_time_multiple(xs, ys, xlabel, ylabel, filename):
	contour_fontsize = 17
	tex_fontsize = 18
	axis_label_fontsize = 20
	
	matplotlib.rc('text', usetex=True)
	matplotlib.rc('font', family='serif')
	
	matplotlib.rcParams['xtick.direction'] = 'out'
	matplotlib.rcParams['ytick.direction'] = 'out'
	
	plt.figure(figsize=(8, 3.5))
	
	pos_left = 0.12
	pos_bottom = 0.2
	pos_width = 0.83
	pos_height = 0.7
	plt.axes([pos_left, pos_bottom, pos_width, pos_height])
	for x, y, i in zip(xs, ys, range(len(xs))):
		#plt.plot(x, [dashed_line_level]*len(x), linestyle='--', color='black')
		plt.plot(x, y, linestyle=['-', ':', '--'][i], color='black')

	plt.xlabel(xlabel, fontsize=axis_label_fontsize)
	plt.ylabel(ylabel, fontsize=axis_label_fontsize)
	
	axis_ranges = plt.axis()
	plt.axis([axis_ranges[0], axis_ranges[1], 0.0, 1.0])


	tt_axes(tex_fontsize)

	save_and_display(filename)

def lineplot_tt_over_time(x, y, title, xlabel, ylabel, filename, dashed_line_level, xmax=None):
	#title = r"Mean $\tau\tau(t, r)$ over time against resolution, $r$"
	#xlabel = r'$r$'
	#ylabel = r'Mean $\tau\tau(t, r)$'
	contour_fontsize = 17
	tex_fontsize = 18
	title_fontsize = 24
	axis_label_fontsize = 20
	
	matplotlib.rc('text', usetex=True)
	matplotlib.rc('font', family='serif')
	
	matplotlib.rcParams['xtick.direction'] = 'out'
	matplotlib.rcParams['ytick.direction'] = 'out'
	
	plt.figure(figsize=(8, 3.5))
	
	pos_left = 0.12
	pos_bottom = 0.2
	pos_width = 0.83
	pos_height = 0.7
	plt.axes([pos_left, pos_bottom, pos_width, pos_height])
	plt.plot(x, [dashed_line_level]*len(x), linestyle='--', color='black')
	plt.plot(x, y, color='black')
	#plt.plot(resolutions, sigmas, color='gray')

	#plt.title(title, fontsize=title_fontsize)
	plt.xlabel(xlabel, fontsize=axis_label_fontsize)
	plt.ylabel(ylabel, fontsize=axis_label_fontsize)
	
	#plt.plot(0.5, 0.5, color='black', marker='+')
	#plt.text(0.51, 0.51, '0.5', fontsize=contour_fontsize)
	#plt.axes().set_aspect('equal')#, 'datalim')
	
	axis_ranges = plt.axis()
	if xmax is None:
		plt.axis([axis_ranges[0], axis_ranges[1], 0.0, 1.0])
	else:
		plt.axis([axis_ranges[0], xmax, 0.0, 1.0])

	tt_axes(tex_fontsize)

	save_and_display(filename)	

def tt_plot_setup():
	matplotlib.rc('text', usetex=True)
	matplotlib.rc('font', family='serif')
	
	matplotlib.rcParams['xtick.direction'] = 'out'
	matplotlib.rcParams['ytick.direction'] = 'out'
	
	plt.figure(figsize=(8, 3.5))
	
	pos_left = 0.17
	pos_bottom = 0.2
	pos_width = 0.79
	pos_height = 0.65
	plt.axes([pos_left, pos_bottom, pos_width, pos_height])

def tt_axes_r_scale(r, range_):
	ax = plt.gca()
	ax.xaxis.set_major_locator(plt.FixedLocator(range(0, range_, r*2)))
	
def tt_axes(tex_fontsize):
	ax = plt.gca()
	for tick in ax.xaxis.get_major_ticks():
		tick.label1.set_fontsize(tex_fontsize)
	for tick in ax.yaxis.get_major_ticks():
		tick.label1.set_fontsize(tex_fontsize)

def save_and_display(filename, dpi=None):
	print "Saving graph..."
	if dpi is not None:
		plt.savefig(filename) #"dipaolo_tautau(t,r)_vs_r_plot.pdf") 
	else:
		plt.savefig(filename, dpi=dpi)
	print "Showing graph..."
	plt.show()
	print "Done!"

def lineplot_tt_f_e_over_time(x, turntaking, efficiency, fairness, title, xlabel, ylabel, filename, r):
	#title = r"Mean $\tau\tau(t, r)$ over time against resolution, $r$"
	#xlabel = r'$r$'
	#ylabel = r'Mean $\tau\tau(t, r)$'
	contour_fontsize = 17
	tex_fontsize = 18
	title_fontsize = 24
	axis_label_fontsize = 20
	
	tt_plot_setup()
	
	rtt_line = plt.plot(x, [0.5]*len(x), linestyle='--', color='black', #'0.65', 
		label=r'$E\big[\tau\tau(t, ' + str(r) + r')\big]$ for random agents')
	tt_line = plt.plot(x, turntaking, '-', color='black', 
		label=r'$\tau\tau(t, ' + str(r) + ')$')
	#e_line = plt.plot(x, efficiency, '--', color='black', 
	#	label=r'$\mathit{efficiency}(t, ' + str(r) + ')$')
	#f_line = plt.plot(x, fairness, ':', color='black', 
	#	label=r'$fairness(t, ' + str(r) + ')$')
	
	#plt.plot(resolutions, sigmas, color='gray')

	#plt.legend(loc='lower right')

	##plt.title(title, fontsize=title_fontsize)
	plt.xlabel(xlabel, fontsize=axis_label_fontsize)
	plt.ylabel(ylabel, fontsize=axis_label_fontsize)
	
	#plt.plot(0.5, 0.5, color='black', marker='+')
	#plt.text(0.51, 0.51, '0.5', fontsize=contour_fontsize)
	#plt.axes().set_aspect('equal')#, 'datalim')
	
	#axis_ranges = plt.axis()
	#plt.axis([axis_ranges[0], axis_ranges[1], 0.0, 1.0])
	
	tt_axes_r_scale(r, len(x))
	#minorticks_on()

	tt_axes(tex_fontsize)

	save_and_display(filename)	

def do_verticalConstructionLines(verticalConstructionLine):
	if verticalConstructionLine is not None:
		r = verticalConstructionLine
		step = r/2.0
		for x in [r + step*x for x in range(7)]:
			print "Construction line at", x
			plt.arrow(x, 0.0, 0.0, 1.0, color='black')


def lineplot_meantau(x, thetas, sigmas, title, xlabel, ylabel, filename, verticalConstructionLine=None, showStd=False, resolutionDivisionFactor=1):
	#title = r"Mean $\tau\tau(t, r)$ over time against resolution, $r$"
	#xlabel = r'$r$'
	#ylabel = r'Mean $\tau\tau(t, r)$'
	contour_fontsize = 17
	tex_fontsize = 18
	title_fontsize = 24
	axis_label_fontsize = 20
	
	matplotlib.rc('text', usetex=True)
	matplotlib.rc('font', family='serif')
	
	matplotlib.rcParams['xtick.direction'] = 'out'
	matplotlib.rcParams['ytick.direction'] = 'out'
	
	#plt.figure()
	plt.figure(figsize=(10, 5))

	plt.xlabel(xlabel, fontsize=axis_label_fontsize)
	plt.ylabel(ylabel, fontsize=axis_label_fontsize)

	if showStd:
		plt.plot(numpy.array(x)/resolutionDivisionFactor, sigmas, color='0.65')
	#plt.plot(x, numpy.array(thetas) + numpy.array(sigmas), color='0.65')	
	#plt.plot(x, numpy.array(thetas) - numpy.array(sigmas), color='0.65')	
	plt.plot(numpy.array(x)/resolutionDivisionFactor, thetas, color='black')
	
	do_verticalConstructionLines(verticalConstructionLine)

	#plt.plot(resolutions, sigmas, color='gray')

	#plt.title(title, fontsize=title_fontsize)

	
	#plt.plot(0.5, 0.5, color='black', marker='+')
	#plt.text(0.51, 0.51, '0.5', fontsize=contour_fontsize)
	#plt.axes().set_aspect('equal')#, 'datalim')
	
	axis_ranges = plt.axis()
	plt.axis([axis_ranges[0], axis_ranges[1], 0.0, 1.0])

	tt_axes(tex_fontsize)

	save_and_display(filename)	
	
def boxPlot(distributions, positions, xlabel, ylabel, ylim, filename=None, generationLabels=False,  whis=1000):
	tex_fontsize = 18
	title_fontsize = 24
	axis_label_fontsize = 20
	
	matplotlib.rc('text', usetex=True)
	matplotlib.rc('font', family='serif')
	
	matplotlib.rcParams['xtick.direction'] = 'out'
	matplotlib.rcParams['ytick.direction'] = 'out'
	
	plt.figure()
	lines = plt.boxplot(distributions, notch=0, sym='b+', positions=positions, whis=whis)
	for line in lines:
		for l in lines[line]:
			if str(l.get_color()) == 'r': #The median is usually coloured red
				l.set_color('0.0')
				l.set_linewidth(2.0)
			else:
				l.set_color('0.0')
				l.set_linewidth(1.0)

	plt.ylim(ylim[0], ylim[1])
	
	if generationLabels:
		ax = plt.gca()
		#ax.yaxis.set_major_locator(plt.FixedLocator([0.0, 1.0, U2_offset, U2_offset + 1.0]))
		class TTFormatter(plt.Formatter):
			def __call__(self, x, pos=None):
				if (x == 1):
					return '3000'
				if (x == 2):
					return '5000'
				if (x == 3):
					return '8000'
				else:
					return str(x)
	
		ax.xaxis.set_major_formatter(TTFormatter())

	plt.xlabel(xlabel, fontsize=axis_label_fontsize)
	plt.ylabel(ylabel, fontsize=axis_label_fontsize)
	
	tt_axes(tex_fontsize)

	save_and_display(filename)
	
	
def plotLinesGrayBlack(x, y, linestyle='-'):
	plt.plot(x, y, color='0.65', linewidth=1, linestyle=linestyle)
	plt.plot(x, y, color='black', linewidth=0, marker=',', linestyle=linestyle)

def turnrecord_plot(x, U1, U2, title, xlabel, ylabel, filename):
	tex_fontsize = 18
	title_fontsize = 24
	axis_label_fontsize = 20
	
	tt_plot_setup()

	#plt.title(title, fontsize=title_fontsize)
	plt.xlabel(xlabel, fontsize=axis_label_fontsize)

	#plt.ylabel(r'$U_1(t)$ \quad \quad \quad \quad $U_2(t)$', fontsize=axis_label_fontsize)
	plt.text(-260.0, 1.7, r'$' + USAGE_ATTEMPT_SEQUENCE_SYMBOL + r'_1(t)$', fontsize=axis_label_fontsize)
	plt.text(-260.0, 0.4, r'$' + USAGE_ATTEMPT_SEQUENCE_SYMBOL + r'_2(t)$', fontsize=axis_label_fontsize)

	visual_buffer = 0.2

	plotLinesGrayBlack(x, U1)
	U2_offset = 1.0+2*visual_buffer
	plotLinesGrayBlack(x, numpy.array(U2) + U2_offset)

	ax = plt.gca()
	ax.yaxis.set_major_locator(plt.FixedLocator([0.0, 1.0, U2_offset, U2_offset + 1.0]))
	class TTFormatter(plt.Formatter):
		def __call__(self, x, pos=None):
			if (x == 0.0):
				return '0'
			if (x == 1.0):
				return '1'
			if (x == U2_offset):
				return '0'
			if (x == 1.0 + U2_offset):
				return '1'

	ax.yaxis.set_major_formatter(TTFormatter())

	plt.ylim(-visual_buffer, 1.0+visual_buffer+U2_offset)
	tt_axes(tex_fontsize)
	save_and_display(filename)	

def human_tt_results_plot(x, Us, taus, xlabel, ylabel, filename):
	tex_fontsize = 18
	tex_fontsize_small = 14
	axis_label_fontsize = 20
	
	matplotlib.rc('text', usetex=True)
	matplotlib.rc('font', family='serif')
	
	matplotlib.rcParams['xtick.direction'] = 'out'
	matplotlib.rcParams['ytick.direction'] = 'out'
	
	plt.figure(figsize=(8, 6))
	
	displaycollisions = False
	
	def turn_record_subplot(x, U, ylabel, linestyle):
		U1, U2 = U[0], U[1]
		
		def plotLinesGrayBlack2(x, y, linestyle='-'):
			#plt.plot(x, y, color='0.65', linewidth=1, linestyle=linestyle)
			plt.plot(x, y, color='black', linewidth=1, linestyle=linestyle)
		
		plotLinesGrayBlack2(x, numpy.array(U1)*2 + numpy.array(U2), linestyle=linestyle)
		
		ax = plt.gca()
		if displaycollisions:
			mark_locations = [0.0, 1.0, 2.0, 3.0]
			jumpamount = 3.0
		else:
			mark_locations = [0.0, 1.0, 2.0]
			jumpamount = 2.0
		ax.yaxis.set_major_locator(plt.FixedLocator(mark_locations))
		class TTFormatter(plt.Formatter):
			def __call__(self, x, pos=None):
				if (x == 0.0):
					return 'Unused'
				if (x == 1.0):
					return '$' + USAGE_ATTEMPT_SEQUENCE_SYMBOL + r'_1(t)$ only'
				if (x == 2.0):
					return '$' + USAGE_ATTEMPT_SEQUENCE_SYMBOL + r'_2(t)$ only'
				if (x == 3.0):
					return 'Collision'
	
		ax.yaxis.set_major_formatter(TTFormatter())
		visual_buffer = 0.1
		plt.ylim(-visual_buffer, jumpamount+visual_buffer)
		
		for tick in ax.yaxis.get_major_ticks():
			tick.label1.set_fontsize(tex_fontsize_small)
			
		plt.xticks(range(0, 1000, 200), [])
		#plt.ylabel(ylabel, fontsize=axis_label_fontsize)

	linestyles = ['-', ':', '--']

	def Shift(p):
		bb = p.get_position()
		bb.x0 += 0.025
		bb.x1 += 0.055
		p.set_position(bb)
		#import pdb; pdb.set_trace()
		#print p1.get_position()

	p1 = plt.subplot(611)#+100*plots)
	Shift(p1)
	turn_record_subplot(x, Us[0], '3000', linestyles[0])
	p2 = plt.subplot(612)#+100*plots)
	Shift(p2)
	turn_record_subplot(x, Us[1], '5000', linestyles[1])
	p3 = plt.subplot(613)#+100*plots)
	Shift(p3)
	turn_record_subplot(x, Us[2], '8000', linestyles[2])
	
	p4 = plt.subplot(212)
	Shift(p4)
	#pos_left = 0.12
	#pos_bottom = 0.2
	#pos_width = 0.83
	#pos_height = 0.7
	#plt.axes([pos_left, pos_bottom, pos_width, pos_height])
	for x, y, i in zip([x]*3, taus, range(3)):
		#plt.plot(x, [dashed_line_level]*len(x), linestyle='--', color='black')
		plt.plot(x, y[:-1], linestyle=linestyles[i], color='black', label=['3000\n$r=61$','5000\n$r=95$','8000\n$r=211$'][i])

	plt.ylabel(ylabel, fontsize=axis_label_fontsize)
	
	axis_ranges = plt.axis()
	plt.axis([axis_ranges[0], axis_ranges[1], 0.0, 1.0])

	plt.xlabel(xlabel, fontsize=axis_label_fontsize)
	ax = plt.gca()
	for tick in ax.xaxis.get_major_ticks():
		tick.label1.set_fontsize(tex_fontsize)
	for tick in ax.yaxis.get_major_ticks():
		tick.label1.set_fontsize(tex_fontsize)
		
	#Legend
	p4.legend(loc="lower right", ncol=3, shadow=False, title="Generation")


	save_and_display(filename)

def iizuka_results_plot(x, Us, taus, xlabel, ylabel, filename):
	tex_fontsize = 18
	tex_fontsize_small = 14
	axis_label_fontsize = 20
	
	matplotlib.rc('text', usetex=True)
	matplotlib.rc('font', family='serif')
	
	matplotlib.rcParams['xtick.direction'] = 'out'
	matplotlib.rcParams['ytick.direction'] = 'out'
	
	plt.figure(figsize=(8, 6))
	
	displaycollisions = False
	
	def turn_record_subplot(x, U, ylabel, linestyle):
		U1, U2 = U[0], U[1]
		
		def plotLinesGrayBlack2(x, y, linestyle='-'):
			#plt.plot(x, y, color='0.65', linewidth=1, linestyle=linestyle)
			plt.plot(x, y, color='black', linewidth=1, linestyle=linestyle)
		
		plotLinesGrayBlack2(x, numpy.array(U1)*2 + numpy.array(U2), linestyle=linestyle)
		
		ax = plt.gca()
		if displaycollisions:
			mark_locations = [0.0, 1.0, 2.0, 3.0]
			jumpamount = 3.0
		else:
			mark_locations = [0.0, 1.0, 2.0]
			jumpamount = 2.0
		ax.yaxis.set_major_locator(plt.FixedLocator(mark_locations))
		class TTFormatter(plt.Formatter):
			def __call__(self, x, pos=None):
				if (x == 0.0):
					return 'Unused'
				if (x == 1.0):
					return '$' + USAGE_ATTEMPT_SEQUENCE_SYMBOL + r'_1(t)$ only'
				if (x == 2.0):
					return '$' + USAGE_ATTEMPT_SEQUENCE_SYMBOL + r'_2(t)$ only'
				if (x == 3.0):
					return 'Collision'
	
		ax.yaxis.set_major_formatter(TTFormatter())
		visual_buffer = 0.1
		plt.ylim(-visual_buffer, jumpamount+visual_buffer)
		
		for tick in ax.yaxis.get_major_ticks():
			tick.label1.set_fontsize(tex_fontsize_small)
			
		plt.xticks(range(0, 1000, 200), [])
		#plt.ylabel(ylabel, fontsize=axis_label_fontsize)

	linestyles = ['-', ':', '--']

	def Shift(p):
		bb = p.get_position()
		bb.x0 += 0.025
		bb.x1 += 0.055
		p.set_position(bb)
		#import pdb; pdb.set_trace()
		#print p1.get_position()

	p1 = plt.subplot(611)#+100*plots)
	Shift(p1)
	turn_record_subplot(x, Us[0], '3000', linestyles[0])
	p2 = plt.subplot(612)#+100*plots)
	Shift(p2)
	turn_record_subplot(x, Us[1], '5000', linestyles[1])
	p3 = plt.subplot(613)#+100*plots)
	Shift(p3)
	turn_record_subplot(x, Us[2], '8000', linestyles[2])
	
	p4 = plt.subplot(212)
	Shift(p4)
	#pos_left = 0.12
	#pos_bottom = 0.2
	#pos_width = 0.83
	#pos_height = 0.7
	#plt.axes([pos_left, pos_bottom, pos_width, pos_height])
	for x, y, i in zip([x]*3, taus, range(3)):
		#plt.plot(x, [dashed_line_level]*len(x), linestyle='--', color='black')
		plt.plot(x, y[:-1], linestyle=linestyles[i], color='black', label=['3000\n$r=61$','5000\n$r=95$','8000\n$r=211$'][i])

	plt.ylabel(ylabel, fontsize=axis_label_fontsize)
	
	axis_ranges = plt.axis()
	plt.axis([axis_ranges[0], axis_ranges[1], 0.0, 1.0])

	plt.xlabel(xlabel, fontsize=axis_label_fontsize)
	ax = plt.gca()
	for tick in ax.xaxis.get_major_ticks():
		tick.label1.set_fontsize(tex_fontsize)
	for tick in ax.yaxis.get_major_ticks():
		tick.label1.set_fontsize(tex_fontsize)
		
	#Legend
	p4.legend(loc="lower right", ncol=3, shadow=False, title="Generation")


	save_and_display(filename)	

def turnresults_plot(x, U1, U2, title, xlabel, ylabel, filename, displaycollisions=True):
	tex_fontsize = 18
	title_fontsize = 24
	axis_label_fontsize = 20
	
	tt_plot_setup()

	#plt.title('Resource usage results', fontsize=title_fontsize)
	plt.xlabel(xlabel, fontsize=axis_label_fontsize)

	#plt.ylabel(r'y', fontsize=axis_label_fontsize)

	#plotSingleRecord(U1, r"$U_1(t)$", False)

	#plotSingleRecord(numpy.array(U2) + 2, r"$U_2(t)$", True)

	plotLinesGrayBlack(x, numpy.array(U1)*2 + numpy.array(U2))

	#mintime = 327
	#collisiontime = 450
	#maxtime = 672
	#plt.plot([mintime, mintime], [0, 7], color='black', linestyle='-')
	#plt.plot([collisiontime, collisiontime], [0, 7], color='black', linestyle='-')
	#plt.plot([maxtime, maxtime], [0, 7], color='black', linestyle='-')

	#plt.yticks([0.0, 1.0, 1.0])

	ax = plt.gca()
	if displaycollisions:
		mark_locations = [0.0, 1.0, 2.0, 3.0]
		jumpamount = 3.0
	else:
		mark_locations = [0.0, 1.0, 2.0]
		jumpamount = 2.0
	ax.yaxis.set_major_locator(plt.FixedLocator(mark_locations))
	class TTFormatter(plt.Formatter):
		def __call__(self, x, pos=None):
			if (x == 0.0):
				return 'Unused'
			if (x == 1.0):
				return '$' + USAGE_ATTEMPT_SEQUENCE_SYMBOL + r'_1(t)$ only'
			if (x == 2.0):
				return '$' + USAGE_ATTEMPT_SEQUENCE_SYMBOL + r'_2(t)$ only'
			if (x == 3.0):
				return 'Collision'

	ax.yaxis.set_major_formatter(TTFormatter())

	visual_buffer = 0.1

	
	plt.ylim(-visual_buffer, jumpamount+visual_buffer)
	
	for tick in ax.xaxis.get_major_ticks():
		tick.label1.set_fontsize(tex_fontsize)
	for tick in ax.yaxis.get_major_ticks():
		tick.label1.set_fontsize(tex_fontsize)

	#plt.plot(0.5, 0.5, color='black', marker='+')
	#plt.text(0.51, 0.51, '0.5', fontsize=contour_fontsize)
	#plt.axes().set_aspect('equal')#, 'datalim')
	
	#axis_ranges = plt.axis()
	#plt.axis([axis_ranges[0], axis_ranges[1], 0.0, 1.0])


	save_and_display(filename)	

def tt_dist_bargraph(ranges, counts, filename):
	matplotlib.rc('text', usetex=True)
	matplotlib.rc('font', family='serif')
	
	matplotlib.rcParams['xtick.direction'] = 'out'
	matplotlib.rcParams['ytick.direction'] = 'out'

	fig = plt.figure(figsize=(8, 4))

	pos_left = 0.1
	pos_bottom = 0.2
	pos_width = 0.87
	pos_height = 0.7
	ax = plt.axes([pos_left, pos_bottom, pos_width, pos_height])
	#ax = fig.add_subplot(111)	
	contour_fontsize = 17
	tex_fontsize = 18
	title_fontsize = 24
	axis_label_fontsize = 20
	
	
	plt.xlabel(r"$\tau\tau(t,r)$", fontsize=axis_label_fontsize)
	plt.ylabel(r"Occurrences", fontsize=axis_label_fontsize)
	
	tt_axes(tex_fontsize)
	
	# histogram our data with numpy
	binset = numpy.arange(0.0, 1.0, 1.0/nbins)
	n, bins = numpy.histogram(data, binset)
	print "Making a histogram with a total of ", n.sum(), "occurrences"
	
	# get the corners of the rectangles for the histogram
	left = numpy.array(bins[:-1])
	right = numpy.array(bins[1:])
	bottom = numpy.zeros(len(left))
	top = bottom + n
	
	# we need a (numrects x numsides x 2) numpy array for the path helper
	# function to build a compound path
	XY = numpy.array([[left,left,right,right], [bottom,top,top,bottom]]).T
	
	# get the Path object
	barpath = matplotlib.path.Path.make_compound_path_from_polys(XY)
	
	# make a patch out of it
	patch = matplotlib.patches.PathPatch(barpath, fill=False, hatch='///', edgecolor='black')
	ax.add_patch(patch)
	
	# update the view limits
	ax.set_xlim(0.0, 1.0)
	ax.set_ylim(0, 10000)
	
	for tick in ax.xaxis.get_major_ticks():
		tick.label1.set_fontsize(tex_fontsize)
	for tick in ax.yaxis.get_major_ticks():
		tick.label1.set_fontsize(tex_fontsize)
	
	save_and_display(filename)	

def quick_histogram(data, nbins, filename):
	matplotlib.rc('text', usetex=True)
	matplotlib.rc('font', family='serif')
	
	matplotlib.rcParams['xtick.direction'] = 'out'
	matplotlib.rcParams['ytick.direction'] = 'out'

	fig = plt.figure(figsize=(8, 4))

	pos_left = 0.1
	pos_bottom = 0.2
	pos_width = 0.87
	pos_height = 0.7
	ax = plt.axes([pos_left, pos_bottom, pos_width, pos_height])
	#ax = fig.add_subplot(111)	
	contour_fontsize = 17
	tex_fontsize = 18
	title_fontsize = 24
	axis_label_fontsize = 20
	
	
	plt.xlabel(r"x", fontsize=axis_label_fontsize)
	plt.ylabel(r"Occurrences", fontsize=axis_label_fontsize)
	
	tt_axes(tex_fontsize)
	
	# histogram our data with numpy
	binset = numpy.linspace(min(data), max(data), nbins)
	print "Top of histogram is at", max(data), " total number of bins is", nbins
	n, bins = numpy.histogram(data, binset)
	#import pdb; pdb.set_trace()
	print "Making a histogram with a total of ", n.sum(), "occurrences"
	
	# get the corners of the rectangles for the histogram
	left = numpy.array(bins[:-1])
	right = numpy.array(bins[1:])
	bottom = numpy.zeros(len(left))
	top = bottom + n
	
	# we need a (numrects x numsides x 2) numpy array for the path helper
	# function to build a compound path
	XY = numpy.array([[left,left,right,right], [bottom,top,top,bottom]]).T
	
	# get the Path object
	barpath = matplotlib.path.Path.make_compound_path_from_polys(XY)
	
	# make a patch out of it
	patch = matplotlib.patches.PathPatch(barpath, fill=False, hatch='///', edgecolor='black')
	ax.add_patch(patch)
	
	ax.set_xlim(min(data)-1, max(data)+1)
	ax.set_ylim(0, max(n))	
	
	for tick in ax.xaxis.get_major_ticks():
		tick.label1.set_fontsize(tex_fontsize)
	for tick in ax.yaxis.get_major_ticks():
		tick.label1.set_fontsize(tex_fontsize)
	
	save_and_display(filename)	
	
def tt_dist_histogram(data, nbins, filename):
	matplotlib.rc('text', usetex=True)
	matplotlib.rc('font', family='serif')
	
	matplotlib.rcParams['xtick.direction'] = 'out'
	matplotlib.rcParams['ytick.direction'] = 'out'

	fig = plt.figure(figsize=(8, 4))

	pos_left = 0.1
	pos_bottom = 0.2
	pos_width = 0.87
	pos_height = 0.7
	ax = plt.axes([pos_left, pos_bottom, pos_width, pos_height])
	#ax = fig.add_subplot(111)	
	contour_fontsize = 17
	tex_fontsize = 18
	title_fontsize = 24
	axis_label_fontsize = 20
	
	
	plt.xlabel(r"$\tau\tau(t,r)$", fontsize=axis_label_fontsize)
	plt.ylabel(r"Occurrences", fontsize=axis_label_fontsize)
	
	tt_axes(tex_fontsize)
	
	# histogram our data with numpy
	binset = numpy.arange(0.0, 1.0, 1.0/nbins)
	n, bins = numpy.histogram(data, binset)
	print "Making a histogram with a total of ", n.sum(), "occurrences"
	
	# get the corners of the rectangles for the histogram
	left = numpy.array(bins[:-1])
	right = numpy.array(bins[1:])
	bottom = numpy.zeros(len(left))
	top = bottom + n
	
	# we need a (numrects x numsides x 2) numpy array for the path helper
	# function to build a compound path
	XY = numpy.array([[left,left,right,right], [bottom,top,top,bottom]]).T
	
	# get the Path object
	barpath = matplotlib.path.Path.make_compound_path_from_polys(XY)
	
	# make a patch out of it
	patch = matplotlib.patches.PathPatch(barpath, fill=False, hatch='///', edgecolor='black')
	ax.add_patch(patch)
	
	# update the view limits
	ax.set_xlim(0.0, 1.0)
	ax.set_ylim(0, 10000)
	
	for tick in ax.xaxis.get_major_ticks():
		tick.label1.set_fontsize(tex_fontsize)
	for tick in ax.yaxis.get_major_ticks():
		tick.label1.set_fontsize(tex_fontsize)
	
	save_and_display(filename)	
	
def ThresholdResolutionVsTTContourPlot(x, y,  mean_tt, xlabel='', ylabel=''):
	matplotlib.rc('text', usetex=True)
	matplotlib.rc('font', family='serif')	
	
	X, Y = numpy.meshgrid(x, y)
	Z = numpy.array(mean_tt)
	assert(Z.size == len(x) * len(y) )
	#Z.shape = (len(x), len(y))
	
	contour_fontsize = 17
	tex_fontsize = 18
	title_fontsize = 24
	axis_label_fontsize = 20
	

	matplotlib.rcParams['xtick.direction'] = 'out'
	matplotlib.rcParams['ytick.direction'] = 'out'
	
	#matplotlib.rcParams['contour.negative_linestyle'] = 'solid' #Uncomment this line to make negative contours have solid lines

	fig = plt.figure(figsize=(8, 6))

	pos_left = 0.1
	pos_bottom = 0.13
	pos_width = 0.87
	pos_height = 0.83
	ax = plt.axes([pos_left, pos_bottom, pos_width, pos_height])	 
	
	contours = numpy.arange(0.0, 0.7, 0.1)#[0.1, 0.2, 0.3, 0.4, 0.5, 0.6]

	CS = plt.contour(X, Y, Z, contours,
					 colors='k', # negative contours will be dashed by default
					 )
	
	#
	clabels = plt.clabel(CS, fontsize=contour_fontsize, inline_spacing=-5, fmt='%1.1f')

	#clabels[0].set_position((200,5))
	#clabels[1].set_position((200,6))
	#clabels[2].set_position((200,7))
	#clabels[3].set_position((300,2))
	#clabels[4].set_position((100,3))
	
	#import pdb; pdb.set_trace()
	plt.xlabel(xlabel, fontsize=axis_label_fontsize)
	plt.ylabel(ylabel, fontsize=axis_label_fontsize)
	
	for tick in ax.xaxis.get_major_ticks():
		tick.label1.set_fontsize(tex_fontsize)
	for tick in ax.yaxis.get_major_ticks():
		tick.label1.set_fontsize(tex_fontsize)
	
	
	#plt.plot(0.5, 0.5, color='black', marker='+')
	#plt.text(0.51, 0.51, '0.5', fontsize=9)
	
	save_and_display('contour_plot_threshold_resolution_vs_mean_tt.pdf')



def humanTTturnrecord(labels, uasStandardForm, speakerWaveformPlotInformation, dt, dt_audio, filename):
#turnrecord_plot_multi(x, turnRecords, title, xlabel, filename):
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

	#plt.title(title, fontsize=title_fontsize)
	plt.xlabel('$t$ (seconds)', fontsize=axis_label_fontsize)

	#plt.ylabel(r'$U_1(t)$ \quad \quad \quad \quad $U_2(t)$', fontsize=axis_label_fontsize)
	plt.text(-11.5, 0.5, labels[0], fontsize=axis_label_fontsize, verticalalignment='center',)
	plt.text(-11.5, 3.1, labels[1], fontsize=axis_label_fontsize, verticalalignment='center',)
	plt.text(-11.5, 5.7, labels[2], fontsize=axis_label_fontsize, verticalalignment='center',)
	plt.text(-11.5, 8.3, labels[3], fontsize=axis_label_fontsize, verticalalignment='center',)
	
	visual_buffer = 0.3
	U2_offset = 1
	
	yAxisTickMarks = {}
	
	
	waveformOffset = 1.6
	verticalOffset = 0.0
	scales = [0.7, 0.5, 0.8, 0.7]
	for U, W, scale in zip(uasStandardForm, speakerWaveformPlotInformation, scales):
		waveformMax, waveformMin = W
		yAxisTickMarks[verticalOffset] = '0'
		yAxisTickMarks[verticalOffset + 1] = '1'
		
		x = numpy.arange(0.0, dt * len(U), dt)
		assert(len(x) == len(U))
		plotLinesGrayBlack(x, numpy.array(U) + verticalOffset)
		yAxisTickMarks[verticalOffset + waveformOffset] = ''
		subplotAudio(waveformMax*scale + waveformOffset + verticalOffset, 
					waveformMin*scale + waveformOffset + verticalOffset, dt_audio)
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

	# plt.ylim(-visual_buffer, 1.0+visual_buffer+U2_offset)
	tt_axes(tex_fontsize)
	#if filename[-3:] == 'png':
		#plt.set_dpi(450)
	save_and_display(filename, dpi=1200)	

def subplotAudio(waveformMax, waveformMin, dt):
	x = numpy.arange(0.0, dt * len(waveformMax), dt)
	assert(len(x) == len(waveformMax))
	
	plt.fill_between(x, waveformMax, waveformMin, color='black')

def plotAudio(waveformMax, waveformMin, samplingFrequency, filename):
	assert(len(waveformMax) == len(waveformMin))
	matplotlib.rc('text', usetex=True)
	matplotlib.rc('font', family='serif')
	
	matplotlib.rcParams['xtick.direction'] = 'out'
	matplotlib.rcParams['ytick.direction'] = 'out'
	
	fig = plt.figure()
	
	dt = 1.0 / samplingFrequency
	
	x = numpy.arange(0.0, dt * len(waveformMax), dt)
	assert(len(x) == len(waveformMax))
	
	plt.fill_between(x, waveformMax, waveformMin, color='black')
	
	axis_ranges = plt.axis()
	plt.axis([axis_ranges[0], axis_ranges[1], -1.0, 1.0]) #Limits y axis to [0, 1]

	
	save_and_display(filename)		
	
if __name__ == '__main__':
	rs, thetas, sigmas = getTurnTakingMeansAndStds()
	linePlot_thetas_w_sigma_error_bars(rs[:998], thetas[:998], sigmas[:998]) #only plot those resolutions below 1000