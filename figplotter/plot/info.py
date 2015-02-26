import matplotlib.pyplot as plt

from matplotlib.figure import Figure as PLTFigure

from collections import OrderedDict

from .. import utils

class SeriesInfo(object):
    def __init__(self, id_):
        self.id_    = id_
        self.name   = None
        self.handle = None

    def set_legend_info(self, name, handle):
        self.name   = name
        self.handle = handle

    def set_points(self, x_values, y_values):
        self.x_values = x_values
        self.y_values = y_values

    def merge(self, series_info):
        assert self.name == series_info.name, 'Series name do not match'

        self.x_values.append(series_info.x_values)
        self.y_values.append(series_info.y_values)

    def __str__(self):
        s = "{0} = {1}: ".format(self.id_, self.name) + "{0}".format(', '.join(["(%.2f, %.2f)" % (float(x), float(y)) for x, y in zip(self.x_values, self.y_values)]))
        return s

class ClusterInfo(object):
    def __init__(self):
        self.cluster_names    = None
        self.cluster_x_values = None
        self.clusters = {}

    def set_clusters(self, names, x_values):
        self.cluster_names    = names
        self.cluster_x_values = x_values

        for name, x in zip(names, x_values):
            if name not in self.clusters.keys():
                self.clusters[name] = []

            self.clusters[name].append(x)

    def merge(self, cluster_info):
        self.cluster_names.append(cluster_info.cluster_names)
        self.cluster_x_values.append(cluster_info.cluster_x_values)

    def __str__(self):
        clusters = ['{0}: {1}'.format(name, ', '.join([ "%.2f" % v for v in self.clusters[name] ])) for name in list(OrderedDict.fromkeys(self.cluster_names)) ]
        s = ', '.join(clusters)
        return s


class AxisInfo(object):
    def __init__(self, ax, figure_info):
        self.ax          = ax
        self.figure_info = figure_info

        self.series       = {}
        self.series_order = []

        self.clusters = {}

    def add_series(self, id_, series_info):
        if id_ not in self.series.keys():
            self.series[id_] = series_info
        else:
            self.series[id_].merge(series_info)

    def set_series_order(self, series_order):
        for series in series_order:
            if series not in self.series_order:
                self.series_order.append(series)

    def set_clusters(self, cluster_info, level = 0):
        if level not in self.clusters.keys():
            self.clusters[level] = cluster_info
        else:
            self.clusters[level].merge(cluster_info)

    def legend(self, **legend_params):
        order = self.series_order
        if order is None:
            order = self.series.keys()

        handles = [ self.series[series].handle for series in order ]
        labels  = [ self.series[series].name for series in order ]

        self.ax.legend(handles, labels, **legend_params)

    def __str__(self):
        s = 'SERIES\n'
        order = self.series_order
        if self.series_order is None:
            order = self.series.keys()
        for series in order:
            s2 = "  > {0}\n".format(self.series[series])
            s += s2

        s += '\nCLUSTERS\n'
        for level, cluster_info in self.clusters.items():
            s2 = "  > Level {0}: {1}\n".format(level, cluster_info)
            s += s2

        return s

class Figure(PLTFigure):
    figure_index = 1

    def __init__(self, *args, **kwargs):
        name = kwargs.get('name', None)
        if name is not None:
            del kwargs[name]
            self.name = name
        else:
            self.name = 'figure{0}'.format(Figure.figure_index)
            Figure.figure_index += 1

        PLTFigure.__init__(self, *args, **kwargs)

        self.axes_   = {}
        self.series_ = {}

    def get_axis_info(self, ax):
        if ax not in self.axes_.keys():
            self.axes_[ax] = AxisInfo(ax, self)

        return self.axes_[ax]

    def add_axis(self, ax):
        if ax not in self.axes_.keys():
            self.axes_[ax] = AxisInfo(ax, self)

    def add_series(self, ax, id_, series_info):
        assert ax in self.axes_.keys(), 'Axis does not exist'

        if id_ not in self.series_.keys():
            self.series_[id_] = series_info
        else:
            self.series_[id_].merge(series_info)

    def add_subplot(self, *args, **kwargs):
        '''
        @param self: figure
        @param args: positional args for Figure.add_subplot
        @param kwargs: keyword args for Figure.add_subplot

        @return: new Axes object bound to figure
        '''
        ax = PLTFigure.add_subplot(self, *args, **kwargs)
        self.add_axis(ax)

        return ax

    def twinx(self, ax):
        ax2 = ax.twinx()
        self.add_axis(ax2)

        return ax2

    def close(self):
        plt.close(self)

    def show(self, warn=True):
        utils.message('Showing figure "%s"' % self.name)
        return PLTFigure.show(self, warn=warn)

    def savefig(self, *args, **kwargs):
        utils.message('Saving figure "%s" in "%s"' % (self.name, args[0]))
        PLTFigure.savefig(self, *args, **kwargs)

