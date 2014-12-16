import numpy as np
import types

import matplotlib
import matplotlib.pyplot as plt

from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

from collections import OrderedDict

from .. import utils
import defaults
import info
from plotter import plotter_func

import matplotlib.patches as mpatches

def instantiate_params(params, series):
    """ Creates parameter dictionaries for the different series.

    This function substitutes utils.Parameter objects with the value for each
    series.

    Args:
        params (dict): original parameters dictionary
        series (list): list of series' identifiers

    Returns:
        dict: a dictionary that contains the instantiation of the original
        parameters for each of the series.
    """
    param_instances = {}

    for s in series:
        # Create an instance of the parameters' dictionary for each series
        p = params.copy()
        for key, value in params.items():
            if isinstance(value, utils.Parameter):
                # Instantiate the value for the current series
                v = value.values[s]
            else:
                # Use the value "as is"
                v = value

            p[key] = v

        param_instances[s] = p

    return param_instances


def plot_bars(ax, x_values, y_values, y_offsets = None, bar_params = None):
    """ Plots an array of bars

    This function plots an array of bars using the given parameters. It
    supports the following non-standard parameters:
        - hatchcolor

    Args:
        ax (Axis): axis where to plot
        x_value (list): x values
        y_value (list): y values
        y_offsets (list): y offsets
        bar_params (dict): dictionary of parameters to be used for the bars

    Returns:
        handle: a handle to be used in the legend generation
    """

    if y_offsets is None:
        y_offsets = [ 0 for _ in y_values ]

    if bar_params is None:
        bar_params = {}

    b_params = bar_params.copy()
    if b_params.has_key('hatchcolor'):
        # If hatchcolor is defined, use edgecolor to define the color of
        # the bar's line
        hcolor = b_params['hatchcolor']
        ecolor = b_params['edgecolor']
        if hcolor != ecolor:
            b_params['edgecolor'] = hcolor

        b_params.pop('hatchcolor', None)

        # Plot the bars
        h = ax.bar(x_values, y_values, **b_params)

        b_params['edgecolor'] = ecolor
        b_params['fill']      = False
        b_params['hatch']     = None

        # Plot empty bars to draw the colored bar lines
        ax.bar(x_values, y_values, bottom = y_offsets, **b_params)
    else:
        h = ax.bar(x_values, y_values, bottom = y_offsets, **bar_params)

    return h


def plot_overflow(ax, x, y, ylim, overflow_params):
    if y >= ylim[1]:
        ax.text(x,                        # x
                ylim[1] + ylim[1] * 0.01, # y
                '%.2f' % y,               # text
                **overflow_params['label'])


def simple_series(ax, series,
                  series_names = None,
                  fun = 'line',
                  key_order   = None,
                  ticks       = None,
                  ticklabels  = None,
                  zoom_params = None,
                  offset      = 0,
                  plot_params = {},
                  overflow_params = {},
                  tick_params = {},
                  **kwargs):
    # Create parameters' dictionaries
    plot_params     = defaults.get_defaults_fun(fun + '_series', fun, plot_params)
    overflow_params = defaults.get_defaults_fun(fun + '_series', 'overflow', overflow_params)
    tick_params     = defaults.get_defaults_fun(fun + '_series', 'tick', tick_params)

    len_series = -1
    for k, v in series.items():
        if len_series == -1:
            len_series = len(v)
        else:
            assert len_series == len(v), 'All series must have the same number of values'

    if key_order is None:
        key_order = series.keys()

    # Instantiate params
    plot_params_series     = instantiate_params(plot_params, key_order)
    overflow_params_series = instantiate_params(overflow_params, key_order)

    plot_params_all = {}

    axis_info = ax.figure.get_axis_info(ax)

    if series_names is None:
        series_names = { v: v for v in key_order }

    if fun == 'bar':
        offsets_bar = np.array([ 0.0 for _ in range(len_series) ])

    for key in key_order:
        if isinstance(series[key], tuple):
            x_values = series[key][1]
            y_values = series[key][0]
        else:
            y_values = series[key]

            if ticks is None:
                x_values = np.array([ x for x in range(len(y_values)) ]) + offset
                if fun == 'bar':
                    x_values = x_values - plot_params_series[key]['width'] / 2.0
            else:
                x_values = np.array(ticks) + offset

        if fun == 'line':
            h, = ax.plot(x_values, y_values, **plot_params_series[key])
        elif fun == 'bar':
            h = plot_bars(ax, x_values, y_values, y_offsets = offsets_bar, bar_params = plot_params_series[key])

            offsets_bar += y_values

        if kwargs.has_key('ylim') and overflow_params_series[key]['enable']:
            for x, y in zip(x_values, y_values):
                plot_overflow(ax, x, y, kwargs['ylim'], overflow_params_series[key])

        series_info = info.SeriesInfo(key)
        series_info.set_legend_info(series_names[key], h)
        series_info.set_points(x_values, y_values)

        axis_info.add_series(key, series_info)

    if fun == 'bar':
        axis_info.set_series_order(key_order[::-1])
    else:
        axis_info.set_series_order(key_order)

    if ticklabels is not None:
        ax.set_xticklabels(ticklabels)
        ax.tick_params(axis='x', which='both', **tick_params)

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


@plotter_func('line', 'overflow', 'tick')
def line_series(*args, **kwargs):
    return simple_series(*args, **kwargs)

@plotter_func('bar', 'overflow', 'tick')
def bar_series(*args, **kwargs):
    return simple_series(*args, fun='bar', **kwargs)

@plotter_func('bar', 'overflow', 'cluster')
def cluster_series(ax, series, clusters,
                   series_names   = None,
                   cluster_names  = None,
                   key_order      = None,
                   offset         = 0,
                   bar_params     = {},
                   cluster_params = {},
                   overflow_params = {},
                   tick_params     = {},
                   **kwargs):
    # Initialize param dictionaries
    bar_params      = defaults.get_defaults_fun('cluster_series', 'bar', bar_params)
    cluster_params  = defaults.get_defaults_fun('cluster_series', 'cluster', cluster_params)
    overflow_params = defaults.get_defaults_fun('cluster_series', 'overflow', overflow_params)

    if key_order is None:
        series_dict = series.items()[0][1]
        key_order = series_dict.keys()
        if not isinstance(series_dict, OrderedDict):
            key_order = sorted(key_order)


    # Instantiate params
    bar_params_series      = instantiate_params(bar_params, key_order)
    overflow_params_series = instantiate_params(overflow_params, key_order)

    nclusters     = len(clusters)
    cluster_width = len(key_order) * bar_params['width']

    ticks = np.array([ x * (cluster_width + cluster_params['separation']) for x in range(nclusters) ]) + offset

    axis_info = ax.figure.get_axis_info(ax)

    if series_names is None:
        series_names = { v: v for v in key_order }

    if cluster_names is None:
        cluster_names = clusters
    else:
        cluster_names = [ cluster_names[c] for c in clusters ]

    for i, key in enumerate(key_order):
        x_values = ticks - cluster_width / 2.0 + i * bar_params_series[key]['width']
        y_values = []

        for c in clusters:
            y_values.append(series[c][key])

        if kwargs.has_key('ylim') and overflow_params_series[key]['enable']:
            for x, y in zip(x_values, y_values):
                plot_overflow(ax, x, y, kwargs['ylim'], overflow_params_series[key])

        h = plot_bars(ax, x_values, y_values, bar_params = bar_params_series[key])

        series_info = info.SeriesInfo(key)
        series_info.set_legend_info(series_names[key], h)
        series_info.set_points(x_values, y_values)

        axis_info.add_series(key, series_info)

    axis_info.set_series_order(key_order)

    cluster_info = info.ClusterInfo()
    cluster_info.set_clusters(clusters, [ t for t in ticks ])
    axis_info.set_clusters(cluster_info)

    ax.set_xticks(ticks)
    ax.set_xticklabels(cluster_names)

    ax.tick_params(axis='x', which='both', **cluster_params['tick_params'])

    ax.set_xlim((ticks[0] - cluster_width / 2.0) - cluster_params['outer'],
                (ticks[-1] + cluster_width / 2.0) + cluster_params['outer'])



@plotter_func('bar', 'overflow', 'cluster_2', 'major_cluster_2')
def cluster_series_2(ax, series, clusters,
                     series_names     = None,
                     cluster_names    = None,
                     key_order        = None,
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
        series_dict = series.items()[0][1].items()[0][1]
        key_order = series_dict.keys()
        if not isinstance(series_dict, OrderedDict):
            key_order = sorted(key_order)

    # Instantiate params
    bar_params_series      = instantiate_params(bar_params, key_order)
    overflow_params_series = instantiate_params(overflow_params, key_order)

    nclusters     = len(clusters[1])
    cluster_width = len(key_order)

    major_clusters      = len(clusters[0])
    major_cluster_width = cluster_width * nclusters + cluster_params['separation'] * (nclusters - 1)

    major_ticks = np.array([ mc * (major_cluster_width + major_cluster_params['separation']) for mc in xrange(major_clusters)]) + offset

    major_cluster_center_to_first_cluster_center = (cluster_width + cluster_params['separation']) * (nclusters - 1) / 2.0
    ticks = np.array([ mtic - major_cluster_center_to_first_cluster_center + c * (cluster_width + cluster_params['separation']) for mtic in major_ticks for c in xrange(nclusters)]) + offset

    ax.set_xticks(ticks, minor = True)
    ax.set_xticks(major_ticks)

    axis_info = ax.figure.get_axis_info(ax)

    if series_names is None:
        series_names = { v: v for v in key_order }

    if cluster_names is None:
        cluster_names = [ None, None ]
        cluster_names[0] = clusters[0]
        cluster_names[1] = clusters[1]
    else:
        cluster_names[0] = [ cluster_names[0][c] for c in clusters[0] ]
        cluster_names[1] = [ cluster_names[1][c] for c in clusters[1] ]

    for i, key in enumerate(key_order):
        x_values = ticks - cluster_width / 2.0 + i
        y_values = []

        for c0 in clusters[0]:
            for c1 in clusters[1]:
                y_values.append(series[c0][c1][key])

        if kwargs.has_key('ylim') and overflow_params_series[key]['enable']:
            for x, y in zip(x_values, y_values):
                plot_overflow(ax, x, y, kwargs['ylim'], overflow_params_series[key])

        h = plot_bars(ax, x_values, y_values, bar_params = bar_params_series[key])

        series_info = info.SeriesInfo(key)
        series_info.set_legend_info(series_names[key], h)
        series_info.set_points(x_values, y_values)

        axis_info.add_series(key, series_info)

    axis_info.set_series_order(key_order)

    cluster_info = info.ClusterInfo()
    cluster_info.set_clusters(clusters[0] * major_clusters, [ t for t in ticks ])
    axis_info.set_clusters(cluster_info, 0)

    cluster_info = info.ClusterInfo()
    cluster_info.set_clusters(clusters[1], [ t for t in major_ticks ])
    axis_info.set_clusters(cluster_info, 1)

    ax.set_xticks(major_ticks, minor = False)
    ax.set_xticklabels(cluster_names[0], minor = False,
                       **major_cluster_params['label_params'])

    ax.set_xticks(ticks, minor = True)
    ax.set_xticklabels(cluster_names[1] * major_clusters, minor = True,
                       **cluster_params['label_params'])

    ax.tick_params(axis='x', which='minor', **cluster_params['tick_params'])
    ax.tick_params(axis='x', which='major', **major_cluster_params['tick_params'])

    ax.set_xlim((ticks[0] - cluster_width / 2.0) - major_cluster_params['outer'],
                (ticks[-1] + cluster_width / 2.0) + major_cluster_params['outer'])
