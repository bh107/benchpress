#!/usr/bin/env python

import tempfile
import argparse
import json
import os
import sys
import re


def identical(run1, run2):
    """Check if two benchmark runs are identical"""
    for k,v in run1.iteritems():
        if v != run2[k] and k != 'times' and k != 'slurm' and k != 'envs':
            return False
    return True

def unique(run, runs):
    """Check if the run exist in runs"""
    for r in runs:
        if identical(run, r):
            return False
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Merge two benchmark results. NB: All meta data is taken from the first json-file.')
    parser.add_argument(
        'file1',
        help='The first json file to merge.'
    )
    parser.add_argument(
        'file2',
        help='The second json file to merge.'
    )
    parser.add_argument(
        'output',
        help='The output file.'
    )
    args = parser.parse_args()

    with open(args.file1, 'r') as f1,open(args.file2, 'r') as f2,open(args.output, 'w') as f3:
        j1 = json.load(f1)
        j2 = json.load(f2)

        out = []
        #Check for unique runs in r1
        for r1 in j1['runs']:
            if unique(r1,j2['runs']):
                out.append(r1)
        #Check for unique runs in r2
        for r2 in j2['runs']:
            if unique(r2,j1['runs']):
                out.append(r2)
        #Merge shared runs
        for r1 in j1['runs']:
            for r2 in j2['runs']:
                if identical(r1, r2):
                    t = r1.copy()
                    t['times'] += r2['times']
                    out.append(t)
                    break

        j1['runs'] = out    #We use the meta-data from the first file
        f3.write(json.dumps(j1, indent=4))
        print "Merged %s and %s into %s"%(f1.name, f2.name, f3.name)
