#!/usr/bin/env python

import json
import argparse
import numpy as np

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("results", help="JSON file containing results")
    args = parser.parse_args()
    data = json.load(open(args.results))
    for run in data["runs"]:
        print "%s [%s, %s, %s]:"%(run["script_alias"], run["bridge_alias"],run["manager_alias"], run["engine"]),
        if len(run["times"]) < 1:
            print "N/A"
        else:
            print run["times"],
            print "%f (%f)"%(np.mean(run["times"]), np.var(run["times"]))

if __name__ == "__main__":
    main()
