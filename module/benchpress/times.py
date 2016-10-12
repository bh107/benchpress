#!/usr/bin/env python
import argparse
import pprint
import json
import press

from result_parser import from_file, from_str, avg
from result_parser import standard_deviation as std

def stack_label(stack):
    """Returns a descriptive label of the stack"""
    ret = ""
    for component in stack:
        ret += "%s/"%component[0]
    return ret[:-1] #We remove the last "/" before returning

def raw(results):
    pprint.pprint(results)

def parsed(results):
    pprint.pprint(from_str(results))

def times(results, baseline=None):

    baselines = {}
    if baseline is not None:
        for script, bridge, res in from_str(results):
            if baseline in bridge:
                assert(script not in baselines)
                baselines[script] = res

    for script, bridge, res in from_str(results):
        print "%s %s [%s]:" % (script, bridge, stack_label(res['stack'])),

        if 'elapsed' not in res or len(res['elapsed']) < 1:
            elapsed = None
        else:
            elapsed = res['elapsed']

        # Normalize time when using a baseline
        if baseline is not None:
            if script in baselines:
                for i in range(len(elapsed)):
                    elapsed[i] = avg(baselines[script]['elapsed']) / elapsed[i]
            else:
                elapsed = None

        if elapsed is None:
            print "N/A"
        else:
            print elapsed,"%f (%f) %d"%(avg(elapsed), std(elapsed), len(elapsed))


def fusepricer(results):
    out = ""
    for script, bridge, res in from_str(results):
        s = "%s ["%script
        for label, name, env in res['stack']:
            s += "%s/"%label
        out += "%s]"%s[:-1]
        if 'fuseprice' not in res:
            out += "N/A"
        else:
            out += " %s"%str(res['fuseprice'])
        out += "\n"
    out = out.split("\n")
    out.sort()
    print "\n".join(out)

def main():
    printers = {'times':times, 'pricer':fusepricer}

    parser = argparse.ArgumentParser()
    parser.add_argument("results", help="JSON file containing results")
    parser.add_argument(
        "-p", "--printer",
        choices=[p for p in printers],
        default='times',
        help="How to print results."
    )
    parser.add_argument(
        "--baseline",
        metavar="BRIDGE_LABEL",
        help="Set a baseline."
    )
    args = parser.parse_args()

    printer = printers[args.printer]
    if args.baseline:
        printer(open(args.results).read(), args.baseline)
    else:
        printer(open(args.results).read())

