from default import *

scripts   = [
    ('Jacobi Stencil',  'jacobi_stencil', '--size=8000*1000*10'),
]

python = {
    'bridges':  [('python-numpy', 'python benchmark/Python/{script}.py {args} --bohrium=False', None)],
    'scripts':  scripts,
}

suites = [
    python
]

