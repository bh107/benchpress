#!/usr/bin/env python
# -*- coding: utf8 -*-
import pprint
import json
from benchpress.cpu_result_parser import flatten, group_by_script, datasetify, ident_ordering, order_idents
from benchpress.cpu_result_parser import datasets_rename, ident_mapping
from graph import Graph, texsafe, brange, pylab, matplotlib

class AbsoluteLine(Graph):
    """
    Renders a single graph with absolute numbers.
    Plotting deviation as well.

    Format of the datasets must be:
    {
        "ident1": {
            "avg": [a1, ... , an],
            "dev": [d1, ... , dn],
        },
        ...
        ,
         "identm": {
            "avg": [a1, ... , an]
            "dev": [d1, ... , dn]
        }
    }
    """

    def render(self, datasets, sample_points):

        thread_limit = max(sample_points)

        self.prep()             # Do some MPL-magic

        plots = []
        legend_texts = []
        idents = order_idents(datasets.keys(), ident_ordering)
        for idx, ident in enumerate(idents): # Plot datasets
            dataset = datasets[ident]["avg"]
            deviation = datasets[ident]["avg"]
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

            legend_txt = r"%s" % ident
            legend_texts.append(legend_txt)

        pylab.legend(                                   # Legends
            plots,
            legend_texts,
            loc=3,
            ncol=3,
            bbox_to_anchor=(0.015, 0.95, 0.9, 0.102),
            borderaxespad=0.0
        )
        pylab.ylabel(                                   # Y-Axis
            r"Elapsed wall-clock in \textbf{seconds}"
        )

        pylab.xlabel(r"Threads")                        # X-Axis
        pylab.xscale("symlog", basey=2, basex=2)
        pylab.xlim(xmin=0.8, xmax=thread_limit*1.20)
        pylab.xticks(sample_points, sample_points)
        pylab.gca().xaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())

        t = pylab.title(texsafe(self.args.title))            # Title
        t.set_y(1.15)
        pylab.tight_layout()

        return self.tofile({"title": self.args.title})              # Finally write it to file

class AbsoluteBar(Graph):
    """
    Renders a single graph with absolute numbers.
    Plotting deviation as well.

    Format of the datasets must be:
    {
        "ident1": {
            "avg": [a1, ... , an],
            "dev": [d1, ... , dn],
        },
        ...
        ,
         "identm": {
            "avg": [a1, ... , an]
            "dev": [d1, ... , dn]
        }
    }
    """

    def render(self, datasets, sample_points):
        self.prep()             # Do some MPL-magic

        min_threads     = min(sample_points)
        max_threads     = max(sample_points)
        data_points = 6
        #linear          = list(brange(min_threads, max_threads))
        plot_count      = len(sample_points)

        idents = order_idents(datasets.keys(), ident_ordering)
        max_runtime = max(
            [max(datasets[ident]['avg']) for ident in idents]
        )

        ind = range(data_points)                # Group start locations
        width = 0.3                             # Width of the bars
        group_width = width * (len(idents))     # Width of the group
        group_center = group_width / 2.0        # Center of groups

        fig, ax = pylab.subplots()

        rects = {}                          # Draw the bars
        for idx, ident in enumerate(idents):
            rects[ident] = ax.bar(
                [x+width*idx for x in ind],
                datasets[ident]["avg"],
                width,
                color=Graph.colors[idx],
                yerr=datasets[ident]["dev"]
            )

        # add some text for labels, title and axes ticks
        ax.set_ylabel(r"Elapsed wall-clock time in \textbf{seconds}")
        ax.set_xticks([x+group_center for x in ind])
        ax.set_xticklabels([str(x) for x in sample_points])

        ax.legend(
            [rects[ident] for ident in idents],
            [ident for ident in idents],
            loc=3,
            ncol=3,
            bbox_to_anchor=(0.01, 0.95, 0.9, 0.102),
            borderaxespad=0.0
        )

        def autolabel(rectangles):
            # attach some text labels
            for rect in rectangles:
                height = rect.get_height()
                ax.text(
                    rect.get_x()+rect.get_width()/2.,
                    1.015 * height,
                    '%.1f' % height,
                    ha='center',
                    va='bottom'
                )

        for ident in idents:
            autolabel(rects[ident])

        pylab.xlabel("Threads")
        t = pylab.title(texsafe(self.args.title))
        t.set_y(1.05)

        pylab.ylim(ymin=0, ymax=max_runtime*1.13)

        pylab.tight_layout()                  # Spit them out to file

        return self.tofile({"title": self.args.title})              # Finally write it to file

class ArgsDummy(object):
    pass

def absolute(title, output_path, datasets, sample_points):
    args = ArgsDummy()
    args.title = title
    args.output_path = output_path
    args.line_width = 2
    args.fn_pattern = "{title}_abs.{ext}"
    args.formats = ["png"]
    args.fontsize = 10

    nidents = len([ident for ident in datasets])
    if nidents < 4:
        g = AbsoluteBar(args)
    else:
        g = AbsoluteLine(args)
    return g.render(datasets, sample_points)


