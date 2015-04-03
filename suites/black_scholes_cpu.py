from default import *

scripts = [
    ('Black Scholes', 'black_scholes', '--size=5000000*10'),
]

fusion_1_32 = [
    ('fusion_01',   'cpu', {'BH_VE_CPU_JIT_FUSION': '1',    'OMP_NUM_THREADS': '1'  }),
    ('fusion_02',   'cpu', {'BH_VE_CPU_JIT_FUSION': '1',    'OMP_NUM_THREADS': '2'  }),
    ('fusion_04',   'cpu', {'BH_VE_CPU_JIT_FUSION': '1',    'OMP_NUM_THREADS': '4'  }),
    ('fusion_08',   'cpu', {'BH_VE_CPU_JIT_FUSION': '1',    'OMP_NUM_THREADS': '8'  }),
    ('fusion_16',   'cpu', {'BH_VE_CPU_JIT_FUSION': '1',    'OMP_NUM_THREADS': '16' }),
    ('fusion_32',   'cpu', {'BH_VE_CPU_JIT_FUSION': '1',    'OMP_NUM_THREADS': '32' }),
]

omp_1_32 = [
    ('omp_01',      'cpu', {'BH_VE_CPU_JIT_FUSION': '0',    'OMP_NUM_THREADS': '1'  }),
    ('omp_02',      'cpu', {'BH_VE_CPU_JIT_FUSION': '0',    'OMP_NUM_THREADS': '2'  }),
    ('omp_04',      'cpu', {'BH_VE_CPU_JIT_FUSION': '0',    'OMP_NUM_THREADS': '4'  }),
    ('omp_08',      'cpu', {'BH_VE_CPU_JIT_FUSION': '0',    'OMP_NUM_THREADS': '8'  }),
    ('omp_16',      'cpu', {'BH_VE_CPU_JIT_FUSION': '0',    'OMP_NUM_THREADS': '16' }),
    ('omp_32',      'cpu', {'BH_VE_CPU_JIT_FUSION': '0',    'OMP_NUM_THREADS': '32' }),
] 

suites = [
    {'bridges': [python_numpy],     'scripts': scripts}, 
    {'bridges': [cpp11_blitz],      'scripts': scripts},
    {'bridges': [cpp11_arma],       'scripts': scripts, 'engines': omp_1_32},
    {'bridges': [cpp11_bxx],        'scripts': scripts, 'engines': fusion_1_32 + omp_1_32, 'filters':  [('complete_reduction', 'complete_reduction', None)]},
    {'bridges': [python_bohrium],   'scripts': scripts, 'engines': fusion_1_32 + omp_1_32, 'filters':  [('complete_reduction', 'complete_reduction', None)]},
]

