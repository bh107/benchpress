# Bridges  with various parameter setups
# (alias, cmd (relative to the root of bohrium), env-vars)
bridges = [
    ('numpy', 'python benchmark/python/{script}.py {args} --bohrium=True', None),
    ('CIL', 'mono benchmark/CIL/Csharp/{script}/bin/Release/{script}.exe {args}', None),
    ('cpp', 'benchmark/cpp/bin/{script} {args}', None)
]


# Managers above the node-vem with various parameter setups.
# NB: the node-vem is hardcoded, the managers here will have the
#     node-vem as child unless it is the node-vem itself
# (alias, manager, cmd (relative to the root of bohrium), env-vars)
managers = [
    ('node',  'node', '',  None),
    ('cluster',  'cluster', 'mpiexec -ppn 1 -np 1 {bridge} : -np 1 taskset -c 0 ./vem/cluster/bh_vem_cluster_slave',  None),
]

# Engines with various parameter setups
# (alias, engine, env-vars)
engines = [
    ('cpu',   'cpu',    None),
    ('gpu',   'gpu',    None),
]

# Scripts and their arguments
# (alias, script, arguments)
scripts   = [
    ('Black Scholes',        'black_scholes',  '--size=100000*10'),
    ('Monte Carlo PI',       'mc',             '--size=100000*100'),
    ('Jacobi Stencil',       'jacobi_stencil', '--size=1000*1000*10'),
    ('Shallow Water',        'shallow_water',  '--size=500*500*10'),
    ('Lattice Boltzmann 2D', 'lattice_boltzmann_D2Q9', '--size=100*1000*10'),
]

# A suite example
# Note that 'engines' and 'managers' may be undefined, in which case they are ignored
suite = {
    'bridges':   bridges,
    'engines':   engines,
    'managers':  managers,
    'scripts':   scripts,
}


native = {
        'bridges': [('native-numpy', 'python benchmark/python/{script}.py {args} --bohrium=False', None)],
        'scripts': scripts
}

suites = [suite, native]

