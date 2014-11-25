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

def csv(results):
    i = 1
    for script, bridge, manager, engine, res in from_str(results):
        print "%d, %s, %s, %s, %s, %f, %f"%(i, script, bridge, manager, 
		engine, avg(res["elapsed"]), std(res["elapsed"]))
        i += 1

def troels(results):
    results = json.loads(results)['runs']
    i = 0
    for run in results:
        i += 1
        script = run['script_alias']
        total_time = filter(None,run['elapsed'])
        timings = run['timings']
        if i == 1:
            tk = timings.keys()
            print "#, Script, Total time, Total time dev., %s"%(", ".join(map(lambda (a,b):a+b,zip(tk,map(lambda s: " ,"+s+" dev.",tk)))))
        print ("%d, %s, %f, %f, "+(", ".join(map(lambda s: "%f, %f",tk))))%((i,script,avg(total_time),std(total_time))+sum(map(lambda k: (avg(timings[k]),std(timings[k])),tk),()))
            
    

def main():
    printers = {'raw':raw, 'times':times, 'parsed': parsed, 'csv': csv, 'troels': troels}

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
