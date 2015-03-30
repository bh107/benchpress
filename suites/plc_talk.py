scriptso = [('Heat Equation 2k x 2k','','2000 2000 1000')
           , ('Heat Equation 4k x 4k','','4000 4000 1000')
           , ('Heat Equation 8k x 8k','','8000 8000 1000')
           ]

scriptsb = [('Heat Equation 2k x 2k','','2000*2000*1000')
           , ('Heat Equation 4k x 4k','','4000*4000*1000')
           , ('Heat Equation 8k x 8k','','8000*8000*1000')
           ]

scriptsp = [('Heat Equation 2k x 2k','','2000*2000*100')
           , ('Heat Equation 4k x 4k','','4000*4000*100')
           , ('Heat Equation 8k x 8k','','8000*8000*100')
           ]


numpy32 = {
    'bridges': [('numpy32', 'python benchmark/python/heat_equation.py --dtype=float32 --bohrium=False --size={args}', None)],
    'scripts': scriptsp
}

numpy64 = {
    'bridges': [('numpy64', 'python benchmark/python/heat_equation.py --dtype=float64 --bohrium=False --size={args}', None)],
    'scripts': scriptsp
}

opencl32 = {
    'bridges': [('opencl32', '~/bohrium/benchmark/heat-eq-jacobi/opencl/heat_eq_jacobi32 ~/bohrium/benchmark/heat-eq-jacobi/opencl/heat_eq_jacobi.cl {args}', None)],
    'scripts': scriptso
}

opencl64 = {
    'bridges': [('opencl64', '~/bohrium/benchmark/heat-eq-jacobi/opencl/heat_eq_jacobi64 ~/bohrium/benchmark/heat-eq-jacobi/opencl/heat_eq_jacobi.cl {args}', None)],
    'scripts': scriptso
}

bohrium32 = {
    'bridges': [('bohrium32', 'python benchmark/python/heat_equation.py --dtype=float32 --bohrium=True --size={args}', None)],
    'engines': [('GPU',  'gpu', None)], 
    'managers': [('node',  'node', '',  None)],
    'scripts': scriptsb
}

bohrium64 = {
    'bridges': [('bohrium64', 'python benchmark/python/heat_equation.py --dtype=float64 --bohrium=True --size={args}', None)],
    'engines': [('GPU',  'gpu', None)], 
    'managers': [('node',  'node', '',  None)],
    'scripts': scriptsb
}


suites = [numpy32,numpy64,opencl32,opencl64,bohrium32,bohrium64]
