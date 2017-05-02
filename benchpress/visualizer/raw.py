# -*- coding: utf-8 -*-
from __future__ import absolute_import
import json
from benchpress.visualizer import util


def visualize(args):
    """Return the visualized output"""

    ret = ""
    cmd_list = json.load(args.results)['cmd_list']
    cmd_list = util.filter_cmd_list(cmd_list, args.labels_to_include, args.labels_to_exclude)
    (cmd_list, label_map) = util.translate_dict(cmd_list, args.label_map)
    for cmd in cmd_list:
        ret += "DUMP of '%s'\n" % cmd['label']
        for job in cmd['jobs']:
            for res in job['results']:
                if not args.no_stdout:
                    ret += "\tSTDOUR:\n"
                    ret += "%s\t%s%s\n" % (util.Color.GREEN, res['stdout'].replace('\n', '\n\t'), util.Color.END)
                if not args.no_stderr:
                    ret += "\tSTDERR:\n"
                    ret += "%s\t%s%s\n" % (util.Color.FAIL, res['stderr'].replace('\n', '\n\t'), util.Color.END)
    return ret


def main():
    parser = util.default_argparse('Raw dump of the stdout and stderr in a Benchpress JSON-file.')
    parser.add_argument(
        "--no-stdout",
        action="store_true",
        help="Don't dump stdout."
    )
    parser.add_argument(
        "--no-stderr",
        action="store_true",
        help="Don't dump stderr."
    )
    args = parser.parse_args()
    if args.output is not None:
        args.output.write(visualize(args))
    else:
        print(visualize(args))


if __name__ == "__main__":
    main()
