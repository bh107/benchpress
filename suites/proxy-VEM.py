managers = [\
           ('proxy', 'proxy', '{bridge}', None),
]

engines = [\
           ('sleep    0ms', 'cpu',  {'BH_VEM_PROXY_SLEEP':0}),
           ('sleep   10ms', 'cpu',  {'BH_VEM_PROXY_SLEEP':10}),
           ('sleep  100ms', 'cpu',  {'BH_VEM_PROXY_SLEEP':100}),
           ('sleep  200ms', 'cpu',  {'BH_VEM_PROXY_SLEEP':200}),
           ('sleep  500ms', 'cpu',  {'BH_VEM_PROXY_SLEEP':500}),
           ('sleep 1000ms', 'cpu',  {'BH_VEM_PROXY_SLEEP':1000}),
]

python_script = [\
    		 ('N-body  5k',        'nbody',          '--size=5000*10'),
    		 ('N-body 10k',        'nbody',          '--size=10000*10'),
    		 ('N-body 15k',        'nbody',          '--size=15000*10'),
    		 ('N-body 20k',        'nbody',          '--size=20000*10'),
    		 ('N-body 25k',        'nbody',          '--size=25000*10'),
    		 ('Heat Equation  5k', 'heat_equation',  '--size=5000*5000*10'),
    		 ('Heat Equation 10k', 'heat_equation',  '--size=10000*10000*10'),
    		 ('Heat Equation 20k', 'heat_equation',  '--size=20000*20000*10'),
    		 ('Heat Equation 25k', 'heat_equation',  '--size=25000*25000*10'),
    		 ('Heat Equation 30k', 'heat_equation',  '--size=30000*30000*10'),
                 ('Shallow Water  5k', 'shallow_water',  '--size=5000*5000*10'),
                 ('Shallow Water 10k', 'shallow_water',  '--size=10000*10000*10'),
                 ('Shallow Water 20k', 'shallow_water',  '--size=20000*20000*10'),
                 ('Shallow Water 25k', 'shallow_water',  '--size=25000*25000*10'),
                 ('Shallow Water 30k', 'shallow_water',  '--size=30000*30000*10'),
                 ('Black Scholes   1m', 'black_scholes',  '--size=1000000*10'),
                 ('Black Scholes  10m', 'black_scholes',  '--size=10000000*10'),
                 ('Black Scholes 100m', 'black_scholes',  '--size=100000000*10'),
]

python_script = [\
    		 ('N-body  5k',        'nbody',          '--size=5000*10'),
    		 ('Heat Equation  5k', 'heat_equation',  '--size=5000*5000*10'),
                 ('Black Scholes   1m', 'black_scholes',  '--size=1000000*10'),
]

python = {
    'bridges': [('numpy', 'python benchmark/python/{script}.py {args} --bohrium=True', None)],
    'managers': managers,
    'engines': engines,
    'scripts': python_script,
    'pre-hook': 'sbatch -p octuplets --nodes 8 hooks/proxy-VEM-pre-hook.sh'
}

python_no_proxy = {
    'bridges':  [('numpy', 'python benchmark/python/{script}.py {args} --bohrium=True', None)],
    'managers': [('cluster',  'cluster', 'mpiexec -ppn 4 -np 1 {bridge} : -np 31 ./vem/cluster/bh_vem_cluster_slave',  {'BH_SLURM_NNODES':8,'OMP_NUM_THREADS':8})],
    'engines':  [('cpu', 'cpu', None)],
    'scripts':  python_script,
    'use_slurm_default': True,
}

python_viz = {
    'bridges': [('numpy', 'python benchmark/python/{script}.py {args} --bohrium=True', None)],
    'managers':[('proxyViz', 'proxy', '{bridge} --visualize', None)],
    'engines': engines,
    'scripts': python_script,
    'pre-hook': 'sbatch -p octuplets --nodes 8 hooks/proxy-VEM-pre-hook.sh'
}
python_viz_no_proxy = {
    'bridges':  [('numpy', 'python benchmark/python/{script}.py {args} --bohrium=True', None)],
    'managers': [('clusterViz',  'cluster', 'mpiexec -ppn 4 -np 1 {bridge} --visualize : -np 31 ./vem/cluster/bh_vem_cluster_slave',  {'BH_SLURM_NNODES':8,'OMP_NUM_THREADS':8})],
    'engines':  [('cpu', 'cpu', None)],
    'scripts':  python_script,
    'use_slurm_default': True,
}

suites = [python,python_no_proxy]
#suites = [python_viz,python_viz_no_proxy]



