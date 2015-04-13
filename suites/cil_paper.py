from default import *

scripts = [
    ('Black Scholes',           'black_scholes',            '--size=5000000*10'),
]

references = {
    'bridges':  [python_numpy, cil_managed, cil_unsafe],
    'scripts':  scripts,
}

bohrium = {
    'bridges':  [cil_bohrium],
    'managers': [('node',  'node', '',  None)],
    'engines':  [('cpu', 'cpu', None)],
    'scripts':  scripts
}

suites = [
    references,
    bohrium
]

