import collections

bar_params = {
    'color'     : '#BB0000',
    'edgecolor' : '#000000',
    'hatch'     : '',
    'linewidth' : 1.0,
    'width'     : 1.0,
}

line_params = {
    'color'     : '#BB0000',
    'linewidth' : 1.0,
    'marker'    : '',
}

overflow_params = {
    'enable' : True,
    'label' : {
        'ha'      : 'left',
        'va'      : 'bottom',
        'fontsize': 9,
        'rotation': 20,
    }
}

cluster_params = {
    'outer'      : 1,
    'separation' : 1,
}

cluster_2_params = {
    'outer'      : 0,
    'separation' : 1,
    'label_params' : {
        'size': 'small'
    },
}

major_cluster_2_params = {
    'label_params': {},
    'label_line': 1, # hack to avoid overlapped labels
    'outer' : 0,
    'separation' : 2,
}

DEFAULTS = {
    'bar'             : bar_params,
    'line'            : line_params,
    'overflow'        : overflow_params,
    'cluster'         : cluster_params,
    'cluster_2'       : cluster_2_params,
    'major_cluster_2' : major_cluster_2_params,
}

DEFAULTS_PER_FUNCTION = {}

def update(d, u):
    for k, v in u.iteritems():
        if isinstance(v, collections.Mapping):
            r = update(d.get(k, {}), v)
            d[k] = r
        else:
            d[k] = u[k]

    return d

def register_fun(fun, params):
    DEFAULTS_PER_FUNCTION[fun] = {}
    for param in params:
        DEFAULTS_PER_FUNCTION[fun][param] = DEFAULTS[param]

def merge_params(default, user):
    params = default.copy()
    update(params, user)
    return params

def set_defaults_fun(fun, key, val):
    assert fun in DEFAULTS_PER_FUNCTION.keys(), 'Invalid function {0}'.format(fun)
    assert key in DEFAULTS_PER_FUNCTION[fun].keys(), '{0} is not a valid param group for {1}'.format(key, fun)

    DEFAULTS_PER_FUNCTION[fun][key] = merge_params(DEFAULTS_PER_FUNCTION[fun][key],
                                                   val.copy())

def get_defaults_fun(fun, key, override = None):
    assert fun in DEFAULTS_PER_FUNCTION.keys(), 'Invalid function {0}'.format(fun)
    assert key in DEFAULTS_PER_FUNCTION[fun].keys(), '{0} is not a valid param group for {1}'.format(key, fun)

    ret = DEFAULTS_PER_FUNCTION[fun][key]
    if override is not None:
        ret = merge_params(ret, override)

    return ret
