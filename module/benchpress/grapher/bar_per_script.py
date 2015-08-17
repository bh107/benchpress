from graph import Graph, texsafe
import numpy as np
from matplotlib.ticker import FormatStrFormatter
from matplotlib import pyplot
from benchpress import result_parser
import json
import re

def plot(cmds, res, baseline):

    import matplotlib.pyplot as plt

    t = cmds
    cmds = []
    for cmd in t:
        cmds.append(texsafe(cmd))

    ind = np.arange(len(cmds))  # the x locations for the groups
    width = 1.0/(len(res)+1)       # the width of the bars

    fig, ax = plt.subplots()
    i = 0
    bars = []
    comps = []

    for comp, value in res:
        avg = [v[0] for v in value]
        err = [v[1] for v in value]
        if len([v for v in avg if v > 0]) == 0:
            raise ValueError("All values to display are zero!")
        c = plt.cm.jet(1. * i / (len(res) - 1))
        b = ax.bar(ind+i*width, avg, width, color=c, log=False, yerr=err)
        bars.append(b)
        comps.append(comp)
        i+=1

    # add some text for labels, title and axes ticks
    ax.set_xticks(ind+(width*len(res))/2.)
    ax.set_xticklabels(cmds, rotation=+90, fontsize=10)
    if baseline is None:
        ax.set_ylabel('Cost in bytes')
    else:
        ax.set_ylabel('Cost compared to %s'%baseline)
    ax.legend(bars, comps)

def get_stack_name(stack):
    names = [comp[0] for comp in stack][1:]
    if "node" in names: names.remove("node")
    names.remove("bccon")
    names.remove("bcexp")
    names.remove("pricer")
    ret = ""
    for name in names:
        ret += "%s/"%name
    return ret[:-1]

class Bar_per_script(Graph):

    def render(self):

        raw = json.load(open(self.args.results))
        data = result_parser.from_file(self.args.results)

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
                        avg = result_parser.avg(r[self.args.data_to_display])
                        err = result_parser.standard_deviation(r[self.args.data_to_display])
                        value = (avg, err)
                    except KeyError:
                        print "WARNING - couldn't find '%s' in output of '%s'"%(self.args.data_to_display, comp)
                        value = (0,0)
                    comps.add(comp)
                    if s in res:
                        res[s][comp] = value
                    else:
                        res[s] = {comp:value}

        #Filter scripts and component stacks
        tmp = comps
        comps = []
        for comp in tmp:
            if re.search(self.args.stacks_to_display, comp) is not None and\
                re.search(self.args.stacks_not_to_display, comp) is None:
                comps.append(comp)
        tmp = scripts
        scripts = []
        for script in tmp:
            if re.search(self.args.scripts_to_display, script) is not None and\
                re.search(self.args.scripts_not_to_display, script) is None:
                scripts.append(script)

        #Extract the name of the baseline component
        comp_baseline = None
        if self.args.baseline is not None:
            for comp in comps:
                if self.args.baseline in comp:
                    comp_baseline = comp
                    break
            if comp_baseline is None:
                raise Exception("Couldn't find the specified baseline"\
                                " %s in the result json"%self.args.baseline)

        if comp_baseline is not None:
            #Remove the baseline component from 'comps' and make all values reletive
            comps.remove(comp_baseline)
            (base_avg, base_err) = res[script][comp_baseline]
            for script in scripts:
                for comp in comps:
                    if res[script][comp_baseline] > 0 or res[script][comp] > 0:
                        try:
                            (avg, err) = res[script][comp]
                            res[script][comp] = (base_avg/avg, 0)
                        except ZeroDivisionError:
                            res[script][comp] = (0,0)

        #Convert to a bar-plot friendly format
        data = []
        for comp in comps:
            values = []
            for script in scripts:
                values.append(res[script][comp])
            data.append((comp,values))
        plot(scripts, data, self.args.baseline)
        self.tofile({"title": self.args.title})

