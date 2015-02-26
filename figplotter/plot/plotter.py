'''
Created on Jan 19, 2015

@author: Javier Cabezas <javier.cabezas@gmail.com>
'''
from . import defaults

PLOTTER_FUNCS = {}

'''
Decorator for plotting functions. It handles the legend, and axes labels, scales and limits
If no figure exists yet the function creates it, otherwise plots on top of the given one
'''
def plotter_func(plot_styles):
    def plotter_decorator(func):
        # Register plotter function
        PLOTTER_FUNCS[func.__name__] = plot_styles

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

            if 'ylim' in kwargs.keys():
                ax.set_ylim(kwargs['ylim'])
            if 'xlim' in kwargs.keys():
                ax.set_xlim(kwargs['xlim'])

            if 'ygrid' in kwargs.keys():
                ax.yaxis.grid(kwargs['ygrid'])
            if 'xgrid' in kwargs.keys():
                ax.xaxis.grid(kwargs['xgrid'])

            if kwargs.get('legend', True):
                legend_params = kwargs.get('legend_params', defaults.legend_params)
                axis_info = fig.get_axis_info(ax)
                axis_info.legend(**legend_params)

            return ax

        return inner

    return plotter_decorator

