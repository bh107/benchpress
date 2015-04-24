#!/usr/bin/env python
# -*- coding: utf8 -*-
import pprint
import string
import json
import os
import matplotlib
matplotlib.use('Agg')   # Essential for generating graphs "headless".
import pylab
from cpu_result_parser import flatten, group_by_script, datasetify

class Graph(object):

    def __init__(
        self,
        title = "Untitled Graph",
        fn_pattern = "{title}.{ext}",
        file_formats = ["png"],
        directory="."):

        self.title = title
        self.fn_pattern = fn_pattern
        self.file_formats = file_formats
        self.output_path = os.path.expandvars(os.path.expanduser(directory))

        self._mpl_init()

    def _mpl_init(self):
        matplotlib.rcParams['axes.labelsize'] = 14
        matplotlib.rcParams['axes.titlesize'] = 16
        matplotlib.rcParams['xtick.labelsize'] = 14
        matplotlib.rcParams['ytick.labelsize'] = 14
        matplotlib.rcParams['legend.fontsize'] = 14
        matplotlib.rcParams['font.family'] = 'serif'
        matplotlib.rcParams['font.serif'] = ['Computer Modern Roman']
        matplotlib.rcParams['text.usetex'] = True
        matplotlib.rcParams['figure.max_open_warning'] = 400

    def plot(self):
        raise Exception("Unimplemented the actual plotting.")

    def prep(self):
        pylab.clf()                     # Essential! Othervise the plots will be f**d up!
        pylab.figure(1)

        pylab.gca().yaxis.grid(True)    # Makes it easier to compare bars
        pylab.gca().xaxis.grid(False)
        pylab.gca().set_axisbelow(True)

        pylab.title(self.title)         # Title

    def tofile(self, fn_args):          # Creates the output-file.

        if not os.path.exists(self.output_path):
            raise("Output path %s does not exists. Cannot spit out graphs")

        def sanitize_fn(filename):
            valid_chars = ".-_%s%s" % (string.digits, string.ascii_lowercase)
            sanitized = []
            for idx, char in enumerate(filename.lower()):
                if char in valid_chars:
                    sanitized.append(char)
                else:
                    sanitized.append("_")
            return "".join(sanitized)

        paths = []
        for file_format in self.file_formats:
        
            filename = sanitize_fn(self.fn_pattern.format(
                ext=file_format,
                **fn_args
            ))
            abs_path = os.sep.join([
                self.output_path,
                filename
            ])
            paths.append(abs_path)

            pylab.savefig(abs_path)
            pylab.show()

        return paths

class Relative(Graph):

    def __init__(
        self,
        title = "Untitled Speedup Graph",
        fn_pattern = "{title}_rel_{baseline}.{ext}",
        file_formats = ["png"]):

        super(Relative, self).__init__(title, fn_pattern, file_formats)

    def render(self, dataset, baseline):
        self.prep()                 # Do some MPL-magic

        

        self.tofile({               # Finally write it to file
            "title": self.title,
            "baseline": baseline
        })

def main(path):
    runs_flattened = flatten(json.load(open(path))["runs"])
    runs_grouped = group_by_script(runs_flattened)
    datasets = datasetify(runs_grouped)

    for script in sorted([script for script in datasets]):
        dataset = datasets[script]
        graph = Relative(title=script)
        graph.render(dataset, "BAHH")
        break

if __name__ == "__main__":
    main("result.json")
