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

def stats( samples ):
    """Returns: (avg, lowest, highest, deviation)"""

    mean    = sum(samples)/len(samples)
    return (mean, max(samples), min(samples), 0)

def lintify( text ):
    """Create a list of numbers for sorting strings."""

    ints = []

    try:                    # Convert the string "2324" to a list with an integer [2325]
        ints = [int(text)]
    except:
        pass

    try:                    # Convert the string "hej" to a list with integers:
                            # [104, 101, 106, 115, 97, 32, 32, 32, 32, 32]
        ceil    = 10
        subject = text[:ceil] + ' '* (ceil-len(text))
        ints    = [ord(x) for x in subject]
    except:
        print "error in lintification!"

    return ints

def normalize( runs ):

    for r in runs:
        if len(r) == 6:
            yield r + [[]]
        elif len(r) == 7:
            yield r

def parse_perf( perf_tl ):
    """Parses a list of 'perf' output into list of dicts with counter as key."""

    perfs = []
    for perf_t in perf_tl:
        counters = {}
        for m in re.finditer('\s+([0-9,\.]+)\s(\w+-(?:[-\w]+))\s+#', perf_t):
            counters[m.group(2)] = int(m.group(1).replace(',','').replace('.',''))
        perfs.append(counters)
   
    return perfs

def render_graph(mark, graphs, output, file_formats=['pdf']):

    try:
        os.makedirs(output)
    except:
        pass

    for graph, data in graphs:

        lbl = [engine_lbl for engine_lbl, time in data]
        val = [time for engine_lbl, time in data]
        pos = arange(len(val))

        clf()                       # Essential! Without clearing the plots will be messed up!
        figure(1)
        bar(pos, val, align='center')

        ylabel(graph)

        rotation = 'horizontal'     # Assume that there is not enough room vertically
        if len(val)> 4:
            rotation = 'vertical'

        xticks(pos, lbl, rotation=rotation)
        xlabel('Vector Engine')
        title(mark)
        grid(True)
                                    # Output them
        fn = output +os.sep+ mark.lower() +'_'+ graph.lower()
        dname = os.path.dirname(fn)
        bname = re.sub('\W', '_', os.path.basename(fn))
        fn = dname +os.sep+ bname

        for ff in file_formats:
            savefig("%s.%s" % ( fn, ff ))

        show()

def render_mgraph(mark, graphs, output, file_formats=['pdf']):

    try:
        os.makedirs(output)
    except:
        pass

    clf()
    data = dict(graphs)

    rotation = 'horizontal'     # Assume that there is not enough room vertically

    groups  = ('NumPy', 'Score', 'Simple')
    width   = 0.25

    ind     = range(0, len(groups))
    ind0    = [i+width      for i in ind]
    ind1    = [i+width*2    for i in ind]
    ind2    = [i+width*3    for i in ind]
    indt    = [i+width*2.5  for i in ind]
   
    el = [10]*3
    l1 = range(10, 13)
    ll = range(100, 130,10)
    
    el = [t for e,t in data['Runtime']]
    l1 = [t/10 for e,t in data['L1-miss']]
    ll = [t/10 for e,t in data['LL-miss']]

    xlabel('Measurement')
    title(mark)
    grid(True)

    rect0 = bar(ind0, el, width, color='r')
    rect1 = bar(ind1, l1, width, color='g')
    rect2 = bar(ind2, ll, width, color='b')
    
    legend( (rect0[0], rect1[0], rect2[0]), ('WC', 'L1-miss', 'LL-miss'))
    xticks(indt, groups)

    fn = output +os.sep+ mark.lower()       # Output them
    dname = os.path.dirname(fn)
    bname = re.sub('\W', '_', os.path.basename(fn))
    fn = dname +os.sep+ bname

    for ff in file_formats:
        savefig("%s.%s" % ( fn, ff ))

    show()

def gen( benchmark, output ):

    try:
        raw     = json.load(open(benchmark))
        meta    = raw['meta']
        runs    = raw['runs']
    except:
        return [1, "Failed loading benchmark %s." % benchmark]

    scale = 1000000.0

    bench       = {}
    baselines   = {}
    for mark, engine_lbl, engine, engine_args, cmd, times, perf_tl in normalize( runs ):

        perfs = parse_perf( perf_tl )
        l1_miss = stats([perf['L1-dcache-load-misses']/scale for perf in perfs])[0]
        ll_miss = stats([perf['LLC-load-misses']      /scale for perf in perfs])[0]
        t_avg, t_max, t_min, t_dev = stats(times)

        if engine:                                  # Results with cphvb enabled.

            if mark in bench:
                bench[mark][engine_lbl] = {
                    'elapsed': t_avg,
                    'l1_miss': l1_miss,
                    'll_miss': ll_miss
                }
            else:
                bench[mark] = { engine_lbl: {
                    'elapsed': t_avg,
                    'l1_miss': l1_miss,
                    'll_miss': ll_miss
                }}

        else:                                       # baseline = cphvb is disabled.
            baselines[mark] = {
                'label'  : engine_lbl,
                'elapsed': t_avg,
                'l1_miss': l1_miss,
                'll_miss': ll_miss
            }

    for mark in bench:
        
        baseline = baselines[mark]
                                                    # Runtime in relation to baseline
        rrt = [(engine_lbl, 1.0/(baseline['elapsed']/bench[mark][engine_lbl]['elapsed'])) for engine_lbl in (bench[mark]) ]
        rrt.sort(key=lambda x: [lintify(y) for y in x[0].split('_')])
        rrt = [(baseline['label'], 1.0 )] + rrt

                                                    # Speed-up in relation to baseline
        rsu = [(engine_lbl, (baseline['elapsed']/bench[mark][engine_lbl]['elapsed'])) for engine_lbl in (bench[mark]) ]
        rsu.sort(key=lambda x: [lintify(y) for y in x[0].split('_')])
        rsu = [(baseline['label'], 1.0 )] + rsu

                                                    # Runtime
        rt = [(engine_lbl, bench[mark][engine_lbl]['elapsed']) for engine_lbl in (bench[mark]) ]
        rt.sort(key=lambda x: [lintify(y) for y in x[0].split('_')])
        rt = [(baseline['label'], baseline['elapsed'] )] + rt
                                                    # L1-miss
        l1 = [(engine_lbl, bench[mark][engine_lbl]['l1_miss']) for engine_lbl in (bench[mark]) ]
        l1.sort(key=lambda x: [lintify(y) for y in x[0].split('_')])
        l1 = [(baseline['label'], baseline['l1_miss'] )] + l1
                                                    # LL-miss
        ll = [(engine_lbl, bench[mark][engine_lbl]['ll_miss']) for engine_lbl in (bench[mark]) ]
        ll.sort(key=lambda x: [lintify(y) for y in x[0].split('_')])
        ll = [(baseline['label'], baseline['ll_miss'] )] + ll

        graphs = [
            #('Runtime relative to %s' % baseline['label'], rrt),
            #('Speedup in relation to %s' % baseline['label'], rsu),
            ('Runtime', rt),
            ('L1-miss', l1),
            ('LL-miss', ll)
        ]

        #render_graph( mark, graphs, output )
        #render_mgraph( mark, graphs, output )
        render_mgraph( mark, graphs, output, ['png'] )
    
    return (0, None)

def main( results, output, multi, only_latest ):

    if multi:

        if not os.path.isdir( results ):
            return [(-1, "ERR: '%s' is not a directory." % ( results ))]

        if not os.path.isdir( output ):
            return [(-1, "ERR: '%s' is not a directory." % ( output ))]

        res = []
        for root, dirs, files in os.walk( results ):
            for fn in [x for x in files if ('json' in x or 'benchmark' in x) and ('latest' in x or not only_latest)]:
                r_input     = root +os.sep+ fn
                r_output    = root.replace('results', 'graphs') +os.sep
                if "latest" in fn:
                    r_output = r_output +os.sep+ 'latest'
                res.append( gen( r_input, r_output ) )
        
        return res

    else:
        return [gen( results, output )]

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Generate graphs / diagrams from benchmarks.')
    parser.add_argument(
        'results',
        help='Path to benchmark results.'
    )
    parser.add_argument(
        '-m',
        dest='m',
        action="store_true",
        default=False,
        help="Recursively find multiple files."
    )
    parser.add_argument(
        '-l',
        dest='l',
        action="store_true",
        default=False,
        help="Only look for 'latest' when using multiple results."
    )
    parser.add_argument(
        '--output',
        dest='output',
        default="graphs",
        help='Where to store generated graphs.'
    )
    args = parser.parse_args()

    res = [msg for r, msg in main( args.results, args.output, args.m, args.l ) if msg]
    print ''.join( res )
