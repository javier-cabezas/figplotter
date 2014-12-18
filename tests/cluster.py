import matplotlib
import matplotlib.pyplot as plt

import figplotter

from figplotter.utils import Parameter as P, clusterize
from figplotter.plot import figure, cluster_series

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
                   clusters,
                   bar_params = {
                       'color' : P({
                           'Read': 'b',
                           'Write': 'g',
                       })
                   })
    fig.show()

def figure_simple_clusterize():
    fig = figure()
    ax = fig.add_subplot(111)
    read  = [1, 2,   4,    5]
    write = [2, 3, 3.5, 3.75]

    clusters = [ 'local', 'remote', 'copy', 'peak' ]
    series = clusterize({'Read': read, 'Write': write}, [clusters])

    cluster_series(ax,
                   series,
                   clusters,
                   bar_params = {
                       'color' : P({
                           'Read': 'b',
                           'Write': 'g',
                       })
                   })
    fig.show()


figure_simple_cluster()
figure_simple_clusterize()

plt.show()
