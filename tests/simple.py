'''
Created on Jan 19, 2015

@author: Javier Cabezas <javier.cabezas@gmail.com>
'''

import matplotlib.pyplot as plt

from figplotter.plot import figure, bar_series, plot_series


def figure_lines():
    fig = figure()
    ax = fig.add_subplot(111)

    plot_series(ax,
                { 'Read':  [1, 2,   4,    5],
                  'Write': [2, 3, 3.5, 3.75] })
    fig.show()


def figure_lines2():
    fig = figure()
    ax = fig.add_subplot(111)

    plot_series(ax,
                { 'Read':  [1, 2,   4,    5] },
                legend = False)
    plot_series(ax,
                { 'Write': [2, 3, 3.5, 3.75] })
    fig.show()


def figure_bars():
    fig = figure()
    ax = fig.add_subplot(111)

    bar_series(ax,
               { 'Read': [1, 2, 4, 5] })
    fig.show()


barstyle = {}
barstyle['*']     = { 'bar::linewidth' : 2 }
barstyle['Read']  = { 'bar::color'     : 'b' }
barstyle['Write'] = { 'bar::color'     : 'g' }

def figure_bars_stacked():
    fig = figure()
    ax = fig.add_subplot(111)

    bar_series(ax,
               { 'Read' : [1, 2,   4,    5],
                 'Write': [2, 3, 3.5, 3.75] },
               style_series = barstyle)
    fig.show()


linestyle = {'*' : {'plot::color' : 'r',
                    'plot::linewidth': 5 }}


def figure_hybrid():
    fig = figure()
    ax = fig.add_subplot(111)

    bar_series(ax,
               { 'Read' : [1, 2,   4,    5],
                 'Write': [2, 3, 3.5, 3.75] },
               style_series = barstyle)
    plot_series(ax,
                { 'Baseline': [1.75, 2.25, 3.25, 3.5] },
                style_series = linestyle)
    fig.show()


figure_lines()
figure_lines2()

figure_bars()
figure_bars_stacked()

figure_hybrid()

plt.show()
