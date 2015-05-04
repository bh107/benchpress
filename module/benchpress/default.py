##################################################################################
#
#   This is the "old" suite format...
#
# The following things seem quite useless... it should probably just be removed...
# the idea of a "default-suite" is to have of bunch of things that are shared amongst
# a wealth of benchmarks... time has shown us that only something like a "bridge-definition"
# is really ever shared...
#

# Bridges  with various parameter setups
# (alias, cmd (relative to the root of bohrium), env-vars)
bridges = [
    ('numpy', 'python benchmark/python/{script}.py {args}', None),
    ('CIL', 'mono benchmark/CIL/Csharp/{script}/bin/{script}.exe {args} --bohrium=True', None),
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
        'bridges': [('native-numpy', 'python benchmark/python/{script}.py {args}', None)],
        'scripts': scripts
}

suites = [suite, native]

#
#
# End of the old suite format
##################################################################################

##################################################################################
#
# This is the new suite-format. A change is needed since the Bohrium configuration
# things are getting out of hand... something more flexible and simpler is needed.
#
# This will make is possible to specify the Bohrium configuration "stack".
# It is currently only possible swap a child of a component or leave the default.
#
# With this format it will be possible to specify the stack from top to bottom.
# Such as chains of filters, and where in the "stack" filters are used.
#

#
# Definition of launchers used by benchmarks,
#
# In a suite the following are "bridges" and further down in this file
# list called "bridges" exists..
# .. and quite a Bohrium sounding thing... anyway... here are the 
# benchmark "bridges"/"launchers"/"runner"/"commands"/"executers".
# Call them what you like, we called them "bridges" for some reason.
#
# In order to be backwards compatible, the stuff below should probably be defined,
# in the "bridges" list (see further down), however, looking at suites then it is
# quite clear that the bridge-list never used. Probably because indexing is numerical
# and not a dict... Anyway instead instead let us define these...
# matching the file-system conventions.
#

# Python
dython_numpy    = ('Dython/NP', 'dython `bp-info --benchmarks`/{script}/python_numpy/{script}.py {args}', None)
python_numpy    = ('Python/NP', 'python `bp-info --benchmarks`/{script}/python_numpy/{script}.py {args}', None)
python_bohrium  = ('Python/BH', 'python -m bohrium `bp-info --benchmarks`/{script}/python_numpy/{script}.py --bohrium=True {args}', None)

# C
c99_seq     = ('C/SEQ',     '`bp-info --benchmarks`/{script}/c99_seq/bin/{script} {args}', None)
c99_seq_ts  = ('C/SEQ/TS',  'taskset -c 0 `bp-info --benchmarks`/{script}/c99_seq/bin/{script} {args}', None)
c99_omp     = ('C/OMP',     '`bp-info --benchmarks`/{script}/c99_omp/bin/{script} {args}', None)
c99_omp_mpi = ('C/OMP_MPI', 'mpirun `bp-info --benchmarks`/{script}/c99_omp_mpi/bin/{script} {args}', None)

# C++
cpp11_seq   = ('CPP/SEQ',   '`bp-info --benchmarks`/{script}/cpp11_seq/bin/{script} {args}', None)
cpp11_seq_ts= ('CPP/SEQ/TS','taskset -c 0 `bp-info --benchmarks`/{script}/cpp11_seq/bin/{script} {args}', None)
cpp11_omp   = ('CPP/OMP',   '`bp-info --benchmarks`/{script}/cpp11_omp/bin/{script} {args}', None)
cpp11_arma  = ('CPP/Arma',  '`bp-info --benchmarks`/{script}/cpp11_armadillo/bin/{script} {args}', None)
cpp11_blitz = ('CPP/Blitz', '`bp-info --benchmarks`/{script}/cpp11_blitz/bin/{script} {args}', None)
cpp11_eigen = ('CPP/Eigen', '`bp-info --benchmarks`/{script}/cpp11_eigen/bin/{script} {args}', None)
cpp11_boost = ('CPP/Boost', '`bp-info --benchmarks`/{script}/cpp11_boost/bin/{script} {args}', None)
cpp11_bxx   = ('CPP/BH',    '`bp-info --benchmarks`/{script}/cpp11_bxx/bin/{script} {args}', None)

# C#
cil_managed   = ('Mono/Managed', 'mono `bp-info --benchmarks`/{script}/csharp_numcil/bin/{script}.exe --bohrium=False {args}', {'NUMCIL_DISABLE_UNSAFE': '1'})
cil_unsafe    = ('Mono/Unsafe',  'mono `bp-info --benchmarks`/{script}/csharp_numcil/bin/{script}.exe --bohrium=False {args}', {'NUMCIL_DISABLE_UNSAFE': '0'})
cil_bohrium   = ('Mono/Bohrium', 'mono `bp-info --benchmarks`/{script}/csharp_numcil/bin/{script}.exe --bohrium=True  {args}', {'BH_GC_FLUSH': '1'})

# F#

# ... others

#
#   Bohrium stack configurations
#
#   bh_stack_name = [
#        (label, component_name, env_vars),
#        (label, component_name, env_vars),
#        (label, component_name, env_vars),
#        (label, component_name, env_vars),
#        (label, component_name, env_vars),
#   ]
#

#
#   This is "special" stack configuration that facilitates executing benchmarks
#   that has nothing to do with Bohrium.
#
bh_stack_none = [
    [('NA', 'bridge', None)],
    [('NA', 'node', None)],
    [('NA', 'cpu', None)]
]

# End of the new format
##################################################################################

