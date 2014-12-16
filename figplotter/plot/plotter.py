import matplotlib
import matplotlib.pyplot as plt

import defaults
import info

PLOTTER_FUNCS = {}

"""
Decorator for plotting functions. It handles the legend, and axes labels, scales and limits
If no figure exists yet the function creates it, otherwise plots on top of the given one
"""
def plotter_func(*plot_params):
    def plotter_decorator(func):
        # Register plotter function
        PLOTTER_FUNCS[func.__name__] = plot_params

        # Intercept function call and parse some arguments
        def inner(ax, *args, **kwargs):
            fig = ax.figure
            func(ax, *args, **kwargs)

            if kwargs.get('ylabel', None) is not None:
                ax.set_ylabel(kwargs['ylabel'])
            if kwargs.get('xlabel', None) is not None:
                ax.set_xlabel(kwargs['xlabel'])
            if kwargs.get('yscale', None) is not None:
                ax.set_yscale(kwargs['yscale'])
            if kwargs.get('xscale', None) is not None:
                ax.set_xscale(kwargs['xscale'])

            if kwargs.has_key('ylim'):
                ax.set_ylim(kwargs['ylim'])

            if kwargs.has_key('ygrid'):
                ax.yaxis.grid(kwargs['ygrid'])
            if kwargs.has_key('xgrid'):
                ax.xaxis.grid(kwargs['xgrid'])

            if kwargs.get('legend', True):
                legend_params = kwargs.get('legend_params', defaults.legend_params)
                axis_info = fig.get_axis_info(ax)
                axis_info.legend(**legend_params)

            return ax

        return inner

    return plotter_decorator

