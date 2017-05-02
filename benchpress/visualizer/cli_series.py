# -*- coding: utf-8 -*-
from __future__ import absolute_import
import json
from benchpress.visualizer import util
from benchpress import time_util


def visualize(args):
    """Return the visualized output"""

    # First we create `means` which map a command label and date to a pair of mean and standard deviation
    # e.g. means['Bean']['2017-05-02 13:29:34.87'] = (0.1289, 0.0006)
    means = {}
    cmd_labels = set()
    creation_dates = set()
    for result in args.results:
        suite = json.load(result)
        creation_date = time_util.str2time(suite['creation_date_utc'])
        cmd_list = suite['cmd_list']
        cmd_list = util.filter_cmd_list(cmd_list, args.labels_to_include, args.labels_to_exclude)
        for cmd in cmd_list:
            succeed_values = util.extract_succeed_results(cmd, args.parse_regex, args.py_type)
            mean = util.mean(succeed_values)
            std = util.standard_deviation(succeed_values)
            if cmd['label'] not in means:
                means[cmd['label']] = {}
            means[cmd['label']][creation_date] = (mean, std)
            cmd_labels.add(cmd['label'])
            creation_dates.add(creation_date)

    creation_dates = sorted(list(creation_dates))
    ret = "Label%s " % args.csv_separator
    for creation_date in creation_dates:
        ret += "%s%s " % (creation_date, args.csv_separator)
    for cmd_label in cmd_labels:
        ret += "\n%s%s " % (cmd_label, args.csv_separator)
        for creation_date in creation_dates:
            (mean, std) = means[cmd_label].get(creation_date, (0, 0))
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
    args = parser.parse_args()
    if args.output is not None:
        args.output.write(visualize(args))
    else:
        print(visualize(args))


if __name__ == "__main__":
    main()
