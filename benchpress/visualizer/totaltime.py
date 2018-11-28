# -*- coding: utf-8 -*-
from __future__ import absolute_import
import json
import re
from benchpress.visualizer import util


def visualize(args):
    """Return the visualized output"""

    total = 0
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
        total += util.mean(succeed_values)
    return total


def main():
    parser = util.default_argparse('Print the total time of all benchmarks in the JSON-file.')
    args = parser.parse_args()
    if args.output is not None:
        args.output.write(str(visualize(args)))
    else:
        print("Total time of all benchmarks: %f" % visualize(args))


if __name__ == "__main__":
    main()
