#!/usr/bin/env python
import matplotlib
matplotlib.use('Agg')       # Essential for generating graphs "headless".

from pylab import *
import argparse
import glob
import json
import sys
import os

def stats( times ):
    """Returns: (avg, lowest, highest, deviation)"""
    
    return (sum(times)/float(len(times)), max(times), min(times), 0.0)

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
        ints = [ord(x) for x in subject]
    except:
        print "error in lintification!"

    return ints

def gen( benchmark, output ):

    try:
        raw     = json.load(open(benchmark))
        meta    = raw['meta']
        runs    = raw['runs']
    except:
        print "Failed loading benchmark."
        return 1

    bench       = {}
    baselines   = {}
    for mark, engine_lbl, engine, engine_args, cmd, times in runs:

        t_avg, t_max, t_min, t_dev = stats(times)
        if engine:                                  # Results with cphvb enabled.

            if mark in bench:
                bench[mark][engine_lbl] = t_avg
            else:
                bench[mark] = { engine_lbl: t_avg }

        else:                                       # baseline = cphvb is disabled.
            baselines[mark] = (engine_lbl, t_avg)

    for mark in bench:
        
        baseline_lbl, baseline = baselines[mark]
                                                    # Runtime in relation to baseline
        rt = [(engine_lbl, 1/(baseline/bench[mark][engine_lbl])) for engine_lbl in (bench[mark]) ]
        rt.sort(key=lambda x: [lintify(y) for y in x[0].split('_')])
        rt = [(baseline_lbl, baseline/baseline )] + rt

                                                    # Speed-up in relation to baseline
        su = [(engine_lbl, (baseline/bench[mark][engine_lbl])) for engine_lbl in (bench[mark]) ]
        su.sort(key=lambda x: [lintify(y) for y in x[0].split('_')])
        su = [(baseline_lbl, baseline/baseline )] + su

        graphs = [
            ('Runtime', rt),
            ('Speedup', su),
        ]

        for graph, data in graphs:

            lbl = [engine_lbl for engine_lbl, time in data]
            val = [time for engine_lbl, time in data]
            pos = arange(len(val))

            clf()                       # Essential! Without clearing the plots will be messed up!
            figure(1)
            bar(pos, val, align='center')

            ylabel('%s in relation to NumPy' % graph)

            rotation = 'horizontal'     # Assume that there is not enough room vertically
            if len(val)> 4:
                rotation = 'vertical'

            xticks(pos, lbl, rotation=rotation)
            xlabel('Vector Engine')
            title(mark)
            grid(True)
                                        # Output them
            fn = output +os.sep+ mark.lower() +'_'+ graph.lower()
            savefig("%s.pdf" % ( fn ))
            savefig("%s.eps" % ( fn ))
            savefig("%s.png" % ( fn ))
            show()

    return 0

def main( results, output, multi ):

    if multi:

        if not os.path.isdir( results ):
            print "ERR: '%s' is not a directory." % ( results )
            return -1

        if not os.path.isdir( output ):
            print "ERR: '%s' is not a directory." % ( output )
            return -1

        for root, dirs, files in os.walk( results ):
            for fn in [x for x in files if 'json' in x or 'benchmark' in x]:
                r_input     = root +os.sep+ fn
                r_output    = root.replace('results', 'graphs') +os.sep
                if "latest" in fn:
                    r_output = r_output +os.sep+ 'latest'
                gen( r_input, r_output )
        
        return 0

    else:
        return gen( results, output )

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
        '--output',
        dest='output',
        default="graphs",
        help='Where to store generated graphs.'
    )
    args = parser.parse_args()

    res = main( args.results, args.output, args.m )
    print res
