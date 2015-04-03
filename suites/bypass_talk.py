from default import *

managers = [
#    ('cluster2',  'cluster', 'mpiexec -ppn 1 -np 1 {bridge} : -np 1 ~/.local/bin/bh_vem_cluster_slave',  {'BH_SLURM_NNODES':2}),
#    ('cluster4',  'cluster', 'mpiexec -ppn 1 -np 1 {bridge} : -np 3 ~/.local/bin/bh_vem_cluster_slave',  {'BH_SLURM_NNODES':4}),
#    ('cluster8',  'cluster', 'mpiexec -ppn 1 -np 1 {bridge} : -np 7 ~/.local/bin/bh_vem_cluster_slave',  {'BH_SLURM_NNODES':8}),
#    ('cluster16',  'cluster', 'mpiexec -ppn 2 -np 1 {bridge} : -np 15 ~/.local/bin/bh_vem_cluster_slave',  {'BH_SLURM_NNODES':8}),
    ('cluster32',  'cluster', 'mpiexec -ppn 4 -np 1 {bridge} : -np 31 ~/.local/bin/bh_vem_cluster_slave',  {'BH_SLURM_NNODES':8}),
]

engines = [
    ('cpu1',  'cpu',   {'OMP_NUM_THREADS':1}),
    ('cpu4',  'cpu',   {'OMP_NUM_THREADS':4}),
    ('cpu8',  'cpu',   {'OMP_NUM_THREADS':8}),
]

python_script = [\
#		 ('Heat Equation 10k', 'heat_equation', '--size=10000*10000*10'),
#		 ('Heat Equation 20k', 'heat_equation', '--size=20000*20000*10'),
#		 ('Heat Equation 25k', 'heat_equation', '--size=25000*25000*10'),
		 ('Heat Equation 30k', 'heat_equation', '--size=30000*30000*10'),
#		 ('N-body 15k',        'nbody',        '--size=15000*10'),
		 ('N-body 20k',        'nbody',        '--size=20000*10'),
#		 ('N-body 25k',        'nbody',        '--size=25000*10'),
#                 ('Shallow Water 20k', 'shallow_water','--size=20000*20000*10'),
                 ('Shallow Water 25k', 'shallow_water','--size=25000*25000*10'),
#                 ('Black Scholes 10m', 'black_scholes','--size=10000000*10'),
                 ('Black Scholes 100m','black_scholes','--size=100000000*10')
]

python = {
    'bridges': [python_bohrium],
    'engines': engines,
    'managers': managers,
    'scripts': python_script
}
python_native = {
    'bridges': [python_numpy],
    'scripts': python_script
}

suites = [python_native, python]
#suites = [python]

