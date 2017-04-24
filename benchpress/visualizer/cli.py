# -*- coding: utf-8 -*-

import json
import re
from benchpress.visualizer import util


def visualize(args):
    """Return the visualized output"""

    ret = ""
    cmd_list = json.load(args.results)
    cmd_list = util.filter_cmd_list(cmd_list, args.labels_to_include, args.labels_to_exclude)
    (cmd_list, label_map) = util.translate_dict(cmd_list, args.label_map)
    for cmd in cmd_list:
        values = []
        for job in cmd['jobs']:
            for res in job['results']:
                match = re.search(args.regex, res['stdout'])
                if res['success'] and match:
                    values.append(args.py_type(match.group(1)))
                else:
                    values.append("N/A")
        ret += "%s: %s" % (label_map[cmd['label']], values)
        succeed_values = util.extract_succeed_results(cmd, args.regex, args.py_type)
        if len(succeed_values) > 0:
            ret += " %.4f" % util.mean(succeed_values)
            ret += " (%.4f)" % util.standard_deviation(succeed_values)
        ret += "\n"
    return ret


def main():
    parser = util.default_argparse('Prints the result of a Benchpress JSON-file.')
    args = parser.parse_args()
    if args.output is not None:
        args.output.write(visualize(args))
    else:
        print(visualize(args))


if __name__ == "__main__":
    main()
