import benchpress as bp
from benchpress.suite_util import BP_ROOT

scripts = [
    ('X-ray',  'xraysim',  ["10*10*1", "20*10*1"]),
    ('Bean',   'galton_bean_machine',  ["10000*10", "20000*10"]),
]

cmd_list = []
for label, name, sizes in scripts:
    for size in sizes:
        full_label = "%s/%s" % (label, size)
        bash_cmd = "python {root}/benchmarks/{script}/python_numpy/{script}.py --size={size}" \
            .format(root=BP_ROOT, script=name, size=size)
        cmd_list.append(bp.command(bash_cmd, full_label))

# Finally, we build the Benchpress suite, which is written to `--output`
bp.create_suite(cmd_list)
