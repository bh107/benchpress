#!/usr/bin/env python
import matplotlib
matplotlib.use('Agg')       # Essential for generating graphs "headless".

from pylab import *
import argparse
import pprint
import glob
import json
import math
import sys
import os
import re

def stats( samples ):
    """Returns: (avg, lowest, highest, deviation)"""

    mean    = sum(samples)/len(samples)
    return (mean, max(samples), min(samples), 0)

def lintify( text ):
    """Create a list of numbers for sorting strings."""

    ints = []

    try:                    # Convert the string "2324" to a list with an integer [2325]
        ints = [int(text)]
    except:
        pass
                            # Convert a string to a list of integers with padding. eg:
    try:                    # "hej" to the list of integers:
        ceil    = 10        # [104, 101, 106, 115, 97, 32, 32, 32, 32, 32]
        subject = text[:ceil] + ' '* (ceil-len(text))
        ints    = [ord(x) for x in subject]
    except:
        print "error in lintification!"

    return ints


def parse_perf( perf_tl ):
    """Parses a list of 'perf' output into list of dicts with counter as key."""

    perfs = []
    for perf_t in perf_tl:
        counters = {}
        for m in re.finditer('\s+([0-9,\.]+)\s(\w+-(?:[-\w]+))\s+#', perf_t):
            counters[m.group(2)] = int(m.group(1).replace(',','').replace('.',''))
        perfs.append(counters)
   
    return perfs

def render_abs_graph(mark, results, baseline, comp=None, output="/tmp", file_formats=['pdf']):

    if comp:
        results.sort(comp)

    lbl = [engine_lbl for (engine_lbl,_) in results]
    val = [result['elapsed'] for (engine_lbl, result) in results]
    pos = arange(len(val))

    clf()                       # Essential! Without clearing the plots will be messed up!
    figure(1)
    bar(pos, val, align='center', color="#1B9E77")

    ylabel('Time in seconds')

    rotation = 'horizontal'     # Assume that there is not enough room vertically
    if len(val)> 4:
        rotation = 'vertical'

    xticks(pos, lbl, rotation=rotation)
    xlabel('Vector Engine')
    title(mark)

    gca().yaxis.grid(True)
    gca().xaxis.grid(False)
    gca().set_axisbelow(True)

                                # Output them
    fn = output +os.sep+ mark.lower() +'_runtime'
    dname = os.path.dirname(fn)
    bname = re.sub('\W', '_', os.path.basename(fn))
    fn = dname +os.sep+ bname

    try:
        os.makedirs(output)
    except:
        pass

    for ff in file_formats:
        savefig("%s.%s" % ( fn, ff ))

    show()



def render_rel_graph(mark, results, bl_eng, comp, output, file_formats=['pdf']):

    if comp:
        results.sort(comp)

    bl_lbl, bl_res = [(engine_lbl, res) for engine_lbl, res in results if engine_lbl.lower() == bl_eng.lower()][0]

    lbl = [bl_lbl]
    lbl += [engine_lbl for (engine_lbl,_) in results if engine_lbl != bl_lbl]

    val = [1.0]
    val += [bl_res['elapsed']/result['elapsed'] for (engine_lbl, result) in results if engine_lbl != bl_lbl]
    pos = arange(len(val))

    clf()                       # Essential! Without clearing the plots will be messed up!
    figure(1)
    bar(pos, val, align='center', color="#1B9E77")

    ylabel('Speedup in relation to %s' % bl_eng)

    rotation = 'horizontal'     # Assume that there is not enough room vertically
    if len(val)> 4:
        rotation = 'vertical'

    xticks(pos, lbl, rotation=rotation)
    xlabel('Vector Engine')
    title(mark)

    gca().yaxis.grid(True)
    gca().xaxis.grid(False)
    gca().set_axisbelow(True)

                                # Output them
    fn = output +os.sep+ mark.lower() +'_speedup'
    dname = os.path.dirname(fn)
    bname = re.sub('\W', '_', os.path.basename(fn))
    fn = dname +os.sep+ bname

    try:
        os.makedirs(output)
    except:
        pass

    for ff in file_formats:
        savefig("%s.%s" % ( fn, ff ))

    show()

def render_grpmark(mark, data, baseline, comp, output, file_formats=['pdf']):

    try:
        os.makedirs(output)
    except:
        pass

    clf()
    data = dict(data)

    benchmarks  = ['Black Scholes',  'Jacobi Iterative - Reduce', 'kNN', 'Shallow Water']
    engines     = [engine for engine in ['NumPy', 'Simple', 'Score'] if engine != baseline]

    rotation = 'horizontal'
    width    = 0.25

    measure  = 'elapsed'

    ind     = range(0, len(benchmarks))
    ind0    = [i+width      for i in ind]
    ind1    = [i+width*2    for i in ind]
    ind2    = [i+width*3    for i in ind]
    ind3    = [i+width*4    for i in ind]

    if baseline:
        indt    = [i+0.1+width*2.5  for i in ind]
    else:
        indt    = [i+width*2.5  for i in ind]
     
    np = [v['elapsed'] for benchmark in benchmarks for e,v in data[benchmark] if e == 'numpy' ]
    si = [v['elapsed'] for benchmark in benchmarks for c, (e,v) in enumerate(data[benchmark]) if e == 'simple']
    sc = [v['elapsed'] for benchmark in benchmarks for c, (e,v) in enumerate(data[benchmark]) if e == 'score']

    if baseline:
        for i in xrange(0, len(np)):
            si[i] = np[i]/si[i]
            sc[i] = np[i]/sc[i]

    if baseline:
        ylabel('Speedup in relation to %s' % baseline)
    else:
        ylabel('Runtime in seconds')

    gca().yaxis.grid(True)
    gca().xaxis.grid(False)
    gca().set_axisbelow(True)

    if baseline:
        rect1 = bar(ind1, si, width, color="#D95F02", hatch="/")
        rect2 = bar(ind2, sc, width, color="#7570B3", hatch=".")

        legend(
            (rect1[0], rect2[0]),
            engines, 
            loc='upper center',
            bbox_to_anchor=(0.5,1.05), fancybox=True, shadow=True, ncol=len(engines)
        )
    else:
        rect0 = bar(ind0, np, width, color="#1B9E77", hatch="*")
        rect1 = bar(ind1, si, width, color="#D95F02", hatch="/")
        rect2 = bar(ind2, sc, width, color="#7570B3", hatch=".")

        legend(
            (rect0[0], rect1[0], rect2[0]),
            engines,
            loc='upper center',
            bbox_to_anchor=(0.5,1.05), fancybox=True, shadow=True, ncol=len(engines)
        )

    xticks(indt, [x if 'Jacobi' not in x else 'Jacobi' for x in benchmarks])

    fn = output +os.sep+ mark.lower()       # Output them
    dname = os.path.dirname(fn)
    bname = re.sub('\W', '_', os.path.basename(fn))
    fn = dname +os.sep+ bname

    for ff in file_formats:
        savefig("%s.%s" % ( fn, ff ))

    show()

def render_grp_graph(mark, data, baseline, comp, output, file_formats=['pdf']):

    try:
        os.makedirs(output)
    except:
        pass

    clf()
    rotation = 'horizontal'     # Assume that there is not enough room vertically

    groups  = ('NumPy', 'Score', 'Simple')
    width   = 0.25

    ind     = range(0, len(groups))
    ind0    = [i+width      for i in ind]
    ind1    = [i+width*2    for i in ind]
    ind2    = [i+width*3    for i in ind]
    indt    = [i+width*2.5  for i in ind]
   
    el = [t['elapsed'] for e,t in data]
    l1 = [t['l1_miss']/10 for e,t in data]
    ll = [t['ll_miss']/10 for e,t in data]

    #xlabel('Measurement')
    title(mark)

    gca().yaxis.grid(True)
    gca().xaxis.grid(False)
    gca().set_axisbelow(True)

    rect0 = bar(ind0, el, width, color="#1B9E77", hatch="*")
    rect1 = bar(ind1, l1, width, color="#D95F02", hatch="/")
    rect2 = bar(ind2, ll, width, color="#7570B3", hatch=".")
    
    legend( (rect0[0], rect1[0], rect2[0]), ('WC', 'L1-miss', 'LL-miss'))
    xticks(indt, groups)

    fn = output +os.sep+ mark.lower()       # Output them
    dname = os.path.dirname(fn)
    bname = re.sub('\W', '_', os.path.basename(fn))
    fn = dname +os.sep+ bname

    for ff in file_formats:
        savefig("%s.%s" % ( fn, ff ))

    show()

def render_by_hand(mark, data, baseline, comp, output, file_formats=['pdf']):

    try:
        os.makedirs(output)
    except:
        pass

    clf()
    rotation = 'horizontal'     # Assume that there is not enough room vertically

    groups  = ('NumPy', 'Score', 'Simple')
    width   = 0.25

    ind     = range(0, len(groups))
    ind0    = [i+width      for i in ind]
    ind1    = [i+width*2    for i in ind]
    ind2    = [i+width*3    for i in ind]
    indt    = [i+width*2.5  for i in ind]
   
    el = [t['elapsed'] for e,t in data]
    l1 = [t['l1_miss']/10 for e,t in data]
    ll = [t['ll_miss']/10 for e,t in data]

    #xlabel('Measurement')
    title(mark)

    gca().yaxis.grid(True)
    gca().xaxis.grid(False)
    gca().set_axisbelow(True)

    rect0 = bar(ind0, el, width, color="#1B9E77", hatch="*")
    rect1 = bar(ind1, l1, width, color="#D95F02", hatch="/")
    rect2 = bar(ind2, ll, width, color="#7570B3", hatch=".")
    
    legend( (rect0[0], rect1[0], rect2[0]), ('WC', 'L1-miss', 'LL-miss'))
    xticks(indt, groups)

    fn = output +os.sep+ mark.lower()       # Output them
    dname = os.path.dirname(fn)
    bname = re.sub('\W', '_', os.path.basename(fn))
    fn = dname +os.sep+ bname

    for ff in file_formats:
        savefig("%s.%s" % ( fn, ff ))

    show()


graphs = {
    'multiple': render_grpmark,
    'speedup':  render_rel_graph,
    'runtime':  render_abs_graph,
    'grouped':  render_grp_graph,
    '3d':       render_rel_graph
}

def normalize( runs ):

    for r in runs:
        if len(r) == 6:
            yield r + [[]]
        elif len(r) == 7:
            yield r

def filter_score(runs):
    return [run for run in runs if 'score' in run[1]]

def filter_simple_mcache(runs):
    return [run for run in runs if 'simple_mcache' in run[1]]

def filter_default( runs ):
    return [r for r in normalize(runs)]

def gen( benchmark, output, graph_name, graph, baseline, file_formats ):

    try:
        raw     = json.load(open(benchmark))
        meta    = raw['meta']
        runs    = filter_default(raw['runs'])
    except:
        return [1, "Failed loading benchmark %s." % benchmark]

    scale = 1000000.0

    bench   = {}
    #for mark, engine_lbl, engine, engine_args, cmd, times, perf_tl in filter_score(runs):
    #for mark, engine_lbl, engine, engine_args, cmd, times, perf_tl in filter_simple_mcache(runs):
    for mark, engine_lbl, engine, engine_args, cmd, times, perf_tl in runs:

        t_avg, t_max, t_min, t_dev = stats(times)

        l1_miss = 0
        ll_miss = 0
        perfs = parse_perf( perf_tl )
        try:
            if perfs:
                l1_miss = stats([perf['L1-dcache-load-misses']/scale for perf in perfs if 'L1-dcache-load-misses' in perf])[0]
                ll_miss = stats([perf['LLC-load-misses']      /scale for perf in perfs if 'LLC-load-misses' in perf])[0]
        except Exception as e:
            print "Err: [%s] when grabbing perf-data." % e

        if mark not in bench:
            bench[mark] = []

        bench[mark].append( (engine_lbl, {
            'elapsed': t_avg,
            'l1_miss': l1_miss,
            'll_miss': ll_miss
        }))

    if graph_name == 'multiple':
        graph( 'performance', bench, baseline, None, output, file_formats )
    else:
        for mark in bench:
            graph( mark, bench[mark], baseline, None, output, file_formats )
    
    return (0, None)

def main( results, output, multi, only_latest, graph_name, file_formats, baseline ):

    graph = graphs[graph_name]

    if multi:

        if not os.path.isdir( results ):
            return [(-1, "ERR: '%s' is not a directory." % ( results ))]

        if not os.path.isdir( output ):
            return [(-1, "ERR: '%s' is not a directory." % ( output ))]

        res = []
        for root, dirs, files in os.walk( results ):
            for fn in [x for x in files if ('json' in x or 'benchmark' in x) and ('latest' in x or not only_latest)]:
                r_input     = root +os.sep+ fn
                r_output    = root.replace('results', 'graphs') +os.sep
                if "latest" in fn:
                    r_output = r_output +os.sep+ 'latest'
                res.append( gen( r_input, r_output, graph_name, graph, baseline, file_formats ) )
        
        return res

    else:
        return [gen( results, output, graph_name, graph, baseline, file_formats )]

if __name__ == "__main__":

    formats = ['png', 'pdf', 'eps']

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
        '-l',
        dest='l',
        action="store_true",
        default=False,
        help="Only look for 'latest' when using multiple results."
    )
    parser.add_argument(
        '--output',
        dest='output',
        default="graphs",
        help='Where to store generated graphs.'
    )
    parser.add_argument(
        '--graph',
        dest='g',
        default='speedup',
        choices=[g for g in graphs]
    )
    parser.add_argument(
        '--format',
        dest='f',
        default='png',
        choices=[ff for ff in formats]
    )
    parser.add_argument(
        '--baseline',
        dest='bl',
        default=None
    )
    args = parser.parse_args()
    res = [msg for r, msg in main( args.results, args.output, args.m, args.l, args.g, [args.f], args.bl ) if msg]
    print ''.join( res )
