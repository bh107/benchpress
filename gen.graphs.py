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

class Graph:
    """
    Baseclass for rendering Matplotlib graphs.
    Does alot of the annoying work, just override the render(...) method,
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

    def to_file(self, text):        # Creates the output-file.

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
            self.yaxis_label='In relation to "%s"' % baseline

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
            ylim([0.5, highest+1])
        if baseline and highest == float(0):
            ymin, ymax = ylim()
            ylim(ymin=0.9)

        xscale("log")
        xlim([xlow-(xlow/8), xhigh+(xhigh/8)])
        legend(labels, bbox_to_anchor=(0.5, -0.15), loc='upper center', ncol=4, borderaxespad=0., fancybox=True, shadow=True)
        ymin, ymax = ylim()
        yticks([x for x in xrange(int(ymin+1), int(ymax)+3, 3)])

        suffix = '_rel' if baseline else '_abs'
        self.to_file(script+suffix)                # Spit them out to file

def group(data, key, warmups):
    """
    Group the dataset by benchmark and 'label'::
        results[script][label] = {
            'avg': [], 
            'var': [],
            'wup': [],
            'size': []
        }
    """

    res = []
    for script, backend, manager, engine, sample in data:

        if warmups >= len(sample[key]):
            raise Exception("You have indicated more warmups than samples+1: "
                            "%d < %d!" %(warmups, len(sample[key])))
        res.append((
            script,
            backend,
            manager,
            engine,
            sample['sizes'].pop(0),
            avg(sample[key][:warmups]),
            avg(sample[key][warmups:]),
            variance(sample[key][warmups:])
        ))
    res = sorted(res)

    results = {}    # This is what will be graphed...
    for script, backend, manager, engine, size, sample_wup, sample_avg, sample_var in res:
        label   = "%s/%s" % (backend, engine)
        if not script in results:
            results[script] = {}

        if not label in results[script]:
            results[script][label] = {key: {'avg': [], 'var': [], 'wup': []}, 'size': []}

        results[script][label]['size'].append(size)
        results[script][label][key]['wup'].append(sample_wup)
        results[script][label][key]['avg'].append(sample_avg)
        results[script][label][key]['var'].append(sample_var)

    return results

def normalize(data, key, baseline):
    """Normalize "grouped" data in relation to ''baseline''."""

    baselines = {}
    for script in data:
        pprint.pprint(data[script][baseline])
        baselines[script] = data[script][baseline][key]

    for script in data:
        for label in data[script]:
            val_avg = []
            for c, t in enumerate(data[script][label][key]['avg']):
                val_avg.append(baselines[script]['avg'][c]/t)
            data[script][label][key]['avg'] = val_avg

    return data

def ordering(data, order=None):
    """Order a data-set, switch from dict to list."""

    ordered_data = {}

    default_order = []      # Default order
    for script in data:
        for label in data[script]:
            default_order.append(label)

    order = order if order else default_order

    for script in data:
        if script not in ordered_data:
            ordered_data[script] = []
        for label in order:
            ordered_data[script].append((label, data[script][label]))

    return ordered_data

def main(args):

    data        = from_file(args.results)                       # Get data from json-file
    grouped     = group(data, 'elapsed', args.warmups)          # Group by benchmark and "label"
    normalized  = normalize(grouped, 'elapsed', args.baseline)  # Normalize by "baseline"
    ordered     = ordering(normalized, args.order)              # And order / filter

    pprint.pprint(ordered)

if __name__ == "__main__":

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
        default=['pdf'],
        nargs='+',
        help="Output file-format(s) of the generated graph(s).",
        choices=[ff for ff in formats]
    )
    parser.add_argument(
        '--type',
        default='scale',
        nargs=1,
        choices=['scale', 'problemsize', 'benchmark'],
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


    main(args)


