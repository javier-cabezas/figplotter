import numpy as np
import types

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

from .. import utils
import defaults
import info
from plotter import plotter_func

def create_generators(params, elems):
    generators = {}
    for key, value in params.items():
        if not isinstance(value, types.FunctionType):
            fun = utils.generator(value)(elems)
        else:
            fun = value(elems)

        generators[key] = fun

    return generators

def instantiate_params(params, series):
    param_instances = {}

    for s in series:
        p = params.copy()
        for key, value in params.items():
            if isinstance(value, utils.Parameter):
                v = value.values[s]
            else:
                v = value

            p[key] = v

        param_instances[s] = p

    return param_instances

def next_generators(params, generators):
    next_params = params.copy()

    for name, value in generators.items():
        next_params[name] = next(value)

    return next_params

def simple_series(ax, series, names,
                  fun = 'line',
                  key_order   = None,
                  ticks       = None,
                  ticklabels  = None,
                  zoom_params = None,
                  offset      = 0,
                  plot_params = {},
                  overflow_params = {},
                  **kwargs):
    # Initialize param dictionaries and generators
    if fun == 'line':
        plot_params = defaults.get_defaults_fun('line_series', 'line', plot_params)
        plot_fun = ax.plot
    elif fun == 'bar':
        plot_params     = defaults.get_defaults_fun('bar_series', 'bar', plot_params)
        overflow_params = defaults.get_defaults_fun('bar_series', 'overflow', overflow_params)
        # TODO: Use overflow_params
        plot_fun = ax.bar

    if key_order is None:
        key_order = series.keys()

    info_order = key_order

    # Initialize generators
    plot_params_series = instantiate_params(plot_params, key_order)

    plot_params_all = {}

    axis_info = ax.figure.get_axis_info(ax)

    for key in key_order:
        if len(series[key]) > 1:
            x_values = series[key][1]
            y_values = series[key][0]
        else:
            y_values = series[key]

            if ticks is None:
                x_values = np.array([ x for x in range(len(y_values)) ]) + offset
            else:
                x_values = np.array(ticks) + offset

        if fun == 'line':
            h, = plot_fun(x_values, y_values, **plot_params_series[key])
        elif fun == 'bar':
            h = plot_fun(x_values, y_values, **plot_params_series[key])

        series_info = info.SeriesInfo(key)
        series_info.set_legend_info(names[key], h)
        series_info.set_points(x_values, y_values)

        axis_info.add_series(key, series_info)

    axis_info.set_series_order(key_order)

    if ticklabels is not None:
        ax.set_xticklabels(ticklabels)

    if zoom_params is not None:
        factor = zoom_params.get('factor', 3)
        bbox_to_anchor = zoom_params.get('bbox_to_anchor', (0, 0, 1, 1))

        ax2 = zoomed_inset_axes(ax, factor, # zoom = factor
                                loc = 2,
                                bbox_to_anchor = bbox_to_anchor,
                                bbox_transform = ax.transAxes, #,
                                borderpad = 0)

        x1, y1 = zoom_params["zoom_from"]
        x2, y2 = zoom_params["zoom_to"]

        ax2.set_xlim(x1, x2)
        ax2.set_ylim(y1, y2)

        mark_inset(ax, ax2, loc1=2, loc2=4, fc="none", ec="0.5")

        for key in key_order:
            h, = ax2.plot(ticks, series[key],
                          **plot_params_series[key])


@plotter_func('line')
def line_series(*args, **kwargs):
    return simple_series(*args, **kwargs)

@plotter_func('bar', 'overflow')
def bar_series(*args, **kwargs):
    return simple_series(*args, **kwargs)

@plotter_func('bar', 'overflow', 'cluster')
def cluster_series(ax, series, cluster_elems, names,
                   key_order      = None,
                   ticks          = None,
                   ticklabels     = None,
                   offset         = 0,
                   bar_params     = {},
                   cluster_params = {},
                   overflow_params = {},
                   **kwargs):
    # Initialize param dictionaries
    bar_params      = defaults.get_defaults_fun('cluster_series', 'bar', bar_params)
    cluster_params  = defaults.get_defaults_fun('cluster_series', 'cluster', cluster_params)
    overflow_params = defaults.get_defaults_fun('cluster_series', 'overflow', overflow_params)

    if key_order is None:
        key_order = series.keys()

    # Initialize generators
    bar_params_series = instantiate_params(bar_params, key_order)

    clusters      = cluster_elems
    cluster_width = len(series) * bar_params['width']

    ticks = np.array([ x * (cluster_width + cluster_params['separation']) for x in range(clusters) ]) + offset

    info_order = key_order

    axis_info = ax.figure.get_axis_info(ax)

    for i, key in enumerate(key_order):
        x_values = ticks - cluster_width / 2.0 + i * bar_params_series[key]['width']
        y_values = series[key]

        if kwargs.has_key('ylim') and overflow_params['enable']:
            ylim = kwargs['ylim']
            for x, y in zip(x_values, y_values):
                if y >= ylim[1]:
                    plt.text(x,                        # x
                             ylim[1] + ylim[1] * 0.01, # y
                             '%.2f' % y,               # text
                             **overflow_params['label'])

        h = ax.bar(x_values, y_values, **bar_params_series[key])

        series_info = info.SeriesInfo(key)
        series_info.set_legend_info(names[key], h)
        series_info.set_points(x_values, y_values)

        axis_info.add_series(key, series_info)

    axis_info.set_series_order(key_order)

    cluster_info = info.ClusterInfo()
    cluster_info.set_clusters(names, [ t for t in ticks ])
    axis_info.set_clusters(cluster_info)

    ax.set_xticks(ticks)
    ax.set_xticklabels(ticklabels)

    ax.set_xlim((ticks[0] - cluster_width / 2.0) - cluster_params['outer'],
                (ticks[-1] + cluster_width / 2.0) + cluster_params['outer'])



@plotter_func('bar', 'overflow', 'cluster_2', 'major_cluster_2')
def cluster_series_2(ax, series, cluster_elems, major_cluster_elems, names,
                     key_order        = None,
                     ticks            = None,
                     ticklabels       = None,
                     major_ticks      = None,
                     major_ticklabels = None,
                     offset           = 0,
                     bar_params           = {},
                     cluster_params       = {},
                     major_cluster_params = {},
                     overflow_params      = {},
                     **kwargs):
    # Initialize param dictionaries
    bar_params           = defaults.get_defaults_fun('cluster_series_2', 'bar', bar_params)
    overflow_params      = defaults.get_defaults_fun('cluster_series_2', 'overflow', overflow_params)
    cluster_params       = defaults.get_defaults_fun('cluster_series_2', 'cluster_2', cluster_params)
    major_cluster_params = defaults.get_defaults_fun('cluster_series_2', 'major_cluster_2', major_cluster_params)

    if key_order is None:
        key_order = series.keys()

    # Initialize generators
    bar_params_series = instantiate_params(bar_params, key_order)

    clusters      = cluster_elems
    cluster_width = len(series)

    major_clusters = major_cluster_elems
    major_cluster_width = cluster_width * clusters + cluster_params['separation'] * (clusters-1)

    if major_ticks is None:
        major_ticks = np.array([ mc * (major_cluster_width + major_cluster_params['separation']) for mc in xrange(major_clusters)]) + offset

    if ticks is None:
        major_cluster_center_to_first_cluster_center = (cluster_width + cluster_params['separation']) * (clusters-1) / 2.0
        ticks = np.array([ mtic - major_cluster_center_to_first_cluster_center + c * (cluster_width + cluster_params['separation']) for mtic in major_ticks for c in xrange(clusters)]) + offset

    ax.set_xticks(ticks, minor=True)
    ax.set_xticks(major_ticks)

    axis_info = ax.figure.get_axis_info(ax)

    for i, key in enumerate(key_order):
        x_values = ticks - cluster_width / 2.0 + i
        y_values = series[key]

        if kwargs.has_key('ylim') and overflow_params['enable']:
            ylim = kwargs['ylim']
            for x, y in zip(x_values, y_values):
                if y >= ylim[1]:
                    plt.text(x,                        # x
                             ylim[1] + ylim[1] * 0.01, # y
                             '%.2f' % y,               # text
                             **overflow_params['label'])

        h = ax.bar(x_values, y_values, **bar_params_series[key])

        ## bar_params2 = bar_params.copy()
        ## bar_params2.pop('hatch', None)
        ## bar_params2['fill'] = False
        ## bar_params2['ec'] = 'black'
        ## bar_params2['lw'] = 0.5
        ## ax.bar(ticks - cluster_width / 2.0 + i, series[key],
        ##        1.0,
        ##        **bar_params2)

        series_info = info.SeriesInfo(key)
        series_info.set_legend_info(names[key], h)
        series_info.set_points(x_values, y_values)

        axis_info.add_series(key, series_info)

    axis_info.set_series_order(key_order)

    cluster_info = info.ClusterInfo()
    cluster_info.set_clusters(ticklabels * major_clusters, [ t for t in ticks ])
    axis_info.set_clusters(cluster_info, 0)

    cluster_info = info.ClusterInfo()
    cluster_info.set_clusters(major_ticklabels, [ t for t in major_ticks ])
    axis_info.set_clusters(cluster_info, 1)

    if ticklabels is not None:
        ax.set_xticklabels(ticklabels * major_clusters, minor=True, **cluster_params['label_params'])
    if major_ticklabels is not None:
        ax.set_xticklabels([('\n' * major_cluster_params['label_line']) + l for l in major_ticklabels],
                           **major_cluster_params['label_params'])

    ax.tick_params(axis='x', which='both', length=0) # removes tick lines

    ax.set_xlim((ticks[0] - cluster_width / 2.0) - major_cluster_params['outer'],
                (ticks[-1] + cluster_width / 2.0) + major_cluster_params['outer'])
