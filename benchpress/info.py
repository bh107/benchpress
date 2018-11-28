# -*- coding: utf-8 -*-
from __future__ import absolute_import
import argparse
import os
from . import suite_util


def main():
    parser = argparse.ArgumentParser(description='Print Benchpress installation info')
    parser.add_argument(
        '--suites',
        action="store_true",
        help="Show the path to the suites directory."
    )
    args = parser.parse_args()

    if args.suites:
        print(os.path.join(suite_util.BP_ROOT, "suites"))


if __name__ == "__main__":
    main()
