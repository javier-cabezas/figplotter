import matplotlib
import matplotlib.pyplot as plt

from plot import *
import defaults
import plotter

for func, params in plotter.PLOTTER_FUNCS.items():
    defaults.register_fun(func, params)

def figure():
    return plt.figure(FigureClass=info.Figure)
