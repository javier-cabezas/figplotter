import matplotlib
import matplotlib.pyplot as plt

import figplotter

from figplotter.utils import Parameter as P
from figplotter.plot import figure, bar_series, line_series

def figure_lines():
    fig = figure()
    ax = fig.add_subplot(111)

    line_series(ax,
                { 'Read':  [1, 2,   4,    5],
                  'Write': [2, 3, 3.5, 3.75] })
    fig.show()


def figure_lines2():
    fig = figure()
    ax = fig.add_subplot(111)

    line_series(ax,
                { 'Read':  [1, 2,   4,    5] },
                legend = False)
    line_series(ax,
                { 'Write': [2, 3, 3.5, 3.75] })
    fig.show()

def figure_bars():
    fig = figure()
    ax = fig.add_subplot(111)

    bar_series(ax,
               { 'Read': [1, 2, 4, 5] })
    fig.show()

def figure_bars_stacked():
    fig = figure()
    ax = fig.add_subplot(111)

    bar_series(ax,
               { 'Read' : [1, 2,   4,    5],
                 'Write': [2, 3, 3.5, 3.75] },
               plot_params = {
                   'color' : P({ 'Read' : 'b',
                                 'Write': 'g'})
               })
    fig.show()

def figure_hybrid():
    fig = figure()
    ax = fig.add_subplot(111)

    bar_series(ax,
               { 'Read' : [1, 2,   4,    5],
                 'Write': [2, 3, 3.5, 3.75] },
               plot_params = {
                   'color' : P({ 'Read' : 'b',
                                 'Write': 'g'})
               })
    line_series(ax,
                { 'Baseline': [1.75, 2.25, 3.25, 3.5] },
                plot_params = { 'color' : 'r' })
    fig.show()

figure_lines()
figure_lines2()

figure_bars()
figure_bars_stacked()

figure_hybrid()

plt.show()
