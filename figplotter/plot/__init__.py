'''
Created on Jan 19, 2015

@author: Javier Cabezas <javier.cabezas@gmail.com>
'''

import matplotlib
import matplotlib.pyplot as plt

from plot import plot_series, bar_series, cluster_series, cluster_series_2
import defaults
import info
import plotter

for func, params in plotter.PLOTTER_FUNCS.items():
    defaults.register_function(func, params)

def figure():
    return plt.figure(FigureClass=info.Figure)
