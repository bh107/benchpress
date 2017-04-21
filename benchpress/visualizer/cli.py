# -*- coding: utf-8 -*-

import argparse
import json
import re


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
    parser = argparse.ArgumentParser(description='Prints the result of a Benchpress JSON-file.')
    parser.add_argument("results", help="JSON file containing results")
    parser.add_argument(
        "--regex",
        type=str,
        default='elapsed-time: ([\d.]+)',
        help="How to parse the result of each run. The RegEX should contain exactly one group."
    )
    parser.add_argument(
        "--py_type",
        choices=['float', 'int', 'str'],
        default='float',
        help="The Python data type of the parsed results."
    )
    args = parser.parse_args()
    # Convert the type represented as a string to a Python type object e.g. "float" => float
    args.py_type = eval(args.py_type)
    print (visualize(args))


if __name__ == "__main__":
    main()
