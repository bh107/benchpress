# -*- coding: utf-8 -*-
from __future__ import absolute_import
import json
from benchpress.visualizer import util
from benchpress import time_util


def visualize(args):
    """Return the visualized output"""

    # First we create `means` which map a command label and date to a pair of mean and standard deviation
    # e.g. means['Bean']['2017-05-02 13:29:34.87'] = (0.1289, 0.0006)
    (means, cmd_labels, meta_keys) = util.means_series_map(args)

    # Then we write the data
    ret = "Label%s " % args.csv_separator
    for meta_key in meta_keys:
        ret += "%s%s " % (meta_key, args.csv_separator)
    for cmd_label in cmd_labels:
        ret += "\n%s%s " % (cmd_label, args.csv_separator)
        for meta_key in meta_keys:
            (mean, std) = means[cmd_label].get(meta_key, (0, 0))
            ret += "%.4f (%.4f)%s " % (mean, std, args.csv_separator)
    return ret


def main():
    parser = util.default_argparse('Prints the result of a series of Benchpress JSON-files.', True)
    parser.add_argument(
        "--csv-separator",
        type=str,
        default=',',
        metavar="sep",
        help="Use the CSV format using 'sep' as the separator."
    )
    parser.add_argument(
        '--meta-key',
        default='creation_date_utc',
        type=str,
        choices=['creation_date_utc', 'tag'],
        help="The meta key, which value vary throughout the series"
    )
    args = parser.parse_args()
    if args.output is not None:
        args.output.write(visualize(args))
    else:
        print(visualize(args))


if __name__ == "__main__":
    main()
