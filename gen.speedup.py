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

colors = [
    "#1B9E77", "#D95F02", "#7570B3",
    "#66A61E", "#E7298A", "#E6AB02",
]

hatches = ["\\", "+", "o", "/", "-", "0"]

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

def parse_perf( perf_tl ):
    """Parses a list of 'perf' output into list of dicts with counter as key."""

    perfs = []
    for perf_t in perf_tl:
        counters = {}
        for m in re.finditer('\s+([0-9,\.]+)\s(\w+-(?:[-\w]+))\s+#', perf_t):
            counters[m.group(2)] = int(m.group(1).replace(',','').replace('.',''))
        perfs.append(counters)
   
    return perfs

def render_abs(script, labels, values, output="/tmp", file_formats=['pdf']):
    pos = arange(len(values))


    clf()                       # Essential! Othervise the plots will be f**d up!
    figure(1)

    for p in pos:
        bar(
            pos[p],
            values[p], 
            align='center',
            color=colors[p],
            hatch=hatches[p]
        )

    ylabel('Time in seconds')

    rotation = 'horizontal'     # Assume that there is not enough room vertically
    if len(values)> 4:
        rotation = 'vertical'

    def hahaha( text ):
        return re.search('\d+$', text).group(0)

    #lbl = [hahaha(l) for l in labels if '_' in l]
    lbl = labels

    xticks(pos, lbl, rotation=rotation)
    xlabel('Engine')
    title(script)

    gca().yaxis.grid(True)
    gca().xaxis.grid(False)
    gca().set_axisbelow(True)
                                # Output them
    fn = output +os.sep+ script.lower() +'_runtime'
    dname = os.path.dirname(fn)
    bname = re.sub('\W', '_', os.path.basename(fn))
    fn = dname +os.sep+ bname

    try:                        # Create output directory
        os.makedirs(output)
    except:
        pass

    for ff in file_formats:     # Create the physical files
        savefig("%s.%s" % ( fn, ff ))

    show()

def main(results, output, file_formats):

    # Parse results file into something for the render
    res = []
    with(open(results)) as fd:
        for run in json.load(fd)['runs']:
            if (run['bridge_alias'] == "bohrium-numpy"):
                tmp = (run['script_alias'], 
                       'bh', 
                       run['engine'],
                       stats(run['times'])[0]
                )
            else:
                tmp = (run['script_alias'], 
                       'py', 
                       'numpy',
                       stats(run['times'])[0]
                )
            res.append(tmp)

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

    for script in labels:
        render_abs(
            script,
            labels[script],
            values[script],
            output,
            file_formats
        )

    return [(True, "")]

if __name__ == "__main__":

    formats = ['png', 'pdf', 'eps']

    parser = argparse.ArgumentParser(description='Generate graphs / diagrams from benchmarks.')
    parser.add_argument(
        'results',
        help='Path to benchmark results.'
    )
    parser.add_argument(
        '--output',
        dest='output',
        default="graphs",
        help='Where to store generated graphs.'
    )
    parser.add_argument(
        '--format',
        dest='f',
        default='pdf',
        choices=[ff for ff in formats]
    )
    args = parser.parse_args()
    res = [msg for r, msg in main(
        args.results, args.output, [args.f]) if msg
    ]
    print ''.join( res )
