#!/usr/bin/env python
import argparse
import pprint
import json

from parser import from_file, from_str, avg
from parser import standard_deviation as std

def raw(results):
    pprint.pprint(results)

def parsed(results):
    pprint.pprint(from_str(results))

def times(results):
    for script, bridge, manager, engine, res in from_str(results):
        print "%s [%s, %s, %s]:" % (script, bridge, manager, engine),
        if 'elapsed' not in res or len(res['elapsed']) < 1:
            print "N/A"
        else:
            print res["elapsed"],"%f (%f) %d"%(avg(res["elapsed"]), std(res["elapsed"]), len(res['elapsed']))

def main():
    printers = {'raw':raw, 'times':times, 'parsed': parsed}

    parser = argparse.ArgumentParser()
    parser.add_argument("results", help="JSON file containing results")
    parser.add_argument(
        "--printer",
        choices=[p for p in printers],
        default='times',
        help="How to print results."
    )
    args = parser.parse_args()

    printer = printers[args.printer]
    printer(open(args.results).read())

if __name__ == "__main__":
    main()
