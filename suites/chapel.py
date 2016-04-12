from benchpress.default import *

scripts   = [
    ('Heat Equation',  'heat_equation', '--size=100*10'),
]

chapel = {
    'launchers':  [chapel_mcore],
    'scripts':  scripts,
}

suites = [
    chapel
]

