'''
Created on Jan 19, 2015

@author: Javier Cabezas <javier.cabezas@gmail.com>
'''

import matplotlib
import matplotlib.pyplot as plt

from . import defaults
from . import info
from . import plotter
from . import plot

plot_series      = plot.plot_series
bar_series       = plot.bar_series
cluster_series   = plot.cluster_series
cluster_series_2 = plot.cluster_series_2


for func, params in plotter.PLOTTER_FUNCS.items():
    defaults.register_function(func, params)


def figure():
    return plt.figure(FigureClass=info.Figure)
