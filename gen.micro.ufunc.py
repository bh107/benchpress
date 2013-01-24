#!/usr/bin/env python
import matplotlib
matplotlib.use('Agg')       # Essential for generating graphs "headless".

from pylab import *
import argparse
import glob
import json
import sys
import os
import re

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

def avg( times ):
    return sum(times)/len(times)

def gen( baseline, alternative, output ):

    try:
        bl  = json.load(open(baseline))
        alt = json.load(open(alternative))
    except Exception as e:
        return [1, "Failed loading on of the benchmarks %s, %s. [ERR: %s]." % (baseline, alternative,e)]

    lbl = []
    val = []
    pos = []

    for opcode, typesig, times, value, err, bohrium in (res for res in bl if res[0] == "BH_POWER") and not bohrium:
        avg_t = avg( times )
        text = ','.join([t.lower().replace('bh_', '').replace('float', 'f').replace('uint','u').replace('int','i').replace('complex','c') for t in typesig])

        for a_avg in (avg(result[2]) for result in alt if result[0] == opcode and result[1] == typesig):
            diff = avg_t-a_avg
            lbl.append( text )
            val.append( diff )

    pos = arange(len(val))
    clf()                       # Essential! Without clf() the plots will be messed up!
    rotation = 'horizontal'     # Assume that there is not enough room vertically
    if len(val)> 4:
        rotation = 'vertical'

    figure(1)
    bar(pos, val, align='center')

    ylabel('Runtime diff of %s in relation to NumPy' % opcode)
    xticks(pos, lbl, rotation=rotation)
    xlabel('Instruction')
    grid(True)
                                # Output them
    savefig("/tmp/%s.pdf" % opcode)
    show()

    return [(0, None)]

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Generate graphs / diagrams from benchmarks.')
    parser.add_argument(
        'baseline',
        help='Path to benchmark results.'
    )
    parser.add_argument(
        'alternative',
        help='Path to benchmark results.'
    )
    parser.add_argument(
        '--output',
        dest='output',
        default="graphs",
        help='Where to store generated graphs.'
    )
    args = parser.parse_args()

    print gen( args.baseline, args.alternative, args.output )
