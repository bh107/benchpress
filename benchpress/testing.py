# -*- coding: utf-8 -*-
"""
#####################
Testing of Benchpress
#####################

To run the test use::

    python -m benchpress.testing
    
.. note:: Do not run this file directly such as ``python benchpress/testing.py`` it will not work!

"""
from __future__ import absolute_import
import unittest
import tempfile
from os.path import join
import sys
import benchpress as bp
import json
import jsonschema


def create_test_suite(suite_path):
    from benchpress.suite_util import BP_ROOT

    scripts = [
        ('X-ray', 'xraysim', ["10*10*1", "20*10*1"]),
        ('Bean', 'galton_bean_machine', ["10000*10", "20000*10"]),
    ]

    cmd_list = []
    for label, name, sizes in scripts:
        for size in sizes:
            full_label = "%s/%s" % (label, size)
            bash_cmd = "python {root}/benchmarks/{script}/python_numpy/{script}.py --size={size}" \
                .format(root=BP_ROOT, script=name, size=size)
            cmd_list.append(bp.command(bash_cmd, full_label))
    bp.create_suite(cmd_list, suite_path)


class SuiteSchema(unittest.TestCase):

    def testSchema(self):
        from . import run
        from . import suite_schema
        tmpdir = tempfile.mkdtemp()
        suite_file = join(tmpdir, "res.json")

        # Check after suite creation
        create_test_suite(suite_file)
        with open(suite_file, "r") as f:
            suite = json.load(f)
            jsonschema.validate(suite, suite_schema)

        # Check after run
        old_argv = sys.argv[:]
        sys.argv[:] = [old_argv[0], suite_file]
        run.main()
        sys.argv = old_argv
        with open(suite_file, "r") as f:
            suite = json.load(f)
            jsonschema.validate(suite, suite_schema)


class BP(unittest.TestCase):

    def setUp(self):
        from . import run
        self.tmpdir = tempfile.mkdtemp()
        self.suite_file = join(self.tmpdir, "res.json")
        create_test_suite(self.suite_file)
        old_argv = sys.argv[:]
        sys.argv[:] = [old_argv[0], self.suite_file]
        run.main()
        sys.argv = old_argv

    def tearDown(self):
        pass

    def testCli(self):
        from .visualizer import cli
        old_argv = sys.argv
        sys.argv = [old_argv[0], self.suite_file]
        cli.main()

    def testCliCSV(self):
        from .visualizer import cli
        old_argv = sys.argv
        sys.argv = [old_argv[0], self.suite_file, "--csv"]
        cli.main()

    def testJSON(self):
        from . import suite_schema
        with open(self.suite_file, "r") as f:
            suite = json.load(f)
            jsonschema.validate(suite, suite_schema)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
