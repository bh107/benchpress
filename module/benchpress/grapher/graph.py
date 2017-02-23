#!/usr/bi "\\",n/env python
# -*- coding: utf8 -*-
import string
import os
import matplotlib
matplotlib.use('Agg')   # Essential for "headless" operation
import pylab
import re


def brange(begin, end):
    thres = 0
    i = 0
    while thres < end:
        thres = 2**i
        i += 1
    thres = end

    c = i = begin
    while i <= end:
        yield i
        i = 2**c
        c += 1


def sanitize_fn(filename):
    valid_chars = ".-_%s%s" % (string.digits, string.ascii_lowercase)
    sanitized = []
    for idx, char in enumerate(filename.lower()):
        if char not in valid_chars:
            char = "_"
        sanitized.append(char)
    return "".join(sanitized)


def texsafe(text):
    """Escape text such that it is tex-safe."""
    conv = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\^{}',
        '\\': r'\textbackslash{}',
        '<': r'\textless',
        '>': r'\textgreater',
    }
    escaped = []

    for char in text:
        if char in conv:
            char = conv[char]
        escaped.append(char)
    return "".join(escaped)


def filter_list(_list, regex_to_include=".*", regex_not_to_include="NotIncluded"):
    """Return a new copy of '_list' where the regex in 'regex_to_include' and 'regex_not_to_include'
        are obeyed"""

    ret = []
    for item in _list:
        if re.search(regex_to_include, item) is not None and \
           re.search(regex_not_to_include, item) is None:
            ret.append(item)
    return ret


def translate_dict(names, name_map):
    """Return a dict mapping old names with new names using the (possible incomplete) 'name_map'"""

    names = list(names)
    ret = {}
    for (old, new) in name_map:
        if len(new) > 0:
            for i in range(len(names)):
                if re.search(old, names[i]) is not None:
                    ret[names[i]] = new
                    names.pop(i)
                    break
    for old, new in [(t, t) for t in names]:
        ret[old] = new
    return ret


class Grapher(object):
    """
    Take a result file and produces some output.

    Can be just a graph, html page, or something completely different
    """

    def __init__(self, args):
        self.args = args

    def render(self):
        raise NotImplementedError()

    def tofile(self, name, source):
        """ Write 'source' to a file named 'name', which should include the extension (e.g. .html or .txt).
            The output directory is taken from self.args.output_path """

        fname = os.path.join(self.args.output_path, name)
        with open(fname, 'w') as f:
            f.write(source)

class Graph(Grapher):
    """
    Base class for rendering Matplotlib graphs.
    Does a lot of the annoying work, just override the plot(...) method,
    and you are good to go!
    """

    colors = [
        "#1b9e77", "#d95f02", "#7570b3", "#e7298a", "#66a61e", "#e6ab02", "#a6761d", "#666666",
        "#1b9e77", "#d95f02", "#7570b3", "#e7298a", "#66a61e", "#e6ab02", "#a6761d", "#666666",
        "#1b9e77", "#d95f02", "#7570b3", "#e7298a", "#66a61e", "#e6ab02", "#a6761d", "#666666",
        "#1b9e77", "#d95f02", "#7570b3", "#e7298a", "#66a61e", "#e6ab02", "#a6761d", "#666666",
    ]

    markers = [
        r'o',
        r's',
        r'D',
        r'*',
        r'<',
        r'>',
        r'^',
        r'v',
        r'$\clubsuit$',
        r'p',
        r'd',
    ]

    marker_sizes = [
        6,6,6,9,7,
        7,7,7,7,7,
        7,7
    ]

    hatches = [
        r'o',
        r's',
        r'D',
        r'*',
        r'<',
        r'>',
        r'^',
        r'v',
        r'$\clubsuit$',
        r'p',
        r'd',
    ]

    def __init__(self, args):
        super(Graph, self).__init__(args)
        self._mpl_init()

    def _mpl_init(self):
        size = self.args.fontsize
        matplotlib.rcParams['axes.labelsize'] = size
        matplotlib.rcParams['axes.titlesize'] = size + 2
        matplotlib.rcParams['xtick.labelsize'] = size
        matplotlib.rcParams['ytick.labelsize'] = size
        matplotlib.rcParams['legend.fontsize'] = size
        matplotlib.rcParams['font.family'] = 'serif'
        matplotlib.rcParams['font.serif'] = ['Computer Modern Roman']
        matplotlib.rcParams['text.usetex'] = True
        matplotlib.rcParams['figure.max_open_warning'] = 400
        matplotlib.rcParams['figure.autolayout'] = True


    def render(self):
        raise Exception("Unimplemented the actual plotting.")

    def prep(self):
        pylab.clf()                     # Essential! Othervise the plots will be f**d up!
        pylab.figure(1)

        pylab.gca().yaxis.grid(True)    # Makes it easier to compare bars
        pylab.gca().xaxis.grid(False)
        pylab.gca().set_axisbelow(True)

    def tofile(self, fn_args):          # Creates the output-file.

        if not os.path.exists(self.args.output_path):
            raise Exception("Output path %s does not exists. Cannot spit out graphs")

        paths = []
        for file_format in self.args.formats:

            filename = sanitize_fn(self.args.fn_pattern.format(
                ext=file_format,
                **fn_args
            ))
            abs_path = os.sep.join([
                self.args.output_path,
                filename
            ])
            paths.append(abs_path)

            pylab.savefig(abs_path)
            pylab.show()

        return paths
