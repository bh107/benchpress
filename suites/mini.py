from default import *

scripts   = [
    ('Jacobi Stencil',  'jacobi_stencil', '--size=1000*1000*10'),
]

python = {
    'bridges':  [('python-numpy', 'dython benchmark/python/{script}.py {args} --bohrium=False', None)],
    'scripts':  scripts,
}

suites = [
    python
]

