from default import *

scripts   = [
        ('numpytest',  '', ''),
]

python = {
    'bridges':  [('python', 'python test/numpy/numpytest.py', None)],
    'scripts':  scripts,
}

suites = [
    python
]

