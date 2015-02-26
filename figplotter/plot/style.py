'''
Created on Jan 19, 2015

@author: Javier Cabezas <javier.cabezas@gmail.com>
'''

import copy
import defaults

from .. import utils


def build_dict(query):
    key, value = query

    ret = {}

    for k, v in value.items():
        names = k.split('::')

        params_name = names[0] + '_params'
        d = utils.Parameter({ key: v })
        if len(names) == 1:
            ret[params_name] = d
        elif len(names) == 2:
            if not ret.has_key(params_name):
                ret[params_name] = {}

            ret[params_name][names[1]] = d
        elif len(names) == 3:
            if not ret.has_key(params_name):
                ret[params_name] = {}
            if not ret[params_name].has_key(names[1]):
                ret[params_name][names[1]] = {}

            ret[params_name][names[1]][names[2]] = d
        else:
            # TODO: fix this
            raise Exception('Query depth greater than 3 is not supported')

    return ret


def expand_query_level(query, val, level, selectors_level):
    fields = query.split('::')

    term = fields[level]

    query_level = []

    if term == '*':
        for valid_term in selectors_level:
            query_level.append(('::'.join(fields[:level] + [ valid_term ] + fields[level + 1:]), copy.deepcopy(val)))
    else:
        assert term in selectors_level, 'Term "{}" used in query "{}" not valid. Valid terms are "{}"' % (term, query, selectors_level)

        query_level.append((query, copy.deepcopy(val)))

    return query_level


def expand_query(query, val, levels, selectors):
    queries = [ (query, val) ]
    for idx in range(levels):
        queries_level = []
        for query, val in queries:
            queries_level += expand_query_level(query, val, idx, selectors[idx])

        queries = queries_level

    return queries


def sort_queries(style, levels):
    # query_histo = { idx: [] for idx in range(levels + 1) }
    query_histo = {}

    for query, val in style.items():
        fields = query.split('::')

        score = 0
        score_level = 10**(levels - 1)
        for idx in range(levels):
            if fields[idx] == '*':
                score += score_level

            score_level /= 10

        if not query_histo.has_key(score):
            query_histo[score] = []

        query_histo[score].append((query, val))

    sorted_queries = []

    for k in sorted(query_histo.keys(), reverse = True):
        sorted_queries += query_histo[k]

    return sorted_queries


def generate_params(style, selectors, style_name = None, fun_name = None):
    levels = 0
    for query, _ in style.items():
        fields = query.split('::')
        if levels == 0:
            levels = len(fields)
        else:
            assert levels == len(fields), 'Selectors length do not match'

    assert levels == 0 or levels == len(selectors), \
           'Selectors do not match queries depth "{} vs {}"'.format(levels, len(selectors))

    sorted_queries = sort_queries(style, levels)

    # Expand queries
    query_list = []
    for query, val in sorted_queries:
        expanded = expand_query(query, val, levels, selectors)

        query_list += expanded

    ret = {}
    if fun_name is not None:
        default_queries = defaults.get_function_defaults(fun_name, selectors, style_name)
        for query in default_queries:
            series_params = build_dict(query)
            utils.update(ret, series_params)

    for query in query_list:
        series_params = build_dict(query)
        utils.update(ret, series_params)

    return ret