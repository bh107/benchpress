from default import *

scripts = [
    ('Synthetic Inplace',   'synth_inplace',    '--size=100000000*10'),
    ('Black Scholes',       'black_scholes',    '--size=1000000*10')
]

managers= [('node', 'node', '', None)]

numpy = {
    'bridges':  [('NumPy', 'python benchmark/python/{script}.py {args} --bohrium=False', None)],
    'scripts':  scripts,
}

bohrium = {
    'bridges':  [('Bohrium', 'python benchmark/python/{script}.py {args} --bohrium=True', None)],
    'managers': [('node',  'node', '',  None) ],
    'fusers':   [('topological', 'topological', None)],
    'engines':  [
        ('fuse_01',   'cpu', {'BH_VE_CPU_JIT_FUSION': '1', 'OMP_NUM_THREADS': '1'}),
        ('fuse_02',   'cpu', {'BH_VE_CPU_JIT_FUSION': '1', 'OMP_NUM_THREADS': '2'}),
        ('fuse_04',   'cpu', {'BH_VE_CPU_JIT_FUSION': '1', 'OMP_NUM_THREADS': '4'}),
#        ('fuse_08',   'cpu', {'BH_VE_CPU_JIT_FUSION': '1', 'OMP_NUM_THREADS': '8'}),
#        ('fuse_16',   'cpu', {'BH_VE_CPU_JIT_FUSION': '1', 'OMP_NUM_THREADS': '16'}),
#        ('fuse_32',   'cpu', {'BH_VE_CPU_JIT_FUSION': '1', 'OMP_NUM_THREADS': '32'}),

        ('sij_01',  'cpu', {'BH_VE_CPU_JIT_FUSION': '0', 'OMP_NUM_THREADS': '1'}),
        ('sij_02',  'cpu', {'BH_VE_CPU_JIT_FUSION': '0', 'OMP_NUM_THREADS': '2'}),
        ('sij_04',  'cpu', {'BH_VE_CPU_JIT_FUSION': '0', 'OMP_NUM_THREADS': '4'}),
#        ('sij_08',  'cpu', {'BH_VE_CPU_JIT_FUSION': '0', 'OMP_NUM_THREADS': '8'}),
#        ('sij_16',  'cpu', {'BH_VE_CPU_JIT_FUSION': '0', 'OMP_NUM_THREADS': '16'}),
#        ('sij_32',  'cpu', {'BH_VE_CPU_JIT_FUSION': '0', 'OMP_NUM_THREADS': '32'}),
    ],
    'scripts':  scripts
}

suites = [
    bohrium,
    numpy
]

