'''
Created on Jan 19, 2015

@author: Javier Cabezas <javier.cabezas@gmail.com>
'''

import collections as C
import copy
import sys


def update(d, u):
    '''
    Recursively update a dict hierarchy. It also merges leafs that are Parameter objects,
    used in the plot styles

    @param d (dict): dictionary to be updated
    @param u (dict): dictionary withe th values to be merged

    @return: the merged dictionary hierarchy
    '''
    for k, v in u.items():
        if isinstance(v, C.Mapping):
            orig = copy.deepcopy(d.get(k, {}))
            r = update(orig, v)
            d[k] = r
        elif isinstance(v, Parameter):
            orig = copy.deepcopy(d.get(k, Parameter({})))
            orig.update(v)
            d[k] = orig
        else:
            d[k] = copy.deepcopy(u[k])

    return d


def range_generator(start, stop):
    assert start < stop, "Wrong values for range generator"
    distance = float(stop - start)
    return lambda x: (start + (distance/(x - 1)) * i if x > 1 else start for i in range(x))


class Parameter(object):
    @staticmethod
    def __check_valid_names(names):
        for name in names:
            if name in []:
                raise Exception('Invalid name "{0}"'.format(name))

    def __init__(self, values):
        if isinstance(values, C.Mapping):
            Parameter.__check_valid_names(values.keys())

        self.values = values

    def update(self, param):
        def check_default_value(orig, new):
            if '*' in orig.keys() and '*' in new.keys():
                if orig['*'] != new['*']:
                    raise Exception('Different default values')
            else:
                return True

        if isinstance(param, Parameter):
            check_default_value(self.values, param.values)
            self.values = update(self.values, param.values)
        elif isinstance(param, C.Mapping):
            check_default_value(self.values, param)
            self.values = update(self.values, param)
        else:
            raise Exception('Updating parameter with no series')

    def __repr__(self):
        return 'Param: {0}'.format(self.values)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)


def param(l):
    if isinstance(l, list):
        # Generator from list
        return lambda x: (m for m in l)
    else:
        # Constant generator
        return lambda x: (l for _ in range(x))


def string_generator(pattern, values):
    return lambda x: (pattern % value for value in values(x))


def clusterize(series, clusters):
    '''
    Creates a tree of dictionaries that represents a hierarchy of clusters. Leaves
    represents the values in the series for each cluster
    '''
    # Check all series contain the same number of values
    len_series = -1
    for k, v in series.items():
        if len_series == -1:
            len_series = len(v)
        else:
            assert len_series == len(v), 'All series must have the same number of values'

    # Compute all the number of clusters
    nclusters = 1
    for cluster_level in clusters:
        nclusters = nclusters * len(cluster_level)

    assert nclusters == len_series, 'Series must contain as many values as clusters'

    def walk(d, fun):
        '''
        Apply fun to each node in the tree

        @arg d (dict): root node of the tree
        @arg fun (function): function to be applied
        '''
        if len(d.items()) == 0:
            fun(d)
        else:
            for k, v in d.items():
                walk(v, fun)

    def leafs(d):
        '''
        Get the clusters in the leaves of the tree

        @arg d (dict): root node of the tree

        @return: list containing the clusters in the leaves of the tree
        '''
        if len(d.items()) == 0:
            return [ d ]
        else:
            ret = []
            for k, v in d.items():
                ret += leafs(v)

        return ret

    # Create the hierarchy of clusters
    ret = C.OrderedDict()
    for cluster_level in clusters:
        def insert_cluster(d):
            for cluster in cluster_level:
                d[cluster] = C.OrderedDict()

        walk(ret, insert_cluster)

    # Add the series values to each cluster leaf
    for i, leaf in enumerate(leafs(ret)):
        for k, series_vals in series.items():
            leaf[k] = series_vals[i]

    return ret


LOG_LEVELS = { 'error'  : -1,
               'message':  0,
               'verbose':  1,
               'debug'  :  2 }
LOG_LEVEL_DEFAULT = 'message'
LOG_LEVEL         = LOG_LEVELS[LOG_LEVEL_DEFAULT]


def set_log_level(log_level):
    global LOG_LEVEL
    if log_level == 'default':
        LOG_LEVEL = LOG_LEVELS[LOG_LEVEL_DEFAULT]
    else:
        assert log_level in LOG_LEVELS.keys(), 'Invalid log level "{0}". Valid values are: {1}'.format(log_level, LOG_LEVELS.keys())
        LOG_LEVEL = LOG_LEVELS[log_level]


def error(msg, cond = True):
    if cond and LOG_LEVEL >= LOG_LEVELS['error']:
        sys.stderr.write('[error]: ' + msg + '\n')


def message(msg, cond = True):
    if cond and LOG_LEVEL >= LOG_LEVELS['message']:
        sys.stdout.write(msg + '\n')


def warning(msg, cond = True):
    if cond and LOG_LEVEL >= LOG_LEVELS['verbose']:
        sys.stderr.write('[warn]: ' + msg + '\n')


def debug(msg, cond = True):
    if cond and LOG_LEVEL >= LOG_LEVELS['debug']:
        sys.stdout.write('[debug]: ' + msg + '\n')
