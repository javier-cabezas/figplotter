'''
Created on Jan 19, 2015

@author: Javier Cabezas <javier.cabezas@gmail.com>
'''

import itertools

from .. import utils

'''
Parameter used for "_" values defined by the base styles
'''
class BaseParameter(utils.Parameter):
    def __init__(self, values):
        self.values = values

P = BaseParameter

bar_params = [
    #'color'     : '#BB0000',
    ('bar::edgecolor', '#000000'),
    ('bar::hatch'    , ''),
    ('bar::linewidth', 1.0),
    ('bar::width'    , 1.0),
]

plot_params = [
    #'color'     : '#BB0000',
    ('plot::linewidth', 1.0),
    ('plot::marker'   , ''),
]

overflow_params = [
    ('overflow::enable'   , True),
    ('overflow::label::ha', 'left'),
    ('overflow::label::va', 'bottom'),
    ('overflow::label::fontsize', 9),
    ('overflow::label::rotation', 20)
]

tick_params = [
    ('tick::color',     '#000000'),
    ('tick::direction', 'out'),
]

major_tick_params = [
    ('major_tick::color',     '#000000'),
    ('major_tick::direction', 'out'),
]

ticklabel_params = [
    ('ticklabel::color', '#000000'),
    ('ticklabel::x',     0.0),
    ('ticklabel::y',     0.0)
]

major_ticklabel_params = [
    ('major_ticklabel::color', '#000000'),
    ('major_ticklabel::x',     0.0),
    ('major_ticklabel::y',     0.0)
]

cluster_params = [
    ('cluster::outer'      , 1),
    ('cluster::separation' , 0.5),
]

DEFAULTS = {
    'bar'             : bar_params,
    'plot'            : plot_params,
    'overflow'        : overflow_params,
    'tick'            : tick_params,
    'major_tick'      : major_tick_params,
    'ticklabel'       : ticklabel_params,
    'major_ticklabel' : major_ticklabel_params,
    'cluster'         : cluster_params,
    'major_cluster'   : cluster_params
}

FUNCTION_DEFAULTS = {}

legend_params = {
    'loc': 'best',
}


def merge_params(default, user):
    params = default.copy()
    utils.update(params, user)
    return params


def register_function(fun, styles):
    FUNCTION_DEFAULTS[fun] = {}
    for style_name, params in styles.items():
        FUNCTION_DEFAULTS[fun][style_name] = {}
        for param in params:
            FUNCTION_DEFAULTS[fun][style_name][param] = DEFAULTS[param]


def get_function_defaults(fun, selectors, style):
    assert fun in FUNCTION_DEFAULTS.keys(), 'Invalid function {0}'.format(fun)

    ret = []

    combinations = itertools.product(*selectors)

    for combination in list(combinations):
        query = "::".join(combination)
        query_dict = {}
        for param in FUNCTION_DEFAULTS[fun][style].keys():
            for k, v in FUNCTION_DEFAULTS[fun][style][param]:
                query_dict[k] = v

        ret += [(query, query_dict)]

    return ret
