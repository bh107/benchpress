#!/usr/bin/env python
# -*- coding: utf8 -*-
import pprint
import json
from cpu_result_parser import flatten, group_by_script, datasetify
from cpu_result_parser import datasets_rename, ident_mapping
from graph import Graph, texsafe, pylab

class Relative(Graph):
    """
    Renders multiple graphs, one for each possible baseline,
    using the first value for each provided dataset in the dict of datasets.

    Format of the datasets must be:
    {
        "ident1": {
            "avg": [v1, ... , vn],
            "dev": [u1, ... , un]
        },
        ...
        ,
         "identm": {
            "avg": [v1, ... , vn],
            "dev": [u1, ... , un]
        }
    }
    """

    def __init__(
        self,
        title = "Untitled Speedup Graph",
        fn_pattern = "{title}_rel_{baseline}.{ext}",
        file_formats = ["png"]):

        super(Relative, self).__init__(title, fn_pattern, file_formats)

    def plot(self, datasets):
        self.prep()                 # Do some MPL-magic
        pprint.pprint(datasets)
        # Compute baselines, max/min for each

        keys = sorted([key for key in datasets])
        for key in keys:            # Construct data using key as baseline

            # Todo: plot the data

            # Todo: labels

            # Todo: x-ticks and labels
            # Todo: y-ticks and labels

            pylab.title(texsafe(self.title))
            pylab.ylabel(r"Speedup in relation to \textbf{%s}" % key)
            pylab.xlabel(r"Threads")
            self.tofile({           # Finally write it to file
                "title": self.title,
                "baseline": key
            })

if __name__ == "__main__":
    path = "result.json"
    runs_flattened = flatten(json.load(open(path))["runs"])
    runs_grouped = group_by_script(runs_flattened)
    datasets = datasets_rename(
        datasetify(runs_grouped),
        ident_mapping
    )

    scripts = sorted([script for script in datasets])
    pprint.pprint(scripts)
    for script in scripts:
        datasets = datasets[script]
        graph = Relative(title=script)
        graph.plot(datasets)
        break
