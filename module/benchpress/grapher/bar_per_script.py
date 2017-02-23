from graph import Graph, texsafe, filter_list, translate_dict
import numpy as np
from matplotlib.ticker import FormatStrFormatter
from matplotlib import pyplot
from benchpress import result_parser
import json
import re


def value_labels(ax, rects):
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%.2f' % float(height),
                ha='center', va='bottom')


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
        c = plt.cm.jet(1. * i / max(len(res)-1, 1))
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

    if not args.no_legend:
        ax.legend(bars,
                  comps,
                  ncol=len(comps),
                  loc='upper center',
                  bbox_to_anchor=(0.5, 1.06),
                  fancybox=True,
                  shadow=True,
                  columnspacing=1)

    # Now make some labels
    value_labels(ax, ax.patches)


def get_stack_name(stack):
    names = [comp[0] for comp in stack][1:]
    ret = ""
    for name in names:
        ret += "%s/"%name
    return ret[:-1]


class Bar_per_script(Graph):

    def render(self):

        data = result_parser.from_file(self.args.results)

        self.prep()             # Do some MPL-magic

        # Extract result data
        res = {}
        scripts = list(set([script for script, _, _ in data]))
        comps = set()
        for s in scripts:
            for script, _, r in data:
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

        # Extract the name of the baseline component
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
            # Let's make all values relative compared to the baseline
            for script in scripts:
                (base_avg, base_err) = res[script][comp_baseline]
                for comp in comps:
                    if res[script][comp_baseline] > 0 or res[script][comp] > 0:
                        try:
                            (avg, err) = res[script][comp]
                            res[script][comp] = (base_avg/avg, 0)
                        except (ZeroDivisionError, KeyError) as e:
                            res[script][comp] = (0, 0)

        # Filter scripts and component stacks
        comps = filter_list(comps, self.args.stacks_to_display, self.args.stacks_not_to_display)
        scripts = filter_list(scripts, self.args.scripts_to_display, self.args.scripts_not_to_display)
        comps.sort()
        scripts.sort()

        # Get translation of the components and scripts
        comp_dict = translate_dict(comps, self.args.stack_map)
        script_dict = translate_dict(scripts, self.args.script_map)

        # Convert to a bar-plot friendly format
        data = []
        for comp in comps:
            values = []
            for script in scripts:
                try:
                    values.append(res[script][comp])
                except KeyError:
                    values.append((0, 0))
            if comp != comp_baseline:
                data.append((comp_dict[comp], values))
        plot([script_dict[s] for s in scripts], data, self.args.baseline, self.args)
        self.tofile({"title": self.args.title})

