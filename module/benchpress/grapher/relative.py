#!/usr/bin/env python
# -*- coding: utf8 -*-
import pprint
import json
from benchpress.cpu_result_parser import flatten, group_by_script, datasetify
from benchpress.cpu_result_parser import datasets_rename, ident_mapping, datasets_baselinify
from graph import Graph, texsafe, brange, pylab, matplotlib

class Relative(Graph):
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

    def __init__(
        self,
        title = "Untitled Speedup Graph",
        line_width = 2,
        fn_pattern = "{title}_rel_{baseline}.{ext}",
        file_formats = ["png"],
        output_path = "."):

        super(Relative, self).__init__(title,
                                       line_width,
                                       fn_pattern,
                                       file_formats,
                                       output_path)

    def render(self, datasets):

        paths = []
        thread_limit = 32
        global_max, baselined = datasets_baselinify(datasets)

        linear = list(brange(1, thread_limit))

        bsl_idents = sorted([ident for ident in baselined])
        for bsl_ident in bsl_idents:# Construct data using ident as baseline
            self.prep()             # Do some MPL-magic

            plots = []
            legend_texts = []
            for idx, ident in enumerate(sorted(baselined[bsl_ident])): # Plot datasets
                dataset = baselined[bsl_ident][ident]["avg"]
                plt, = pylab.plot(
                    linear,
                    dataset,
                    linestyle="-",
                    label=ident,
                    color=Graph.colors[idx],
                    lw=self.line_width,
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
                linear,
                linear,
                "--",
                color='gray',
                lw=self.line_width
            )  # Linear, for reference

            # TODO: Legends
            pylab.legend(
                plots,
                legend_texts,
                loc=3,
                ncol=3,
                bbox_to_anchor=(0.015, 0.95, 0.9, 0.102),
                borderaxespad=0.0
            )
            pylab.ylabel(                                   # Y-Axis
                r"Speedup in relation to \textbf{%s}" % bsl_ident
            )
            pylab.yscale("symlog", basey=2, basex=2)
            pylab.ylim(
                ymin=0,
                ymax=max(global_max*1.2, thread_limit*1.2),
                
            )
            yticks = list(brange(1, max(thread_limit, global_max*2)))
            pylab.yticks(yticks, yticks)
            pylab.gca().yaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())

            pylab.xlabel(r"Threads")                        # X-Axis
            pylab.xscale("symlog", basey=2, basex=2)
            pylab.xlim(xmin=0.8, xmax=thread_limit*1.20)
            pylab.xticks(linear, linear)
            pylab.gca().xaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())

            t = pylab.title(texsafe(self.title))                # Title
            t.set_y(1.15)
            pylab.tight_layout()

            paths += self.tofile({                                   # Finally write it to file
                "title": self.title,
                "baseline": bsl_ident
            })

        return paths

if __name__ == "__main__":
    path = "engine.json"
    runs_flattened = flatten(json.load(open(path))["runs"])
    runs_grouped = group_by_script(runs_flattened)
    datasets = datasets_rename(
        datasetify(runs_grouped),
        ident_mapping
    )

    scripts = sorted([script for script in datasets])
    for script in scripts:
        graph = Relative(title=script)
        graph.render(datasets[script])
        break
