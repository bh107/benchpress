
managers = [
    ('node',  'node', '',  None),
    ('cluster1',  'cluster', 'mpiexec -ppn 1 -np 1 {bridge} : -np 0 ./vem/cluster/bh_vem_cluster_slave',  {'BH_SLURM_NNODES':1}),
    ('cluster2',  'cluster', 'mpiexec -ppn 1 -np 1 {bridge} : -np 1 ./vem/cluster/bh_vem_cluster_slave',  {'BH_SLURM_NNODES':2}),
    ('cluster4',  'cluster', 'mpiexec -ppn 1 -np 1 {bridge} : -np 3 ./vem/cluster/bh_vem_cluster_slave',  {'BH_SLURM_NNODES':4}),
    ('cluster8',  'cluster', 'mpiexec -ppn 1 -np 1 {bridge} : -np 7 ./vem/cluster/bh_vem_cluster_slave',  {'BH_SLURM_NNODES':8}),
]

engines = [('cpu',  'cpu',   None)]

python_script = [\
#		 ('N-body 15k',        'nbody',        '--size=15000*10'),
#		 ('N-body 20k',        'nbody',        '--size=20000*10'),
#                 ('Shallow Water 20k', 'shallow_water','--size=20000*20000*10'),
                 ('Shallow Water 25k', 'shallow_water','--size=25000*25000*10'),
#                 ('Black Scholes 10m', 'black_scholes','--size=10000000*10'),
 #                ('Black Scholes 100m','black_scholes','--size=100000000*10')
]

python = {
    'bridges': [('numpy', 'python benchmark/Python/{script}.py {args} --bohrium=True', None)],
    'engines': engines,
    'managers': managers,
    'scripts': python_script
}
python_native = {
    'bridges': [('numpy-native', 'python benchmark/Python/{script}.py {args} --bohrium=False', None)],
    'scripts': python_script
}

suites = [python_native]#, python]

