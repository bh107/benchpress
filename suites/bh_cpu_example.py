from default import *

#
#   Example Bohrium stack configuration
#
bh_cpu_stack = [
    ('bridge',  [('default',    'bridge',             None)]),
    ('filter',  [('creduce',    'complete_reduction', None)]),
    ('vem',     [('node',       'node',               None)]),
    ('fuser',   [('topo',       'topological',        None)]),
    ('ve',      [('cpu',        'cpu',                None)])
]

#
#   Scripts
#
scripts = [
    ('Black Scholes',   'black_scholes',  '--size=100000*10'),
    ('Monte Carlo PI',  'mc',             '--size=100000*100'),

#
#   Default launchers (python_numpy, python_bohrium) are used.
#

#
#   Putting them together in the following example suite definition
#
bh_example_suite = {
    'launchers': [python_bohrium],
    'scripts': scripts,
    'bohrium': bh_cpu_stack
}

np_example_suite = {
    'launchers': [python_numpy],
    'scripts': scripts
}

#
#   As usual, put them into the list of suites to run.
#
suites = [
    bh_cpu_suite,
    np_cpu_suite
]
