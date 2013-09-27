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

    # Parse results file into something for the render
    res = []
    with(open(results_fn)) as fd:
        for run in json.load(fd)['runs']:
            # Grab the --size=... parameter
            regex = '--size=(\d+)(?:\*(\d+))?(?:\*(\d+))?(?:\*(\d+))?(?:\*(\d+))?(?:\*(\d+))?'
            sizes = []
            for cmd in run['cmd']:
                m = re.match(regex, cmd)
                if m:
                    sizes = [int(size) for size in m.groups() if size]
                    break
            
            # Compress bridge-alias
            #bridge_alias = ''.join([x[0]+x[1] for x in run['bridge_alias'].split('-')])
            #engine_alias = 'native' if 'N/A' == run['engine_alias'] else run['engine_alias']
            bridge_alias, engine_alias = run['bridge_alias'].split('/')
            res.append((
                run['script_alias'],
                bridge_alias,
                engine_alias,
                float(stats(run['times'])[0]),
                int(sizes[0])
            ))
    res = sorted(res)

    results = {}    # Create a dict...
    for script, backend, engine, seconds, size in res:
        label   = "%s/%s" % (backend, engine)
        if not script in results:
            results[script] = {}

        if not label in results[script]:
            results[script][label] = {'times': [], 'size': []}

        results[script][label]['times'].append(seconds)
        results[script][label]['size'].append(size)

    return results

class Graph:
    """
    Baseclass for rendering Matplotlib graphs.
    Does all alot of the annoying work, just override the render(...) method,
    and you are good to go!
    """

    def __init__(
        self,
        output="/tmp",
        file_formats=["pdf"],
        file_postfix='runtime',
        graph_title="Unknown Graph",
        xaxis_label="Problemsize",
        yaxis_label="Time in Seconds"
    ):
        self.graph_title    = graph_title
        self.xaxis_label    = xaxis_label
        self.yaxis_label    = yaxis_label
        self.output         = output
        self.file_formats   = file_formats
        self.file_postfix   = file_postfix

    def prep(self):
        clf()                       # Essential! Othervise the plots will be f**d up!
        figure(1)

        gca().yaxis.grid(True)      # Makes it easier to compare bars
        gca().xaxis.grid(False)
        gca().set_axisbelow(True)

        title(self.graph_title)     # Title and axis labels
        ylabel(self.yaxis_label)    # Label on the y-axis
        xlabel(self.xaxis_label)    # Label on the x-axis

    def render(self):
        raise Exception('YOU ARE DOING IT WRONG!')

    def to_file(self, text):
        fn = self.output +os.sep+ text.lower() +'_'+self.file_postfix
        dname = os.path.dirname(fn)
        bname = re.sub('\W', '_', os.path.basename(fn))
        fn = dname +os.sep+ bname

        try:                            # Create output directory
            os.makedirs(self.output)
        except:
            pass

        for ff in self.file_formats:    # Create the physical files
            savefig("%s.%s" % (fn, ff))

        show()

class Absolute(Graph):
    """
    Create a graph that shows elapsed time on the y-axis and engines on 
    along the x-axis using "bridge_alias/engine_alias" as labels.
    """

    def render(self, script, results, order=None, baseline=None, highest=None):

        if baseline:
            self.yaxis_label='Speedup in relation to "%s"' % baseline

        self.prep()                         # Prep it / clear the drawing board

        data = []       # Restructe the results
        if order:
            for label in order:
                data.append((label, results[label]))
        else:
            data = [(label, results[label]) for label in results]

        bsl  = [res['times'] for lbl, res in data if baseline and lbl == baseline]
        bsl  = bsl[0] if bsl else bsl

        labels = []
        xlow  = None
        xhigh = None
        for label, numbers in data:
            sizes   = numbers['size']

            if not xlow:            # Axis scaling
                xlow = min(sizes)
            if not xhigh:
                xhigh = max(sizes)

            if min(sizes) < xlow:
                xlow = min(sizes)
            if max(sizes) > xhigh:
                xhigh = max(sizes)

            if baseline:
                times = [bsl[c]/number for c, number in enumerate(numbers['times'])]
            else:
                times = numbers['times']
            p = plot(sizes, times, label=label, marker='.')
            labels.append(label)

        if baseline and highest != float(0):
            ylim([0.5, highest+0.1])
        if baseline and highest == float(0):
            ymin, ymax = ylim()
            ylim(ymin=0.9)

        xscale("log")
        xlim([xlow-(xlow/8), xhigh+(xhigh/8)])
        legend(labels, bbox_to_anchor=(0.5, -0.15), loc='upper center', ncol=4, borderaxespad=0., fancybox=True, shadow=True)

        suffix = '_rel' if baseline else '_abs'
        self.to_file(script+suffix)                # Spit them out to file

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
        Absolute(args.output, args.formats, 'runtime', script).render(
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
    args = parser.parse_args()

    main(args)

