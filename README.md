figplotter
==========

Plotting infrastructure for Python using matplotlib

Install
-------

You can easily install figplotter using [pip](https://pypi.python.org/pypi/pip).

In your home directory:
```
pip install figplotter --user
```

In the system (requires superuser privileges):
```
sudo pip install figplotter
```

Example
-------

This is the code to generate a figure with two-level clustering using figplotter:
```python
from figplotter.utils import Parameter as P, clusterize
from figplotter.plot import figure, cluster_series_2
# We can set the properties of the bars with bar-granularity. All properties
# offered by matplotlib are supported. Bars are selected by using data
# identifiers. In a two-level clustering figure, three fields are specified:
# cluster_level1::cluster_level2::series.
# Wildcards can be used in any field to select groups of bars.
style_series = {
    '*::*::Read' : { 'bar::color' : 'b' },
    '*::*::Write': { 'bar::color' : 'g' },
    'PCIe 3.0::remote::*' : { 'bar::linewidth': 5   }
}
# We can also set the axis properties. In a two-level clustering figure the
# properties of the ticks and labels can be configured independently for the
# two levels of clusters (tick/ticklabel and major_tick/major_ticklabel).
style_axis = {
    '*': { 'tick::direction'      : 'inout',
           'major_tick::direction': 'out' },
    'x': { 'major_tick::length'   : 20,
           'major_tick::top'      : False,
           'major_ticklabel::y'   : -0.05 }
}
# Figures/axes are created just like in matplotlib
fig = figure()
ax = fig.add_subplot(111)

read  = [1, 2,   4,    5]
write = [2, 3, 3.5, 3.75]
clusters_1 = [ 'local', 'remote' ]
clusters_2 = [ 'PCIe 2.0', 'PCIe 3.0' ]
# Helper functions are provided to reshape data as expected by the plotting
# functions
data = clusterize({ 'Read': read, 'Write': write}, [clusters_2, clusters_1])

cluster_series_2(ax,
                 data,
                 [clusters_2, clusters_1],
                 ylim = (0, 4.5),
                 style_series = style_series,
                 style_axis = style_axis)

fig.show()
```
![two-level clustering](https://raw.githubusercontent.com/wiki/javier-cabezas/figplotter/images/cluster.png)
