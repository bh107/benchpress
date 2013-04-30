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
        print run["script"],"[", run["bridge"],", ", run["engine"],"]:",  run["times"], np.average( run["times"])
    

if __name__ == "__main__":
    main()
