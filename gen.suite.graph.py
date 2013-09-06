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

from parser import from_file as rparse

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

    mean = sum(samples)/float(len(samples))
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
            savefig("%s.%s" % (fn, ff), bbox_inches='tight')

        show()

class Absolute(Graph):
    """
    Create a graph that shows elapsed time on the y-axis and engines on 
    along the x-axis using "bridge_alias/engine_alias" as labels.
    """

    def render(self, script, results, order=None, baseline=None, highest=None):

        self.graph_title    = "Benchmark Suite"
        self.graph_title    = ""
        self.xaxis_label    = "Benchmark"
        self.xaxis_label    = ""
        self.yaxis_label    = "Speedup in relation to Python/NumPy"

        self.prep()
        scripts, data = results
       
        labels          = []
        times_ordered   = []

        for label in order:
            times_ordered.append((label, data[label]))
            labels.append(label)

        rects = []
        plots = []
        for c, (label, times) in enumerate(times_ordered):
            width = 0.25
            ind   = [x+width*c+0.6 for x in range(len(times))]
            rect = bar(ind, times, width, color=colors[c])
            rects.append(rect)

        rs = [r[0] for r in rects]

        rotation = "vertical"
        legend(rs, labels,bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=3,
               mode="expand", borderaxespad=0., fancybox=True, shadow=True)

        ylim(ymin=0.9)
        xticks(ind, rotation=rotation)
        gca().set_xticklabels(scripts)

        self.to_file(script)                # Spit them out to file

def filter_data(data, baseline, exclude=[]):
    scripts = []
    times  = {}

    prev = None
    baseline = 1.0
    for script, bridge, manager, engine, res in data:

        if script in exclude:
            continue

        seconds = sum(res['elapsed'])/float(len(res['elapsed']))
        label   = "%s" % (bridge.split("/")[1])

        if script != prev:
            scripts.append(script)
        
        if label not in times:
            times[label] = [seconds]
        else:
            times[label].append(seconds)

        prev = script

    ret = (scripts, times)

    return ret

def main(args):
    scripts, times = data = filter_data(rparse(args.results), args.baseline, args.exclude) # Get the results from json-file
    
    if args.baseline and args.baseline in times:    # Normalize
        baseline = times[args.baseline]
        del times[args.baseline]
        for label in times:
            for c, elapsed in enumerate(times[label]):
                times[label][c] = baseline[c] / times[label][c]

    highest = 1.0
    for label in times:
        if times[label] > highest:
            highest = times[label]

    if args.ylimit:
        highest = float(args.ylimit)

    Absolute(args.output, args.formats, 'runtime', 'benchmarks').render(
        args.postfix, data, args.order, args.baseline, highest
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
        '--exclude',
        default=[],
        nargs='+',
        help='Exclude these benchmarks.'
    )
    parser.add_argument(
        '--postfix',
        default='runtime',
        help="Bla bla"
    )

    parser.add_argument(
        '--ylimit',
        default=None,
        help="Max value of the y-axis"
    )
    args = parser.parse_args()

    main(args)

