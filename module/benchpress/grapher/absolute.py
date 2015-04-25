#!/usr/bin/env python
# -*- coding: utf8 -*-
import pprint
import json
from benchpress.cpu_result_parser import flatten, group_by_script, datasetify
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

    def __init__(self,
                 title = "Untitled Absolute Graph",
                 line_width = 2,
                 fn_pattern = "{title}_abs.{ext}",
                 file_formats = ["png"],
                 output_path = "."):

        super(AbsoluteLine, self).__init__(title,
                                           line_width,
                                           fn_pattern,
                                           file_formats,
                                           output_path)

    def render(self, datasets):

        thread_limit = 32

        linear = list(brange(1, thread_limit))

        self.prep()             # Do some MPL-magic

        plots = []
        legend_texts = []
        for idx, ident in enumerate(sorted(datasets)): # Plot datasets
            dataset = datasets[ident]["avg"]
            deviation = datasets[ident]["avg"]
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
        pylab.xticks(linear, linear)
        pylab.gca().xaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())

        t = pylab.title(texsafe(self.title))            # Title
        t.set_y(1.15)
        pylab.tight_layout()

        self.tofile({"title": self.title})              # Finally write it to file

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

    def __init__(self,
                 title = "Untitled Absolute Graph",
                 line_width = 2,
                 fn_pattern = "{title}_abs.{ext}",
                 file_formats = ["png"],
                 output_path = "."):
        super(AbsoluteBar, self).__init__(title,
                                          line_width,
                                          fn_pattern,
                                          file_formats,
                                          output_path)

    def render(self, datasets):
        self.prep()             # Do some MPL-magic

        min_threads     = 1
        max_threads     = 32 
        data_points = 6
        linear          = list(brange(min_threads, max_threads))
        plot_count      = len(linear)

        idents = sorted(datasets)
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
        ax.set_xticklabels([str(x) for x in linear])

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
        t = pylab.title(texsafe(self.title))
        t.set_y(1.05)

        pylab.ylim(ymin=0, ymax=max_runtime*1.13)

        pylab.tight_layout()                  # Spit them out to file

        self.tofile({"title": self.title})              # Finally write it to file

class Absolute(Graph):

    def __init__(self,
                 title = "Untitled Absolute Graph",
                 line_width = 2,
                 fn_pattern = "{title}_abs.{ext}",
                 file_formats = ["png"],
                 output_path = "."):

        super(Absolute, self).__init__(title,
                                       line_width,
                                       fn_pattern,
                                       file_formats,
                                       output_path)

    def render(self, datasets):

        nidents = len([ident for ident in datasets])
        args = {
            "title": self.title,
            "line_width": self.line_width,
            "file_formats": self.file_formats,
            "fn_pattern": self.fn_pattern
        }
        if nidents < 4:
            g = AbsoluteBar(**args)
        else:
            g = AbsoluteLine(**args)
        g.render(datasets)

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
        graph = Absolute(title=script)
        graph.render(datasets[script])
