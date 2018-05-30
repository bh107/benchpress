# -*- coding: utf-8 -*-
from __future__ import absolute_import
import json
import re
from benchpress.visualizer import util


def visualize(args):
    """Return the visualized output"""

    ret = ""
    cmd_list = json.load(args.results)['cmd_list']
    cmd_list = util.filter_cmd_list(cmd_list, args.labels_to_include, args.labels_to_exclude)
    (cmd_list, label_map) = util.translate_dict(cmd_list, args.label_map)
    for cmd in cmd_list:
        values = []
        if 'jobs' in cmd:
            for job in cmd['jobs']:
                if 'results' in job:
                    for res in job['results']:
                        match_list = re.findall(args.parse_regex, res['stdout'])
                        if res['success'] and len(match_list) > 0:
                            for match in match_list:
                                values.append(args.py_type(match))
                        else:
                            values.append("N/A")
        succeed_values = util.extract_succeed_results(cmd, args.parse_regex, args.py_type)
        mean = util.mean(succeed_values)
        std = util.standard_deviation(succeed_values)
        if args.csv:
            sep = args.csv_separator
            ret += "%s%s %.4f%s %.4f" % (label_map[cmd['label']], sep, mean, sep, std)
        else:
            ret += "%s: %s" % (label_map[cmd['label']], values)
            if len(succeed_values) > 0:
                ret += " %.4f" % mean
                ret += " (%.4f)" % std
        ret += "\n"
    return ret


def main():
    parser = util.default_argparse('Prints the result of a Benchpress JSON-file.')
    parser.add_argument(
        "--csv",
        action="store_true",
        help="Use the CSV format using 'separator' as the separator."
    )
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
