from graph import Graph
import numpy as np
from matplotlib.ticker import FormatStrFormatter
from matplotlib import pyplot
from benchpress import result_parser
import json

def plot(cmds, res, baseline):

    import matplotlib.pyplot as plt

    ind = np.arange(len(cmds))  # the x locations for the groups
    width = 1.0/(len(res)+1)       # the width of the bars

    fig, ax = plt.subplots()
    i = 0
    bars = []
    fusers = []
    for fuser, costs in res:
        c = plt.cm.jet(1. * i / (len(res) - 1))
        b = ax.bar(ind+i*width, costs, width, color=c)
        bars.append(b)
        fusers.append(fuser)
        i+=1

    # add some text for labels, title and axes ticks
    ax.set_xticks(ind+(width*len(res))/2.)
    ax.set_xticklabels(cmds, rotation=-35)
    if baseline is None:
        ax.set_ylabel('Cost in bytes')
    else:
        ax.set_ylabel('Cost compared to %s'%baseline)
    ax.set_ylim(0,30)
    #ax.set_yscale('log')
    ax.legend(bars, fusers)

def get_stack_name(stack):
    names = [comp[0] for comp in stack][1:]
    names.remove("node")
    names.remove("bccon")
    names.remove("bcexp")
    names.remove("pricer")
    ret = ""
    for name in names:
        ret += "%s/"%name
    return ret[:-1]

class Fuse_price(Graph):

    def render(self, args):

        raw = json.load(open(args.results))
        data = result_parser.from_file(args.results)

        self.prep()             # Do some MPL-magic

        # Extract result data
        res = {}
        scripts = list(set([script for script, _, _, _, _ in data]))
        comps = set()
        for s in scripts:
            for script, _, _, _, r in data:
                if script == s:
                    comp = get_stack_name(r['stack'])
                    try:
                        value = r['fuseprice'][0]
                    except:
                        value = 0
                    comps.add(comp)
                    if s in res:
                        res[s][comp] = value
                    else:
                        res[s] = {comp:value}

        #Extract the name of the optimal component
        comp_optimal = None
        for comp in comps:
            if 'optimal' in comp:
                comp_optimal = comp
                break

        #Let's make sure that the optimal component is the best
        if comp_optimal is not None:
            for s in scripts:
                if comp_optimal in res[s]:
                    best = res[s][comp_optimal]
                    for comp, value in res[s].iteritems():
                        if value < best:
                            raise Exception("The optimal fuser isn't best: %s(%d) < %s(%d)"\
                                             %(comp, value, comp_optimal, best))

        #Extract the name of the baseline component
        comp_baseline = None
        if args.baseline is not None:
            for comp in comps:
                if args.baseline in comp:
                    comp_baseline = comp
                    break
            if comp_baseline is None:
                raise Exception("Couldn't find the specified baseline"\
                                " %s in the result json"%args.baseline)

        if comp_baseline is not None:
            #Remove the baseline component from 'comps' and make all values reletive
            comps.remove(comp_baseline)
            for script in scripts:
                for comp in comps:
                    if res[script][comp_baseline] > 0 or res[script][comp] > 0:
                        res[script][comp] = res[script][comp_baseline] / res[script][comp]

        #Convert to a bar-plot friendly format
        data = []
        for comp in comps:
            values = []
            for script in scripts:
                values.append(res[script][comp])
            data.append((comp,values))
        plot(scripts, data, args.baseline)
        self.tofile({"title": self.title})

