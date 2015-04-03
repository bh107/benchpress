from default import *

scripts   = [
    ('Jacobi Stencil',  'jacobi_stencil', '--size=1000*1000*10'),
]

python = {
    'bridges':  [dython_numpy],
    'scripts':  scripts,
}

suites = [
    python
]

