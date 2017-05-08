# -*- coding: utf-8 -*-
from __future__ import absolute_import
from benchpress.visualizer import util


def value_labels(ax, rects):
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%.2f' % float(height),
                ha='center', va='bottom')


def line_per_cmd(args):
    import matplotlib
    if args.output is not None:
        matplotlib.use('Agg') # We need this to make matplotlib work on systems with no DISPLAY
    import matplotlib.pyplot as plt
    import pylab

    matplotlib.rcParams.update({'figure.subplot.right': args.plot_size})
    matplotlib.rcParams.update({'figure.subplot.bottom': args.plot_size})
    plt.style.use(args.pyplot_style)

    # First we create `means` which map a command label and date to a pair of mean and standard deviation
    # e.g. means['Bean']['2017-05-02 13:29:34.87'] = (0.1289, 0.0006)
    (means, cmd_labels, meta_keys) = util.means_series_map(args)

    # Let's write a plot line for each command label
    fig, ax = plt.subplots()
    lines = []
    for cmd_label in cmd_labels:
        x, y, err = ([], [], [])
        for i in range(len(meta_keys)):
            (mean, std) = means[cmd_label].get(meta_keys[i], (0, 0))
            x.append(i)
            y.append(mean)
            err.append(std)
        lines.append(ax.errorbar(x, y, fmt='-o', yerr=err))

    if args.ymin is not None:
        plt.ylim(ymin=float(args.ymin))
    if args.ymax is not None:
        plt.ylim(ymax=float(args.ymax))
    if args.title is not None:
        plt.title(util.texsafe(args.title))

    # Add some text for labels, title and axes ticks
    ax.set_xticks(range(len(meta_keys)))
    ax.set_xticklabels(meta_keys, rotation=args.xticklabel_rotation)

    if not args.no_legend and not args.mpld3: # mpld3 comes with its own legends
        ax.legend(lines, cmd_labels, loc='best', fancybox=True, shadow=True)

    if args.mpld3:
        import mpld3
        from mpld3 import plugins
        interactive_legend = plugins.InteractiveLegendPlugin(lines, cmd_labels)
        plugins.connect(fig, interactive_legend)

    if args.output is not None:
        fname = args.output.name
        fformat = fname.split('.')[-1]
        print ("Writing file '%s' using format '%s'." % (fname, fformat))
        if args.mpld3:
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
            mpld3.show()
        else:
            pylab.show()


def main():
    parser = util.default_argparse('Plots the result of a Benchpress JSON-file (one bar per command)', True)
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
        '--plot-size',
        type=float,
        default=0.7,
        help="Size of the plot compared to total figure (0.1 to 1.0)"
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
        help="The matplotlib.pyplot.style to use"
    )
    parser.add_argument(
        '--meta-key',
        default='creation_date_utc',
        type=str,
        choices=['creation_date_utc', 'tag'],
        help="The meta key, which value vary throughout the series"
    )
    parser.add_argument(
        '--mpld3',
        action='store_true',
        help="Generate mpld3 plot <https://mpld3.github.io>"
    )
    args = parser.parse_args()
    line_per_cmd(args)


if __name__ == "__main__":
    main()
