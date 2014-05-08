scripts = [('Heat Equation 1000*1000*10','','6000 100')]


C = {
    'bridges': [
                ('C_seq', '~/benchmark/heat-eq-jacobi/c/sequential {args}', {'OMP_NUM_THREADS':1}), 
		('C_omp*1', '~/benchmark/heat-eq-jacobi/c/openmp {args}', {'OMP_NUM_THREADS':1}),
		('C_omp*2', '~/benchmark/heat-eq-jacobi/c/openmp {args}', {'OMP_NUM_THREADS':2}),
		('C_omp*8', '~/benchmark/heat-eq-jacobi/c/openmp {args}', {'OMP_NUM_THREADS':8}),
		('C_cluster2*8', 'mpiexec -np 2 ~/benchmark/heat-eq-jacobi/c/openmp_mpi {args}', {'OMP_NUM_THREADS':8}),
		('C_cluster4*8', 'mpiexec -np 4 ~/benchmark/heat-eq-jacobi/c/openmp_mpi {args}', {'OMP_NUM_THREADS':8}),
		('C_cluster8*8', 'mpiexec -np 8 ~/benchmark/heat-eq-jacobi/c/openmp_mpi {args}', {'OMP_NUM_THREADS':8}),
		('C_cluster8*32', 'mpiexec -np 8 ~/benchmark/heat-eq-jacobi/c/openmp_mpi {args}', {'OMP_NUM_THREADS':32}),
	       ],
    'scripts': scripts
}

managers = [
    ('node',  'node', '',  None),
    ('cluster8',  'cluster', 'mpiexec -np 1 {bridge} : -np 7 ~/.local/bin/bh_vem_cluster_slave',  {'BH_SLURM_NNODES':8}),
]

python = {
    'bridges': [('numpy_bohrium', 'python ~/benchmark/heat-eq-jacobi/python/bohrium_numpy.py {args}', None)],
    'engines': [('omp*1',  'cpu', {'OMP_NUM_THREADS':1}), 
                ('omp*8',  'cpu', {'OMP_NUM_THREADS':8})],
    'managers': managers,
    'scripts': scripts
}

python_native = {
    'bridges': [('numpy_pure', 'python ~/benchmark/heat-eq-jacobi/python/pure_numpy.py {args}', None)],
    'scripts': scripts
}

opencl = {
    'bridges': [('opencl', '~/benchmark/heat-eq-jacobi/opencl/heat_eq_jacobi ~/benchmark/heat-eq-jacobi/opencl/heat_eq_jacobi.cl {args}', None)],
    'scripts': scripts
}

bh_gpu = {
    'bridges': [('bh_gpu', 'python ~/benchmark/heat-eq-jacobi/python/bohrium_numpy.py {args}', None)],
    'engines': [('GPU',  'gpu', None)], 
    'managers': [('node',  'node', '',  None)],
    'scripts': scripts
}

suites = [C, python_native, python, opencl, bh_gpu]
suites = [opencl, bh_gpu]

