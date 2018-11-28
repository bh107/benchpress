import benchpress as bp
from benchpress.suite_util import BP_ROOT

""" Use this benchmark for testing performance of Bohrium"""

scripts = [
    ('shallow_water', "2000*2000*100"),
    ('heat_equation', "2000*2000*100"),
    ('convolve1d', "1000000*100*100"),
    ('galton_bean_machine', "5000000*100"),
    ('montecarlo_pi', "5000000*100"),
]

cmd_list = []
for name, size in scripts:
    bash_cmd = "python -m bohrium {root}/benchmarks/{script}/python_numpy/{script}.py {size}" \
        .format(root=BP_ROOT, script=name, size=size)
    for stack in ['openmp', 'opencl']:
        full_label = "%s/%s/%s" % (stack, name, size)
        env = {'BH_STACK': stack}
        cmd_list.append(bp.command(bash_cmd, full_label, env))

bp.create_suite(cmd_list)
