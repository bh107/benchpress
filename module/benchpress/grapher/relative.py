#!/usr/bin/env python
# -*- coding: utf8 -*-
import pprint
import json
import copy
from benchpress.cpu_result_parser import flatten, group_by_script, datasetify, ident_ordering, order_idents
from benchpress.cpu_result_parser import datasets_rename, ident_mapping, datasets_baselinify
from graph import Graph, texsafe, brange, pylab, matplotlib

class RelativeGraph(Graph):
    """
    Renders multiple graphs, one for each possible baseline,
    using the first value for each provided dataset in the dict of datasets.

    Format of the datasets must be:
    {
        "ident1": {
            "avg": [v1, ... , vn]
        },
        ...
        ,
         "identm": {
            "avg": [v1, ... , vn]
        }
    }
    """

    def render(self, datasets, sample_points):

        paths = []
        thread_max = max(sample_points)
        global_max, baselined = datasets_baselinify(datasets)

        idents = order_idents(baselined.keys(), ident_ordering)
        for bsl_ident in idents:    # Construct data using ident as baseline
            self.prep()             # Do some MPL-magic

            plots = []
            legend_texts = []
            for idx, ident in enumerate(idents):            # Plot datasets
                dataset = baselined[bsl_ident][ident]["avg"]
                plt, = pylab.plot(
                    sample_points,
                    dataset,
                    linestyle="-",
                    label=ident,
                    color=Graph.colors[idx],
                    lw=self.args.line_width,
                    marker=Graph.markers[idx],
                    markersize=Graph.marker_sizes[idx]
                )
                plots.append(plt)

                legend_txt = r"%s: \textbf{%.1f} - \textbf{%.1f}" % (
                    ident,
                    baselined[bsl_ident][ident]["min"],
                    baselined[bsl_ident][ident]["max"]
                )
                legend_texts.append(legend_txt)

            pylab.plot(
                sample_points,
                sample_points,
                "--",
                color='gray',
                lw=self.args.line_width
            )                                               # sample_points, for reference

            pylab.legend(
                plots,
                legend_texts,
                loc=3,
                ncol=3,
                bbox_to_anchor=(0.015, 0.95, 0.9, 0.102),
                borderaxespad=0.0
            )                                               # legends

            pylab.xlabel(r"Threads")                        # X-Axis - begin
            pylab.xscale("symlog", basey=2, basex=2)
            pylab.xlim(xmin=0.8, xmax=thread_max*1.20)
            pylab.xticks(sample_points, sample_points)
            pylab.gca().xaxis.set_major_formatter(
                matplotlib.ticker.ScalarFormatter()
            )                                               # X-Axis - end

            pylab.ylabel(                                   # Y-Axis
                r"Speedup in relation to \textbf{%s}" % bsl_ident
            )
            pylab.yscale("symlog", basey=2, basex=2)
            pylab.ylim(
                ymin=0,
                ymax=max(global_max*1.2, thread_max*1.2),
            )

            yticks = copy.deepcopy(sample_points)
            if global_max*2 > thread_max:
                yticks[-1] = int(global_max*2)
            pylab.yticks(yticks, yticks)
            pylab.gca().yaxis.set_major_formatter(
                matplotlib.ticker.ScalarFormatter()
            )                                               # Y-Axis - end

            t = pylab.title(texsafe(self.args.title))            # Title
            t.set_y(1.15)
            pylab.tight_layout()

            paths += self.tofile({                          # Finally write it to file
                "title": self.args.title,
                "baseline": bsl_ident
            })

        return paths

class ArgsDummy(object):
    pass

def relative(title, output_path, datasets, sample_points):
    args = ArgsDummy()
    args.title = title
    args.output_path = output_path
    args.line_width = 2
    args.fn_pattern = "{title}_rel_{baseline}.{ext}"
    args.file_formats = ["png"]

    return RelativeGraph(args).render(datasets, sample_points)

