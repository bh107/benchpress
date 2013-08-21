from default import *

scripts   = [
#    ('Black Scholes',        'black_scholes',   '--size=1000000*20'),
    ('Monte Carlo PI',       'monte_carlo_pi',  '--size=10000000*20'),
]

bohrium = {
    'bridges':  [('cpp', 'benchmark/cpp/bin/{script} {args}', None)],
    'managers': [('node',  'node', '',  None)],
    'engines': [
        ('cpu',         'cpu',      {'BH_CORE_VCACHE_SIZE': '10'}),
        ('dynamite',    'dynamite', {'BH_VE_DYNAMITE_DOFUSE': '0', 'BH_CORE_VCACHE_SIZE': '10'}),
        ('dynamite_fused',    'dynamite', {'BH_DISABLE_BHIR_GRAPH':'1', 'BH_CORE_VCACHE_SIZE': '10'}),
    ],
    'scripts':  scripts
}

suites = [
    bohrium,
]

