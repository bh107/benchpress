from default import *

scripts   = [
        ('numpytest',  '', ''),
]

python = {
    'bridges': [('python', 'python test/numpy/numpytest.py', None)],
    'engines': [('CPU', 'cpu', None),
                ('GPU', 'gpu', None)],
    'scripts':  scripts,
}

suites = [
    python
]

