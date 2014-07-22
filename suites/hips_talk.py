scripts = [('Heat Equation 26k**2*10','','26000 10')]


C = {
    'bridges': [
                ('C_seq', '~/benchmark/heat-eq-jacobi/c/sequential {args}', {'OMP_NUM_THREADS':1}), 
		('C_omp*1', '~/benchmark/heat-eq-jacobi/c/openmp {args}', {'OMP_NUM_THREADS':1}),
		('C_omp*2', '~/benchmark/heat-eq-jacobi/c/openmp {args}', {'OMP_NUM_THREADS':2}),
		('C_omp*8', '~/benchmark/heat-eq-jacobi/c/openmp {args}', {'OMP_NUM_THREADS':8}),
		('C_cluster2*8', 'mpiexec -ppn 1 -np 2 ~/benchmark/heat-eq-jacobi/c/openmp_mpi {args}', {'OMP_NUM_THREADS':8}),
		('C_cluster8*8', 'mpiexec -ppn 1 -np 8 ~/benchmark/heat-eq-jacobi/c/openmp_mpi {args}', {'OMP_NUM_THREADS':8}),
		('C_cluster8*16', 'mpiexec -ppn 1 -np 8 ~/benchmark/heat-eq-jacobi/c/openmp_mpi {args}', {'OMP_NUM_THREADS':16}),
		('C_cluster8*32', 'mpiexec -ppn 1 -np 8 ~/benchmark/heat-eq-jacobi/c/openmp_mpi {args}', {'OMP_NUM_THREADS':32}),
	       ],
    'scripts': scripts,
    'use_slurm_default': True,
}

managers = [
    ('node',  'node', '',  None),
    ('cluster8',  'cluster', 'mpiexec -ppn 1 -np 1 {bridge} : -np 7 ~/.local/bin/bh_vem_cluster_slave',  {'BH_SLURM_NNODES':8}),
]

python = {
    'bridges': [('numpy_bohrium', 'python ~/benchmark/heat-eq-jacobi/python/bohrium_numpy.py {args}', None)],
    'engines': [('omp*1',  'cpu', {'OMP_NUM_THREADS':1}), 
                ('omp*8',  'cpu', {'OMP_NUM_THREADS':8}),
                ('omp*16',  'cpu', {'OMP_NUM_THREADS':16}),
                ('omp*32', 'cpu', {'OMP_NUM_THREADS':32})],
    'managers': managers,
    'scripts': scripts,
    'use_slurm_default': True,
}

python_native = {
    'bridges': [('numpy_pure', 'python ~/benchmark/heat-eq-jacobi/python/pure_numpy.py {args}', None)],
    'scripts': scripts,
    'use_slurm_default': True,
}


gpu_scripts = [('Heat Equation 6k**2*1000','','6000 1000')]

opencl = {
    'bridges': [('opencl', '~/benchmark/heat-eq-jacobi/opencl/heat_eq_jacobi ~/benchmark/heat-eq-jacobi/opencl/heat_eq_jacobi.cl {args}', None)],
    'scripts': gpu_scripts,
    'use_slurm_default': False,
}

bh_gpu = {
    'bridges': [('bh_gpu', 'python ~/benchmark/heat-eq-jacobi/python/bohrium_numpy.py {args}', None)],
    'engines': [('GPU',  'gpu', None)], 
    'managers': [('node',  'node', '',  None)],
    'scripts': gpu_scripts,
    'use_slurm_default': False,
}

suites = [C, python_native, python]
suites = [opencl, bh_gpu] + suites

#suites = [python]
