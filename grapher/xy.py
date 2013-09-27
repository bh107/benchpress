#!/usr/bin/env python
import matplotlib
matplotlib.use('Agg')       # Essential for generating graphs "headless".

from pylab import *
import argparse
import pprint
import glob
import json
import math
import sys
import os
import re

from parser import from_file as rparse, avg, variance

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

def stats(samples):
    """Returns: (avg, lowest, highest, deviation)"""

    mean = sum(samples)/len(samples)
    return (mean, max(samples), min(samples), 0)

def lintify(text):
    """Create a list of numbers for sorting strings."""

    ints = []

    try:                    # Convert the string "2324" 
        ints = [int(text)]  # to a list with an integer [2325]
    except:
        pass
                            # Convert a string to a list of integers
                            # with "padding". eg:
    try:                    # "hej" to the list of integers:
        ceil    = 10        # [104, 101, 106, 115, 97, 32, 32, 32, 32, 32]
        subject = text[:ceil] + ' '* (ceil-len(text))
        ints    = [ord(x) for x in subject]
    except:
        print "error in lintification!"

    return ints

def parse_results(results_fn):
    """Parses a list of 'perf' output into list of dicts with counter as key."""
    pdata = rparse(results_fn)

    res = []
    for script, bridge, manager, engine, data in pdata:
        print data
        res.append((
            script,
            ''.join((x[0] for x in bridge.split('/'))),
            engine,
            data['sizes'][0],
            avg(data['elapsed'])
        ))
    res = sorted(res)

    results = {}    # Create a dict...
    for script, backend, engine, size, seconds in res:
        label   = "%s/%s" % (backend, engine)
        if not script in results:
            results[script] = {}

        if not label in results[script]:
            results[script][label] = {'times': [], 'size': []}

        results[script][label]['times'].append(seconds)
        results[script][label]['size'].append(size)

    return results


def main(args):

    data = parse_results(args.results) # Get the results from json-file

    highest   = 1.0
    if args.baseline:            # Determine the y-limit
        baselines = {}
        for script in data:
            baselines[script] = data[script][args.baseline]['times']

        for script in data:
            for lbl in data[script]:
                if args.order and lbl not in args.order:
                    continue
                for c, t in enumerate(data[script][lbl]['times']):
                    k = baselines[script][c]/t
                    if k > highest:
                        highest = k
    if args.ylimit:
        highest = float(args.ylimit)

    for script in data:                   # Render them
        Absolute(args.output, args.formats, 'runtime_%s' % args.postfix, script).render(
            script, data[script], args.order, args.baseline, highest
        )

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description = 'Generate graphs showing "bridge_alias/engine_alias" \n'+\
                      'along the x-axis and elapsed time/speedup on the y-axis.'
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
        '--formats',
        default=['pdf'],
        nargs='+',
        choices=[ff for ff in formats]
    )
    parser.add_argument(
        '--baseline',
        default=None,
        help='Baseline on the form: "bridge_alias/engine_alias"'
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
    parser.add_argument(
        '--postfix',
        default='runtime',
        help="Bla bla"
    )
    args = parser.parse_args()

    main(args)

