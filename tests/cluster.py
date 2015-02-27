'''
Created on Jan 19, 2015

@author: Javier Cabezas <javier.cabezas@gmail.com>
'''

import matplotlib.pyplot as plt

from figplotter.utils import clusterize
from figplotter.plot import figure, cluster_series, cluster_series_2


style_series = {
    '*'       : { 'bar::color'    : 'r' },
    '*::Read' : { 'bar::color'    : 'b' },
    '*::Write': { 'bar::color'    : 'g' },
    'peak::*' : { 'bar::linewidth': 5   }
}


style_axis = {
    '*': { 'tick::direction'      : 'inout',
           'major_tick::direction': 'out' },
    'x': { 'major_tick::length'   : 20,
           'major_tick::top'      : False,
           'major_ticklabel::y'   : -0.05 }
}


def figure_simple_cluster():
    fig = figure()
    ax = fig.add_subplot(111)
    read  = [1, 2,   4,    5]
    write = [2, 3, 3.5, 3.75]

    clusters = [ 'local', 'remote', 'copy', 'peak' ]
    series = {}
    for i, cluster in enumerate(clusters):
        series[cluster] = {}

        series[cluster]['Read']  = read[i]
        series[cluster]['Write'] = write[i]

    cluster_series(ax,
                   series,
                   [ clusters ],
                   style_series = style_series,
                   style_axis = style_axis)

    fig.show()


def figure_simple_clusterize():
    fig = figure()
    ax = fig.add_subplot(111)
    read  = [1, 2,   4,    5]
    write = [2, 3, 3.5, 3.75]

    clusters = [ 'local', 'remote', 'copy', 'peak' ]
    series = clusterize({'Read': read, 'Write': write}, [ clusters ])

    cluster_series(ax,
                   series,
                   [ clusters ],
                   style_series = style_series,
                   style_axis = style_axis)

    fig.show()


style_series_2 = {
    '*::*::*'    : { 'bar::color'    : 'r' },
    '*::*::Read' : { 'bar::color'    : 'b' },
    '*::*::Write': { 'bar::color'    : 'g' },
    'PCIe 3.0::remote::*' : { 'bar::linewidth': 5   }
}


def figure_twolevel():
    fig = figure()
    ax = fig.add_subplot(111)
    read  = [1, 2,   4,    5]
    write = [2, 3, 3.5, 3.75]

    clusters_1 = [ 'PCIe 2.0', 'PCIe 3.0' ]
    clusters_2 = [ 'local', 'remote' ]
    series = {}
    for i, cluster1 in enumerate(clusters_1):
        series[cluster1] = {}

        for j, cluster2 in enumerate(clusters_2):
            series[cluster1][cluster2] = {}

            series[cluster1][cluster2]['Read']  = read[j + i * len(clusters_2)]
            series[cluster1][cluster2]['Write'] = write[j + i * len(clusters_2)]

    cluster_series_2(ax,
                     series,
                     [clusters_1, clusters_2],
                     ylim=(0,4.5),
                     style_series = style_series_2,
                     style_axis = style_axis)

    fig.show()


def figure_twolevel_clusterize():
    fig = figure()
    ax = fig.add_subplot(111)
    read  = [1, 2,   4,    5]
    write = [2, 3, 3.5, 3.75]

    clusters_1 = [ 'PCIe 2.0', 'PCIe 3.0' ]
    clusters_2 = [ 'local', 'remote' ]
    series = clusterize({ 'Read': read, 'Write': write}, [clusters_1, clusters_2])

    cluster_series_2(ax,
                     series,
                     [clusters_1, clusters_2],
                     ylim=(0,4.5),
                     style_series = style_series_2,
                     style_axis = style_axis)

    fig.show()


figure_simple_cluster()
figure_simple_clusterize()

figure_twolevel()
figure_twolevel_clusterize()

plt.show()
