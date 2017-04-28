#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Example of how to generate a Benchpress suite file 

"""

import benchpress as bp
from benchpress.suite_util import BP_ROOT

scripts = [
    ('X-ray',  'xraysim',  ["10*10*1", "20*10*1"]),
    ('Bean',   'galton_bean_machine',  ["10000*10", "20000*10"]),
]

python_numpy = [
    ("Python", "dython %s/benchmarks/{script}/python_numpy/{script}.py --size={size}" % BP_ROOT),
]

bohrium_numpy = [
    ("Bohrium", "dython -m bohrium %s/benchmarks/{script}/python_numpy/{script}.py --size={size}" % BP_ROOT),
]

backends = [
    ("OMP1", {'OMP_NUM_THREADS': 1, 'BH_STACK': 'openmp'}),
    ("OMP4", {'OMP_NUM_THREADS': 4, 'BH_STACK': 'openmp'}),
    ("GPU",  {'BH_STACK': 'opencl'}),
]

# Let's build the command list
cmd_list = []
for script_label, script_name, script_sizes in scripts:
    for size in script_sizes:
        # Commands for pure Python/NumPy
        for launcher_label, launcher_cmd in python_numpy:
            cmd_line = launcher_cmd.format(script=script_name, size=size)
            label = "%s/%s/%s" % (script_label, size, launcher_label)
            cmd_list.append(bp.command(cmd_line, label))
        # Commands for Bohrium, which include different combinations of execution backends
        for launcher_label, launcher_cmd in bohrium_numpy:
            cmd_line = launcher_cmd.format(script=script_name, size=size)
            for backend_label, backend_env in backends:
                label = "%s/%s/%s/%s" % (script_label, size, launcher_label, backend_label)
                cmd_list.append(bp.command(cmd_line, label, backend_env))

# Finally, we build the Benchpress suite, which is written to `--output`
bp.create_suite(cmd_list)
