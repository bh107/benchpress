#!/usr/bin/env python
from copy import copy, deepcopy
import argparse
import pkgutil
import pprint
import json 

#from grapher.graph import *
#from grapher.scale import *
from result_parser import from_file, avg, variance

formats = ['png', 'pdf', 'eps']

def group(data, key, warmups):

    res = []
    for script, backend, manager, engine, sample in data:

        if len(sample[key]) == 0:
            print "Ignoring: %s (%s, %s, %s)" % (script, backend, manager, engine)
            continue

        if warmups >= len(sample[key]):
            raise Exception("You have indicated more warmups than samples+1: "
                            "%d < %d!" %(warmups, len(sample[key])))
        res.append((
            script,
            backend,
            manager,
            engine,
            sample['sizes'].pop(0),
            {
            'wup':  avg(sample[key][:warmups]),
            'avg':  avg(sample[key][warmups:]),
            'var':  variance(sample[key][warmups:])
            }
        ))
    res = sorted(res)

    results = {}    # This is what will be graphed...
    for script, backend, manager, engine, sizes, sample in res:
        label   = "%s/%s/%s" % (backend, manager, engine)
        if not script in results:
            results[script] = {}

        if not label in results[script]:
            results[script][label] = {key: {'avg': [], 'var': [], 'wup': []}, 'size': []}

        results[script][label]['size'].append(sizes)
        results[script][label][key]['wup'].append(sample['wup'])
        results[script][label][key]['avg'].append(sample['avg'])
        results[script][label][key]['var'].append(sample['var'])

    return results

def normalize(data, key, baseline):
    """Normalize "grouped" data in relation to ''baseline''."""

    baselines = {}
    for script in data:
        baselines[script] = deepcopy(data[script][baseline][key])

    speedup = {}

    for script in data:
        if script not in speedup:
            speedup[script] = {}
        for label in data[script]:
            if label not in speedup[script]:
                speedup[script][label] = []
            for c, t in enumerate(data[script][label][key]['avg']):
                speedup[script][label].append(baselines[script]['avg'][c]/t)

    for script in data:
        for label in data[script]:
            data[script][label][key]['avg'] = speedup[script][label]

    return data

def ordering(data, order=None):
    """Order a data-set, switch from dict to list."""

    ordered_data = {}
    default_order = []      # Default order
    for script in data:
        for label in data[script]:
            default_order.append(label)
        break

    order = order if order else default_order

    for script in data:
        if script not in ordered_data:
            ordered_data[script] = []
        for label in order:
            ordered_data[script].append((label, data[script][label]))

    return ordered_data

def main(args):

    raw = json.load(open(args.results))
    data = from_file(args.results)               # Get data from json-file

    for format in args.formats:
        graph = args.graph_module(
            args.output, args.formats, args.postfix,
            graph_title = "Something",
            xaxis_label = "Threads",
            yaxis_label = "Wall-Clock in Seconds"
        )
        graph.render(raw, data, args.order, args.baseline)

