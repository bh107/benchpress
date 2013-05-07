managers = [
    ('node',  'node', '',  None),
    ('cluster1',  'cluster', 'mpiexec -ppn 1 -np 1 {bridge} : -np 0 taskset -c 1 ./vem/cluster/bh_vem_cluster_slave',  {'BH_SLURM_NNODES':1}),
    ('cluster2',  'cluster', 'mpiexec -ppn 1 -np 1 {bridge} : -np 1 taskset -c 1 ./vem/cluster/bh_vem_cluster_slave',  {'BH_SLURM_NNODES':2}),
    ('cluster4',  'cluster', 'mpiexec -ppn 1 -np 1 {bridge} : -np 3 taskset -c 1 ./vem/cluster/bh_vem_cluster_slave',  {'BH_SLURM_NNODES':4}),
    ('cluster8',  'cluster', 'mpiexec -ppn 1 -np 1 {bridge} : -np 7 taskset -c 1 ./vem/cluster/bh_vem_cluster_slave',  {'BH_SLURM_NNODES':8}),
]

engines = [('simple',  'simple',   None)]

python_script = [('Shallow Water','shallow_water','--size=10000*10000*10')]
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

cil_script = [('N-body','nbody','--size=5000*10 --no-temp-arrays=True')]
cil = {
    'bridges': [('CIL', 'mono benchmark/CIL/Csharp/{script}/bin/Release/{script}.exe {args}', None)],
    'engines': engines,
    'managers': managers,
    'scripts': cil_script
}
cil_native = {
    'bridges': [('CIL-native', 'mono benchmark/CIL/Csharp/{script}/bin/Release/{script}.exe {args}', None)],
    'scripts': cil_script
}

cpp_script = [('Black Scholes','black_scholes','--size=10000000*10')]
cpp = {
    'bridges': [('CPP', 'benchmark/cpp/bin/{script} {args}', None)],
    'engines': engines,
    'managers': managers,
    'scripts': cpp_script
}
cpp_native = {
    'bridges': [('CPP-native', 'benchmark/cpp/bin/{script} {args}', None)],
    'scripts': cpp_script
}

suites = [python_native, python, cil, cpp]


