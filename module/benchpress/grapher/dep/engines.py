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
            # Compress bridge-alias
            #bridge_alias = ''.join([x[0] for x in run['bridge_alias'].split('-')])
            #engine_alias = 'native' if 'N/A' == run['engine_alias'] else run['engine_alias']
            bridge_alias, engine_alias = run['bridge_alias'].split('/')
            res.append((
                run['script_alias'],
                bridge_alias,
                engine_alias,
                stats(run['times'])[0]
            ))

    res = sorted(res)

    labels = {}
    values = {}
    for r in res:
        script  = r[0]
        label   = "%s/%s" % (r[1], r[2])
        value   = float(r[3])
        if script in labels:
            labels[script].append(label)
            values[script].append(value)
        else:
            labels[script] = [label]
            values[script] = [value]

    return (labels, values)

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
        xaxis_label="Bridge/Engine",
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

    def render(self, script, labels, values, order):

        self.prep()                         # Prep it / clear the drawing board

        if order:                           # Order and limit the labels
            data = dict(zip(labels, values))
            labels = []
            values = []
            for label in order:
                labels.append(label)
                values.append(data[label])

        rotation = 'horizontal'             # Assume that there is not enough room vertically
        if len(values)>= 4:                  # so change orientation of labels
            rotation = 'vertical'

        pos = arange(len(values))           # Output values as bars
        for p in pos:
            bar(
                pos[p],
                values[p], 
                align='center',
                color=colors[p],
                hatch=hatches[p]
            )

        xticks(pos, labels, rotation=rotation)  # Output labels
        #ymin, ymax = ylim()
        ylim(ymin=0.9, ymax=2.4)

        self.to_file(script)                # Spit them out to file

class Speedup(Absolute):
    """
    Create a graph that shows speedup on the y-axis and engines on 
    along the x-axis using "bridge_alias/engine_alias" as labels.
    "Baseline" is a string on the form: "bridge_alias/engine_alias".
    """

    def render(self, baseline, script, labels, values, order):

                                            # Get index of baseline label
        bl_index = [c for c, lable in enumerate(labels) if lable == baseline]
        if not bl_index:
            raise Exception('Baseline label was not found!')
        bl_index = bl_index[0]

        bl_label = labels.pop(bl_index)     # Remove baseline label from labels
        bl_value = values.pop(bl_index)     # Remove baseline value from values

                                            # Turn elapsed time into speedup in
                                            # relation to bl_value
        values = [bl_value/v for v in values]

        values.insert(0, 1.0)               # Prepend baseline "value"
        labels.insert(0, bl_label)          # Prepend baseline label



        Absolute.render(self, script, labels, values, order)

def main(results, baseline, order, output, file_formats):

    labels, values = parse_results(results) # Get the results from json-file

    for script in labels:                   # Render them
        if baseline:
            Speedup(
                output,
                file_formats,
                'speedup',
                script,
                yaxis_label='Speedup in relation to "%s"' % baseline,

            ).render(
                baseline, script, labels[script], values[script], order
            )
        else:
            Absolute(output, file_formats, 'runtime', script).render(
                script, labels[script], values[script], order
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
    args = parser.parse_args()

    main(args.results, args.baseline, args.order, args.output, args.formats)

