c_seq = [('Heat Equation 1000*1000*10','','1000 1000')]
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
    'scripts': c_seq
}

suites = [C]

