from benchpress.default import *

suites = [{
    "scripts": [('Leibnitz PI',   'leibnitz_pi',  '--size=1000')],
    "launchers": [python_numpy],
    "bohrium": bh_stack_none,
    "use_slurm_default": True,
}]
