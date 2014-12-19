from collections import OrderedDict

def range_generator(start, stop):
    assert start < stop, "Wrong values for range generator"
    distance = float(stop - start)
    return lambda x: (start + (distance/(x - 1)) * i if x > 1 else start for i in range(x))

class Parameter(object):
    def __init__(self, values):
        self.values = values

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
    len_series = -1
    for k, v in series.items():
        if len_series == -1:
            len_series = len(v)
        else:
            assert len_series == len(v), 'All series must have the same number of values'

    nclusters = 1
    for cluster_level in clusters:
        nclusters = nclusters * len(cluster_level)

    assert nclusters == len_series, 'Series must contain as many values as clusters'

    def leafs(d):
        if len(d.items()) == 0:
            return [ d ]
        else:
            ret = []
            for k, v in d.items():
                ret += leafs(v)

        return ret

    def walk(d, fun):
        if len(d.items()) == 0:
            fun(d)
        else:
            for k, v in d.items():
                walk(v, fun)

    ret = OrderedDict()
    for cluster_level in clusters:
        def insert_cluster(d):
            for cluster in cluster_level:
                d[cluster] = OrderedDict()

        walk(ret, insert_cluster)

    for i, leaf in enumerate(leafs(ret)):
        for k, series_vals in series.items():
            leaf[k] = series_vals[i]

    return ret
