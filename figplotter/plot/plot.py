'''
Created on Jan 19, 2015

@author: Javier Cabezas <javier.cabezas@gmail.com>
'''

from collections import OrderedDict, Mapping
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes

import copy
import itertools
import numpy as np

from .. import utils
from . import info
from . import plotter
from . import style


def instantiate_params_series(params_out, params_in, series):
    for key, value in params_in.items():
        if isinstance(value, utils.Parameter):
            # Instantiate the value for the current series
            if series in value.values.keys():
                v = value.values[series]
            else:
                del params_out[key]
                continue
        elif isinstance(value, Mapping):
            # Nested property, go to the next level
            instantiate_params_series(params_out[key], params_in[key], series)
            continue
        else:
            # Use the value "as is"
            v = value

        params_out[key] = v


def instantiate_params(params, series_list):
    ''' Creates parameter dictionaries for the different series.

    This function substitutes utils.Parameter objects with the value for each
    series.

    @param params (dict): original parameters dictionary
    @param series_list (list): list of series' identifiers

    @return dict: a dictionary that contains the instantiation of the original
            parameters for each of the series.
    '''
    param_instances = {}

    for series in series_list:
        # Create an instance of the parameters' dictionary for each series
        params_in  = copy.deepcopy(params)
        params_out = copy.deepcopy(params)
        instantiate_params_series(params_out, params_in, series)
        param_instances[series] = params_out

    return param_instances


def plot_bars(ax, x_values, y_values, y_offsets = None, bar_params = {}):
    ''' Plots an array of bars

    This function plots an array of bars using the given parameters. It
    supports the following non-standard parameters:
        - hatchcolor

    @param ax (Axis): axis where to plot
    @param x_values (list): x values
    @param y_values (list): y values
    @param y_offsets (list): y offsets
    @param bar_params (dict): dictionary of parameters to be used for the bars

    @return handle: a handle to be used in the legend generation
    '''

    if y_offsets is None:
        y_offsets = np.zeros(len(y_values))

    if 'hatchcolor' in bar_params.keys():
        b_params = bar_params.copy()
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
    '''
    Plots labels with values greater than ylim

    This function plots labels with values greater than ylim.

    @param ax (Axis): axis where to plot
    @param x (number): x value
    @param y (number): y value
    @param ylim (number): maximum y value in the figure
    @param overflow_params (dict): dictionary of parameters to be used for the labels
    '''
    if y >= ylim[1]:
        ax.text(x,                        # x
                ylim[1] + ylim[1] * 0.01, # y
                '%.2f' % y,               # text
                **overflow_params['label'])


def simple_series(ax, series,
                  fun,
                  series_names = None,
                  key_order   = None,
                  ticks       = None,
                  ticklabels  = None,
                  zoom_params = None,
                  offset      = 0,
                  style_series = {},
                  style_axis = {},
                  **kwargs):
    len_series = -1
    for _, v in series.items():
        if len_series == -1:
            len_series = len(v)
        else:
            assert len_series == len(v), 'All series must have the same number of values'

    if key_order is None:
        key_order = list(series.keys())

    params_series = style.generate_params(style_series, [ key_order ], 'style_series', fun + '_series')
    params_axis   = style.generate_params(style_axis, [['x', 'y']], 'style_axis', fun + '_series')

    barplot_params  = params_series[fun + '_params']
    overflow_params = params_series['overflow_params']

    tick_params      = params_axis['tick_params']
    ticklabel_params = params_axis['ticklabel_params']

    # Instantiate params_series
    barplot_params_series  = instantiate_params(barplot_params, key_order)
    overflow_params_series = instantiate_params(overflow_params, key_order)

    tick_params_axis = instantiate_params(tick_params, ['x', 'y'])
    ticklabel_params_axis = instantiate_params(ticklabel_params, ['x', 'y'])

    axis_info = ax.figure.get_axis_info(ax)

    if series_names is None:
        series_names = { v: v for v in key_order }

    if fun == 'bar':
        offsets_bar = np.zeros(len_series)

    for key in key_order:
        if isinstance(series[key], tuple):
            x_values = series[key][1]
            y_values = series[key][0]
        else:
            y_values = series[key]

            if ticks is None:
                x_values = np.arange(len(y_values)) + offset
                if fun == 'bar':
                    x_values = x_values - barplot_params_series[key]['width'] / 2.0
            else:
                x_values = np.array(ticks) + offset

        if fun == 'plot':
            h, = ax.plot(x_values, y_values, **barplot_params_series[key])
        elif fun == 'bar':
            h = plot_bars(ax, x_values, y_values, y_offsets = offsets_bar, bar_params = barplot_params_series[key])

            offsets_bar += y_values

        if 'ylim' in kwargs.keys() and overflow_params_series[key]['enable']:
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
        if ticks is not None:
            ax.set_xticks(ticks)

        ax.set_xticklabels(ticklabels, **ticklabel_params_axis['x'])

    ax.tick_params(axis='x', **tick_params_axis['x'])
    ax.tick_params(axis='y', **tick_params_axis['y'])

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
            if fun == 'plot':
                h, = ax2.plot(ticks, series[key], **barplot_params_series[key])
            else:
                h = plot_bars(ax2, ticks, series[key], bar_params = barplot_params_series[key])


@plotter.plotter_func({'style_series': ['plot', 'overflow'],
                       'style_axis'  : ['tick', 'ticklabel']})
def plot_series(*args, **kwargs):
    args = list(args) + ['plot']
    return simple_series(*args, **kwargs)


@plotter.plotter_func({'style_series': ['bar', 'overflow'],
                       'style_axis'  : ['tick', 'ticklabel']})
def bar_series(*args, **kwargs):
    args = list(args) + ['bar']
    return simple_series(*args, **kwargs)


@plotter.plotter_func({'style_series' : ['bar', 'overflow'],
                       'style_axis'   : ['tick', 'ticklabel'],
                       'style_cluster': ['cluster']})
def cluster_series(ax, series, clusters,
                   series_names  = None,
                   cluster_names = None,
                   key_order     = None,
                   offset        = 0,
                   style_series  = {},
                   style_axis    = {},
                   style_cluster = {},
                   **kwargs):
    if key_order is None:
        series_dict = series[list(series.keys())[0]]
        key_order = series_dict.keys()
        if not isinstance(series_dict, OrderedDict):
            key_order = sorted(key_order)

    assert len(clusters) == 1, 'This function only supports one-level clustering'
    clusters = clusters[0]

    params_series  = style.generate_params(style_series, [ clusters, key_order ], 'style_series', 'cluster_series')
    params_axis    = style.generate_params(style_axis, [ ['x', 'y'] ], 'style_axis', 'cluster_series')
    params_cluster = style.generate_params(style_cluster, [ clusters ], 'style_cluster', 'cluster_series')

    # Initialize param dictionaries
    bar_params      = params_series['bar_params']
    overflow_params = params_series['overflow_params']

    tick_params      = params_axis['tick_params']
    ticklabel_params = params_axis['ticklabel_params']

    cluster_params = params_cluster['cluster_params']

    series_fqn = [ "::".join(e) for e in list(itertools.product(clusters, key_order)) ]

    # Instantiate params
    bar_params_series      = instantiate_params(bar_params, series_fqn)
    overflow_params_series = instantiate_params(overflow_params, series_fqn)

    tick_params_axis      = instantiate_params(tick_params, ['x', 'y'])
    ticklabel_params_axis = instantiate_params(ticklabel_params, ['x', 'y'])

    cluster_params_clusters = instantiate_params(cluster_params, clusters)

    cluster_widths = {}
    for cluster in clusters:
        cluster_width = 0.0
        for key in key_order:
            cluster_width += bar_params_series[cluster + "::" + key]['width']

        cluster_widths[cluster] = cluster_width

    current = offset
    ticks_list = [ ]
    for i, cluster in enumerate(clusters):
        if i == 0:
            current += cluster_params_clusters[cluster]['outer']
            current += cluster_widths[cluster] / 2.0
        else:
            current += cluster_widths[clusters[i-1]] / 2.0
            current += cluster_params_clusters[clusters[i-1]]['separation']
            current += cluster_params_clusters[cluster]['separation']
            current += cluster_widths[cluster] / 2.0

        ticks_list.append(current)

    ticks = np.array(ticks_list)

    if series_names is None:
        series_names = { v: v for v in key_order }

    if cluster_names is None:
        cluster_names = clusters
    else:
        cluster_names = [ cluster_names[c] for c in clusters ]

    axis_info = ax.figure.get_axis_info(ax)
    axis_info.set_series_order(key_order)

    for i, cluster in enumerate(clusters):
        off = 0.0
        for key in key_order:
            series_fqn = cluster + '::' + key
            x_value = ticks[i] - cluster_widths[cluster] / 2.0 + off
            y_value = series[cluster][key]

            off += bar_params_series[series_fqn]['width']

            if 'ylim' in kwargs.keys() and overflow_params_series[series_fqn]['enable']:
                plot_overflow(ax, x_value, y_value, kwargs['ylim'], overflow_params_series[series_fqn])

            h = plot_bars(ax, [x_value], [y_value], bar_params = bar_params_series[series_fqn])

            # Register information for the series
            series_info = info.SeriesInfo(key)
            series_info.set_legend_info(series_names[key], h)
            series_info.set_points([x_value], [y_value])
            axis_info.add_series(key, series_info)

    # TODO: Fix cluster info
    """cluster_info = info.ClusterInfo()
    cluster_info.set_clusters(clusters, [ t for t in ticks ])
    axis_info.set_clusters(cluster_info)"""

    ax.set_xticks(ticks)
    ax.set_xticklabels(cluster_names, **ticklabel_params_axis['x'])
    ax.tick_params(axis='x', which='both', **tick_params_axis['x'])
    ax.tick_params(axis='y', which='both', **tick_params_axis['y'])

    first_cluster_width = cluster_widths[clusters[0]]
    first_cluster_outer = cluster_params_clusters[clusters[0]]['outer']
    last_cluster_width = cluster_widths[clusters[-1]]
    last_cluster_outer = cluster_params_clusters[clusters[-1]]['outer']
    if offset > 0:
        ax.set_xlim(right = ticks[-1] + last_cluster_width/2.0 + last_cluster_outer)
    else:
        ax.set_xlim(left = ticks[0] - (first_cluster_width/2.0 + first_cluster_outer),
                    right = ticks[-1] + last_cluster_width/2.0 + last_cluster_outer)


@plotter.plotter_func({'style_series'       : ['bar', 'overflow'],
                       'style_axis'         : ['tick', 'ticklabel', 'major_tick', 'major_ticklabel'],
                       'style_cluster'      : ['cluster'],
                       'style_major_cluster': ['cluster']})
def cluster_series_2(ax, series, clusters,
                     series_names  = None,
                     cluster_names = None,
                     key_order     = None,
                     offset        = 0,
                     style_series  = {},
                     style_axis    = {},
                     style_cluster = {},
                     style_major_cluster = {},
                     **kwargs):
    if key_order is None:
        series_dict = series[list(series.keys())[0]]
        series_dict = series_dict[list(series_dict.keys())[0]]
        key_order = series_dict.keys()
        if not isinstance(series_dict, OrderedDict):
            key_order = sorted(key_order)

    assert len(clusters) == 2, 'This function only supports two-level clustering'

    params_series  = style.generate_params(style_series, clusters + [ key_order ], 'style_series', 'cluster_series_2')
    params_axis    = style.generate_params(style_axis, [ ['x', 'y'] ], 'style_axis', 'cluster_series_2')
    params_cluster = style.generate_params(style_cluster, clusters, 'style_cluster', 'cluster_series_2')
    params_major_cluster = style.generate_params(style_major_cluster, [ clusters[0] ], 'style_major_cluster', 'cluster_series_2')

    # Initialize param dictionaries
    bar_params      = params_series['bar_params']
    overflow_params = params_series['overflow_params']

    tick_params      = params_axis['tick_params']
    ticklabel_params = params_axis['ticklabel_params']
    major_tick_params      = params_axis['major_tick_params']
    major_ticklabel_params = params_axis['major_ticklabel_params']

    cluster_params       = params_cluster['cluster_params']
    major_cluster_params = params_major_cluster['cluster_params']

    series_fqn   = [ "::".join(e) for e in list(itertools.product(*(clusters + [key_order]))) ]
    clusters_fqn = [ "::".join(e) for e in list(itertools.product(*clusters)) ]

    # Instantiate params
    bar_params_series      = instantiate_params(bar_params, series_fqn)
    overflow_params_series = instantiate_params(overflow_params, series_fqn)

    tick_params_axis      = instantiate_params(tick_params, ['x', 'y'])
    ticklabel_params_axis = instantiate_params(ticklabel_params, ['x', 'y'])
    major_tick_params_axis      = instantiate_params(major_tick_params, ['x', 'y'])
    major_ticklabel_params_axis = instantiate_params(major_ticklabel_params, ['x', 'y'])

    cluster_params_clusters = instantiate_params(cluster_params, clusters_fqn)
    major_cluster_params_clusters = instantiate_params(major_cluster_params, clusters[0])

    major_clusters = clusters[0]
    minor_clusters = clusters[1]

    major_cluster_widths = {}
    cluster_widths = {}
    for i, major_cluster in enumerate(major_clusters):
        major_cluster_width = 0.0
        for j, cluster in enumerate(minor_clusters):
            prev_cluster_fqn = "::".join([major_cluster, minor_clusters[j-1]])
            cluster_fqn      = "::".join([major_cluster, cluster])
            cluster_width = 0.0
            for key in key_order:
                series_fqn      = "::".join([major_cluster, cluster, key])
                cluster_width += bar_params_series[series_fqn]['width']

            cluster_widths[cluster_fqn] = cluster_width

            major_cluster_width += cluster_width
            if j == 0 or j == len(minor_clusters) - 1:
                major_cluster_width += cluster_params_clusters[cluster_fqn]['outer']
            if j > 0:
                major_cluster_width += cluster_params_clusters[prev_cluster_fqn]['separation']
            if j < len(minor_clusters) - 1:
                major_cluster_width += cluster_params_clusters[cluster_fqn]['separation']

        major_cluster_widths[major_cluster] = major_cluster_width

    current = offset
    ticks_list = [ ]
    for i, major_cluster in enumerate(major_clusters):
        if i == 0:
            current += major_cluster_params_clusters[major_cluster]['outer']
        else:
            current += major_cluster_params_clusters[major_clusters[i-1]]['separation']
            current += major_cluster_params_clusters[major_cluster]['separation']

        for j, cluster in enumerate(minor_clusters):
            prev_cluster_fqn = "::".join([major_cluster, minor_clusters[j-1]])
            cluster_fqn      = "::".join([major_cluster, cluster])
            if j == 0:
                current += cluster_params_clusters[cluster_fqn]['outer']
                current += cluster_widths[cluster_fqn] / 2.0
            else:
                current += cluster_widths[prev_cluster_fqn] / 2.0
                current += cluster_params_clusters[prev_cluster_fqn]['separation']
                current += cluster_params_clusters[     cluster_fqn]['separation']
                current += cluster_widths[cluster_fqn] / 2.0

            ticks_list.append(current)

            if j == len(minor_clusters) - 1:
                current += cluster_widths[cluster_fqn] / 2.0
                current += cluster_params_clusters[cluster_fqn]['outer']

        if i == len(major_clusters) - 1:
            current += major_cluster_params_clusters[major_cluster]['outer']

    ticks = np.array(ticks_list)

    current = offset
    major_ticks_list = [ ]
    for i, major_cluster in enumerate(major_clusters):
        if i == 0:
            current += major_cluster_params_clusters[major_cluster]['outer']
            current += major_cluster_widths[major_cluster] / 2.0
        else:
            current += major_cluster_widths[major_clusters[i-1]] / 2.0
            current += major_cluster_params_clusters[major_clusters[i-1]]['separation']
            current += major_cluster_params_clusters[major_cluster]['separation']
            current += major_cluster_widths[major_cluster] / 2.0

        major_ticks_list.append(current)

    major_ticks = np.array(major_ticks_list)

    ax.set_xticks(ticks, minor = True)
    ax.set_xticks(major_ticks, minor = False)

    axis_info = ax.figure.get_axis_info(ax)
    axis_info.set_series_order(key_order)

    if series_names is None:
        series_names = { v: v for v in key_order }

    if cluster_names is None:
        cluster_names = [ None, None ]
        cluster_names[0] = clusters[0]
        cluster_names[1] = clusters[1]
    else:
        cluster_names[0] = [ cluster_names[0][c] for c in clusters[0] ]
        cluster_names[1] = [ cluster_names[1][c] for c in clusters[1] ]

    for i, major_cluster in enumerate(major_clusters):
        for j, cluster in enumerate(minor_clusters):
            cluster_fqn = '::'.join([major_cluster, cluster])
            off = 0.0
            for key in key_order:
                series_fqn = '::'.join([major_cluster, cluster, key])
                x_value = ticks[i * len(minor_clusters) + j] - cluster_widths[cluster_fqn] / 2.0 + off
                y_value = series[major_cluster][cluster][key]

                off += bar_params_series[series_fqn]['width']

                if 'ylim' in kwargs.keys() and overflow_params_series[series_fqn]['enable']:
                    plot_overflow(ax, x_value, y_value, kwargs['ylim'], overflow_params_series[series_fqn])

                h = plot_bars(ax, [x_value], [y_value], bar_params = bar_params_series[series_fqn])

                # Register information for the series
                series_info = info.SeriesInfo(key)
                series_info.set_legend_info(series_names[key], h)
                series_info.set_points([x_value], [y_value])
                axis_info.add_series(key, series_info)

    """
    cluster_info = info.ClusterInfo()
    cluster_info.set_clusters(clusters[0] * major_clusters, [ t for t in ticks ])
    axis_info.set_clusters(cluster_info, 0)

    cluster_info = info.ClusterInfo()
    cluster_info.set_clusters(clusters[1], [ t for t in major_ticks ])
    axis_info.set_clusters(cluster_info, 1)
    """

    ax.set_xticks(major_ticks, minor = False)
    ax.set_xticklabels(cluster_names[0], minor = False,
                       **major_ticklabel_params_axis['x'])

    ax.set_xticks(ticks, minor = True)
    ax.set_xticklabels(cluster_names[1] * len(major_clusters), minor = True,
                       **ticklabel_params_axis['x'])

    ax.tick_params(axis='x', which='minor', **tick_params_axis['x'])
    ax.tick_params(axis='x', which='major', **major_tick_params_axis['x'])
    ax.tick_params(axis='y', which='minor', **tick_params_axis['y'])
    ax.tick_params(axis='y', which='major', **major_tick_params_axis['y'])

    first_major_cluster_width = major_cluster_widths[major_clusters[0]]
    first_major_cluster_outer = major_cluster_params_clusters[major_clusters[0]]['outer']
    last_major_cluster_width = major_cluster_widths[major_clusters[-1]]
    last_major_cluster_outer = major_cluster_params_clusters[major_clusters[-1]]['outer']
    if offset > 0:
        ax.set_xlim(right = major_ticks[-1] + last_major_cluster_width/2.0 + last_major_cluster_outer)
    else:
        ax.set_xlim(left = major_ticks[0] - (first_major_cluster_width/2.0 + first_major_cluster_outer),
                    right = major_ticks[-1] + last_major_cluster_width/2.0 + last_major_cluster_outer)
