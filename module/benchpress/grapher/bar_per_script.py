from graph import Graph, texsafe
import numpy as np
from matplotlib.ticker import FormatStrFormatter
from matplotlib import pyplot
from benchpress import result_parser
import json
import re

def plot(cmds, res, baseline, args):

    import matplotlib.pyplot as plt

    t = cmds
    cmds = []
    for cmd in t:
        cmds.append(texsafe(cmd))

    ind = np.arange(len(cmds))  # the x locations for the groups

    margin = 0.05
    width = (1.-2.*margin)/len(res)

    fig, ax = plt.subplots()
    i = 0
    bars = []
    comps = []

    for comp, value in res:
        avg = [v[0] for v in value]
        err = [v[1] for v in value]
        if len([v for v in avg if v > 0]) == 0:
            raise ValueError("All values to display are zero in '%s'"%comp)
        c = plt.cm.jet(1. * i / (len(res) - 1))
        b = ax.bar(ind+i*width, avg, width, color=c, log=args.ylog, yerr=err)
        bars.append(b)
        comps.append(texsafe(comp))
        i+=1

    if args.ymin is not None:
        plt.ylim(ymin=float(args.ymin))
    if args.ymax is not None:
        plt.ylim(ymax=float(args.ymax))

    plt.xlim(xmax=ind[-1]+1)

    # add some text for labels, title and axes ticks
    ax.set_xticks(ind+(width*len(res))/2.)
    ax.set_xticklabels(cmds, rotation=args.xticklabel_rotation)
    if args.ylabel is not None:
        ax.set_ylabel(args.ylabel)
    elif baseline is None:
        ax.set_ylabel(args.data_to_display)
    else:
        ax.set_ylabel('%s compared to %s'%(args.data_to_display, baseline))

    ax.legend(bars,
              comps,
              ncol=len(comps),
              loc='upper center',
              bbox_to_anchor=(0.5, 1.06),
              fancybox=True,
              shadow=True,
              columnspacing=1)

def get_stack_name(stack):
    names = [comp[0] for comp in stack][1:]
    if "node" in names: names.remove("node")
    if "bccon" in names: names.remove("bccon")
    if "bcexp" in names: names.remove("bcexp")
    if "pricer" in names: names.remove("pricer")
    if "bcexp_gpu" in names: names.remove("bcexp_gpu")
    if "dimclean" in names: names.remove("dimclean")
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

        if self.args.baseline is not None:
            #Let's make all values relative compared to the baseline
            for script in scripts:
                (base_avg, base_err) = res[script][comp_baseline]
                for comp in comps:
                    if res[script][comp_baseline] > 0 or res[script][comp] > 0:
                        try:
                            (avg, err) = res[script][comp]
                            res[script][comp] = (base_avg/avg, 0)
                        except (ZeroDivisionError, KeyError) as e:
                            res[script][comp] = (0,0)

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

        comps.sort()
        scripts.sort()

        #Translate comps names
        tmp = comps
        comps = []
        for (old, new) in self.args.stack_map:
            for i in xrange(len(tmp)):
                if re.search(old, tmp[i]) is not None:
                    new = tmp[i] if new == "" else new
                    comps.append((tmp[i],new))
                    tmp.pop(i)
                    break
        comps += [(t,t) for t in tmp]

        #Translate script names
        tmp = scripts
        scripts = []
        for (old, new) in self.args.script_map:
            for i in xrange(len(tmp)):
                if re.search(old, tmp[i]) is not None:
                    new = tmp[i] if new == "" else new
                    scripts.append((tmp[i],new))
                    tmp.pop(i)
                    break
        scripts += [(t,t) for t in tmp]

        #Convert to a bar-plot friendly format
        data = []
        for (comp_old, comp_new) in comps:
            values = []
            for (script_old, script_new) in scripts:
                try:
                    values.append(res[script_old][comp_old])
                except KeyError:
                    values.append((0,0))
            data.append((comp_new,values))
        plot([s[1] for s in scripts], data, self.args.baseline, self.args)
        self.tofile({"title": self.args.title})

