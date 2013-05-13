#!/usr/bin/env python

import tempfile
import argparse
import json
import os
import sys
import re

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Merge two benchmark results.')
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
        j1.update(j2)
        f3.write(json.dumps(j1, indent=4))
        print "Merged %s and %s into %s"%(f1.name, f2.name, f3.name)
