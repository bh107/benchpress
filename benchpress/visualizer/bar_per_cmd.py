# -*- coding: utf-8 -*-
from __future__ import absolute_import
import json
import numpy as np
from benchpress.visualizer import util
import matplotlib
import matplotlib.pyplot as plt
import pylab


def value_labels(ax, rects):
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%.2f' % float(height),
                ha='center', va='bottom')


def one_bar_per_cmd(args):
    matplotlib.rcParams['axes.labelsize'] = args.fontsize
    matplotlib.rcParams['axes.titlesize'] = args.fontsize + 2
    matplotlib.rcParams['xtick.labelsize'] = args.fontsize
    matplotlib.rcParams['ytick.labelsize'] = args.fontsize
    matplotlib.rcParams['legend.fontsize'] = args.fontsize
    matplotlib.rcParams['font.family'] = 'serif'
    matplotlib.rcParams['font.serif'] = ['Computer Modern Roman']
    matplotlib.rcParams['text.usetex'] = True
    matplotlib.rcParams['figure.max_open_warning'] = 400
    matplotlib.rcParams['image.cmap'] = "gray"
    matplotlib.rcParams['image.interpolation'] = "none"
    matplotlib.rcParams['figure.autolayout'] = True
    pylab.clf()                     # Essential! Otherwise the plots will be f**d up!
    pylab.figure(1)
    pylab.gca().yaxis.grid(True)    # Makes it easier to compare bars
    pylab.gca().xaxis.grid(False)
    pylab.gca().set_axisbelow(True)
    plt.style.use(args.pyplot_style)

    cmd_list = json.load(args.results)['cmd_list']
    cmd_list = util.filter_cmd_list(cmd_list, args.labels_to_include, args.labels_to_exclude)
    (cmd_list, label_map) = util.translate_dict(cmd_list, args.label_map)

    # For a bar-chart, we need labels, values, and errors
    labels = [util.texsafe(cmd['label']) for cmd in cmd_list]
    values = []
    std = []
    for cmd in cmd_list:
        res = util.extract_succeed_results(cmd, args.parse_regex, args.py_type)
        if len(res) == 0:
            res = [0]
        values.append(util.mean(res))
        std.append(util.standard_deviation(res))

    # Let's write the bar-chart using matplotlib
    margin = 0.05
    width = (1. - 1. * margin) / len(cmd_list)
    ind = np.arange(len(cmd_list))  # the x locations for each bar
    fig, ax = plt.subplots()
    ax.bar(ind * width, values, width, log=args.ylog, yerr=std)

    if args.ymin is not None:
        plt.ylim(ymin=float(args.ymin))
    if args.ymax is not None:
        plt.ylim(ymax=float(args.ymax))
    if args.title is not None:
        plt.title(util.texsafe(args.title))

    # Add some text for labels, title and axes ticks
    ax.set_xticks(ind*width+width/2.)
    ax.set_xticklabels(labels, rotation=args.xticklabel_rotation)

    if args.ylabel is not None:
        ax.set_ylabel(args.ylabel)

    # Now make some labels
    value_labels(ax, ax.patches)

    if args.output is not None:
        fname = args.output.name
        fformat = fname.split('.')[-1]
        print ("Writing file '%s' using format '%s'." % (fname, fformat))
        if args.mpld3:
            import mpld3
            if fformat == "html":
                mpld3.save_html(fig, args.output)
            elif fformat == "json":
                mpld3.save_json(fig, args.output)
            else:
                raise ValueError("--mpld3: The output must be either `html` or `json`")
        else:
            pylab.savefig(args.output, format=fformat)
    else:
        if args.mpld3:
            import mpld3
            mpld3.show()
        else:
            pylab.show()


def main():
    parser = util.default_argparse('Plots the result of a Benchpress JSON-file (one bar per command)')
    parser.add_argument(
        '--title',
        default=None,
        help='The title of the chart.'
    )
    parser.add_argument(
        '--warmups',
        default=0,
        type=int,
        help="Specify the amount of samples from warm-up rounds."
    )
    parser.add_argument(
        '--ymax',
        default=None,
        help="Max value of the y-axis"
    )
    parser.add_argument(
        '--ymin',
        default=None,
        help="Min value of the y-axis"
    )
    parser.add_argument(
        '--ylog',
        default=False,
        action='store_true',
        help="Makes the y-axis logarithmic"
    )
    parser.add_argument(
        '--ylabel',
        default="Elapsed time in seconds",
        help="Label on the y-axis"
    )
    parser.add_argument(
        '--xticklabel-rotation',
        default=90,
        metavar='DEGREE',
        type=int,
        help="The rotation of the labels on the x-axis"
    )
    parser.add_argument(
        '--no-legend',
        default=False,
        action='store_true',
        help="Hide the legend box"
    )
    parser.add_argument(
        '--fontsize',
        default=12,
        type=int,
        help="Fontsize"
    )
    parser.add_argument(
        '--pyplot-style',
        default='seaborn-darkgrid',
        type=str,
        choices=plt.style.available,
        help="The matplotlib.pyplot.style to use"
    )
    parser.add_argument(
        '--mpld3',
        action='store_true',
        help="Generate mpld3 plots <https://mpld3.github.io>"
    )
    args = parser.parse_args()
    one_bar_per_cmd(args)


if __name__ == "__main__":
    main()
