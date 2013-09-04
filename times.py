#!/usr/bin/env python

import json
import argparse
import numpy as np
from parser import from_file as rparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("results", help="JSON file containing results")
    args = parser.parse_args()

    for script, bridge, manager, engine, res in rparse(args.results):
        print "%s [%s, %s, %s]:" % (script, bridge, manager, engine),
        if 'elapsed' not in res or len(res['elapsed']) < 1:
            print "N/A"
        else:
            print "%f (%f)"%(np.mean(res["elapsed"]), np.var(res["elapsed"]))

if __name__ == "__main__":
    main()
