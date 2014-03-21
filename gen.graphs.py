#!/usr/bin/env python
from copy import copy, deepcopy
import argparse
import pkgutil
import pprint

#from grapher.graph import *
#from grapher.scale import *
from parser import from_file, avg, variance

formats = ['png', 'pdf', 'eps']

colors  = [
    "#B3E2CD", "#FDCDAC", "#CBD5E8",
    "#F4CAE4", "#E6F5C9", "#FFF2AE",
    "#F1E2CC", "#CCCCCC",
    "#B3E2CD", "#FDCDAC", "#CBD5E8",
    "#F4CAE4", "#E6F5C9", "#FFF2AE",
    "#F1E2CC", "#CCCCCC",
    "#B3E2CD", "#FDCDAC", "#CBD5E8",
    "#F4CAE4", "#E6F5C9", "#FFF2AE",
    "#F1E2CC", "#CCCCCC",
]

hatches = [
    "\\", "+", "o", "/", "-", "O",
    "\\", "+", "o", "/", "-", "O",
    "\\", "+", "o", "/", "-", "O",
    "\\", "+", "o", "/", "-", "O",
    "\\", "+", "o", "/", "-", "O",
]

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

    data    = from_file(args.results)               # Get data from json-file
    grouped = group(data, 'elapsed', args.warmups)  # Group by benchmark and "label"

    if args.baseline:                               # Normalize by "baseline"
        normalized = normalize(grouped, 'elapsed', args.baseline)
    else:
        normalized = grouped

    #
    #   This is bypass stuff
    #

    for format in args.formats:
        if args.type == 'bypass_overhead':
            graph = args.graph_module(
                args.output, args.formats, args.postfix,
                "overhead", 'Application', 'Slowdown'
            )
            graph.render(data, args.order, args.baseline)
        else:
            graph = args.graph_module(
                args.output, [format], args.postfix,
                'latency', 'Injected Latency (in ms)', 'Speeddown'
            )
            graph.render(grouped, args.order, args.baseline)

if __name__ == "__main__":

    graph_types = {}    # Auto-load all graph-modules from grapher/*
                        # The graph-class must be a capilized version of the
                        # filename
    for _, module, _ in pkgutil.iter_modules(['grapher']):
        if module == 'graph':
            continue

        module_caps = module.capitalize()
        m = __import__("grapher.%s" % module, globals(), locals(), [module_caps], -1)

        graph_types[module] = m.__dict__[module_caps]

    parser = argparse.ArgumentParser(
        description = 'Generate different types of graphs.'
    )
    parser.add_argument(
        'results',
        help='Path to benchmark results.'
    )
    parser.add_argument(
        '--output',
        default="graphs",
        help='Where to store generated graphs.'
    )
    parser.add_argument(
        '--postfix',
        default='runtime',
        help="Append this to the filename of the generated graph(s)."
    )
    parser.add_argument(
        '--formats',
        default=['png'],
        nargs='+',
        help="Output file-format(s) of the generated graph(s)."
    )
    parser.add_argument(
        '--type',
        default=[[gt for gt in graph_types][0]],
        nargs=1,
        choices=[gt for gt in graph_types],
        help="The type of graph to generate"
    )
    parser.add_argument(
        '--warmups',
        default=0,
        type=int,
        help="Specify the amount of samples from warm-up rounds."
    )
    parser.add_argument(
        '--baseline',
        default=None,
        help='Baseline label for relative graphs.'
    )
    parser.add_argument(
        '--order',
        default=None,
        nargs='+',
        help='Ordering of the ticks.'
    )
    parser.add_argument(
        '--ylimit',
        default=None,
        help="Max value of the y-axis"
    )

    args = parser.parse_args()
    args.type = args.type.pop()
    args.graph_module = graph_types[args.type]

    main(args)


