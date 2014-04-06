from default import *

scripts = [
    ('Convolve',    'convolve',     '--size=25'),
    ('Wireworld',   'wireworld',    '--size=1000*10'),
    ('27-Point',    'point27',      '--size=400*10'),
]

managers= [('node', 'node', '', None)]

numpy = {
    'bridges':  [('NumPy', 'python benchmark/Python/{script}.py {args} --bohrium=False', None)],
    'scripts':  scripts,
}

bohrium = {
    'bridges':  [('Bohrium',    'python benchmark/Python/{script}.py {args} --bohrium=True', None)],
    'managers': [('node',       'node', '',  None)],
    'engines':  [('cpu',        'cpu',  None)],
    'scripts':  scripts
}

suites = [
    bohrium,
    numpy
]

