# -*- coding: utf-8 -*-

import argparse
import json
import re
from benchpress.visualizer import util


def visualize(args):
    """Return the visualized output"""

    ret = ""
    with open(args.results, 'r') as json_file:
        cmd_list = json.load(json_file)
        for cmd in cmd_list:
            values = []
            for job in cmd['jobs']:
                for res in job['results']:
                    match = re.search(args.regex, res['stdout'])
                    if res['success'] and match:
                        values.append(args.py_type(match.group(1)))
                    else:
                        values.append("N/A")
            ret += "%s: %s\n" % (cmd['label'], values)
    return ret


def main():
    parser = util.default_argparse('Prints the result of a Benchpress JSON-file.')
    args = parser.parse_args()
    print (visualize(args))


if __name__ == "__main__":
    main()
