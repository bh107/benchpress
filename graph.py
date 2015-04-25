#!/usr/bin/env python
# -*- coding: utf8 -*-
import string
import os
import matplotlib
matplotlib.use('Agg')   # Essential for "headless" operation
import pylab

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

class Graph(object):
    """
    Baseclass for rendering Matplotlib graphs.
    Does alot of the annoying work, just override the plot(...) method,
    and you are good to go!
    """

    colors = [
        "#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00", "#ffff33",
        "#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00", "#ffff33",
        "#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00", "#ffff33"
    ]

    hatches = [
        "\\", "+", "o", "/", "-", "O",
        "\\", "+", "o", "/", "-", "O",
        "\\", "+", "o", "/", "-", "O",
        "\\", "+", "o", "/", "-", "O",
        "\\", "+", "o", "/", "-", "O",
    ]

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

    def tofile(self, fn_args):          # Creates the output-file.

        if not os.path.exists(self.output_path):
            raise("Output path %s does not exists. Cannot spit out graphs")

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
