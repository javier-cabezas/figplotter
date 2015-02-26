figplotter
==========

Plotting infrastructure for Python using matplotlib

Example
-------

This is the code to generate a figure with two-level clustering using figplotter:
```python
from figplotter.utils import Parameter as P, clusterize
from figplotter.plot import figure, cluster_series, cluster_series_2

style_series_2 = {
    '*::*::Read' : { 'bar::color'    : 'b' },
    '*::*::Write': { 'bar::color'    : 'g' },
    'PCIe 3.0::remote::*' : { 'bar::linewidth': 5   }
}

style_axis = {
    '*': { 'tick::direction'      : 'inout',
           'major_tick::direction': 'out' },
    'x': { 'major_tick::length'   : 20,
           'major_tick::top'      : False,
           'major_ticklabel::y'   : -0.05 }
}

fig = figure()
ax = fig.add_subplot(111)
read  = [1, 2,   4,    5]
write = [2, 3, 3.5, 3.75]

clusters_1 = [ 'local', 'remote' ]
clusters_2 = [ 'PCIe 2.0', 'PCIe 3.0' ]
series = clusterize({ 'Read': read, 'Write': write}, [clusters_2, clusters_1])

cluster_series_2(ax,
                 series,
                 [clusters_2, clusters_1],
                 ylim = (0, 4.5),
                 style_series = style_series_2,
                 style_axis = style_axis)

fig.show()
```
![two-level clustering](https://raw.githubusercontent.com/wiki/javier-cabezas/figplotter/images/cluster.png)
