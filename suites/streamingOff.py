from benchpress.default import *

scripts = [
    ('X-ray 020^3 40^2',  'xraysim',     '--size=20*40*5'),
    ('MC Pi 0.1G',   'montecarlo_pi',    '--size=100000000*5'),
    ('MFE 040^2',    'idl_init_explode', '--size=40*40*5'),
]

stack_openmp = [
    [('default',    'bridge',       None)],
    [('bcexp',      'bcexp_openmp', None)],
    [('bccon',      'bccon_openmp', None)],
    [\
      ('streamOn',  'node',  {"BH_OPENMP_ARRAY_CONTRACTION":"1"}),
      ('streamOff', 'node',  {"BH_OPENMP_ARRAY_CONTRACTION":"0"}) \
    ],
    [('openmp',     'openmp',       None)],
]

suite_openmp = {
    'scripts': scripts,
    'launchers':  [python_bohrium],
    'bohrium': stack_openmp
}
suite_numpy = {
    'scripts': scripts,
    'launchers':  [python_numpy],
    'bohrium': bh_stack_none
}

suites = [
    suite_openmp,
    suite_numpy,
]

