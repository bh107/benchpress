from default import *

scholes = [
    ('Black Scholes',        'black_scholes',   '--size=125000*10'),
    ('Black Scholes',        'black_scholes',   '--size=250000*10'),
    ('Black Scholes',        'black_scholes',   '--size=500000*10'),
    ('Black Scholes',        'black_scholes',   '--size=1000000*10'),
    ('Black Scholes',        'black_scholes',   '--size=2000000*10'),
    ('Black Scholes',        'black_scholes',   '--size=4000000*10'),
]

scripts = scholes

engines = [
    ('cpu',     'cpu',      {'BH_CORE_VCACHE_SIZE':  '0', 'BH_VE_CPU_TRAVERSAL': 'naive'}),
    ('cpu_vc',  'cpu',      {'BH_CORE_VCACHE_SIZE': '30', 'BH_VE_CPU_TRAVERSAL': 'naive'}),
    ('floops',  'cpu',      {'BH_CORE_VCACHE_SIZE': '30', 'BH_VE_CPU_TRAVERSAL': 'fruit_loops'}),
    ('tiling',  'tiling',   {'BH_CORE_VCACHE_SIZE': '30'}),
    ('dynamite','dynamite', {'BH_CORE_VCACHE_SIZE': '30'}),
    ('mcore',   'mcore',    {'BH_CORE_VCACHE_SIZE': '30'}),
]
managers= [('node', 'node', '', None)]

cpp = {
    'bridges': [('Bh/cpp', './benchmark/cpp/bin/{script} {args}', None)],
    'managers': managers,
    'engines':  engines,
    'scripts':  scripts
}

blitz = {
    'bridges': [('Blitz++', './benchmark/blitz/bin/{script} {args}', None)],
    'scripts':  scripts
}

arma = {
    'bridges': [('Armadillo', './benchmark/armadillo/bin/{script} {args}', None)],
    'scripts':  scripts
}

suites = [
    cpp,
    blitz,
    arma
]

