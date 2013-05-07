managers = [
    ('node',  'node', '',  None),
    ('cluster',  'cluster', 'mpiexec -ppn 1 -np 1 {bridge} : -np 1 taskset -c 1 ./vem/cluster/bh_vem_cluster_slave',  None),
    ('cluster',  'cluster', 'mpiexec -ppn 1 -np 1 {bridge} : -np 3 taskset -c 1 ./vem/cluster/bh_vem_cluster_slave',  None),
    ('cluster',  'cluster', 'mpiexec -ppn 1 -np 1 {bridge} : -np 7 taskset -c 1 ./vem/cluster/bh_vem_cluster_slave',  None),
]

engines = [('simple',  'simple',   None)]

python = {
    'bridges': [('numpy', 'python benchmark/Python/{script}.py {args} --bohrium=True', None)],
    'engines': engines,
    'managers': managers,
    'scripts': [('Shallow Water','shallow_water','--size=500*500*10')]
}

cil = {
    'bridges': [('CIL', 'mono benchmark/CIL/Csharp/{script}/bin/Release/{script}.exe {args}', None)],
    'engines': engines,
    'managers': managers,
    'scripts': [('N-body','nbody','--size=1000*100 --no-temp-arrays=True')]
}

cpp = {
    'bridges': [('CPP', 'benchmark/cpp/bin/{script} {args}', None)],
    'engines': engines,
    'managers': managers,
    'scripts': [('Black Scholes','black_scholes','--size=1000000*10')]
}

suites = [python, cil, cpp]


