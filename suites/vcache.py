from default import *

scholes = [
#    ('Black Scholes',        'black_scholes',   '--size=250000*5'),
#    ('Black Scholes',        'black_scholes',   '--size=500000*5'),
#    ('Black Scholes',        'black_scholes',   '--size=1000000*5'),
#    ('Black Scholes',        'black_scholes',   '--size=2000000*5'),
#    ('Black Scholes',        'black_scholes',   '--size=4000000*5'),
    ('Black Scholes',        'black_scholes',   '--size=8000000*5'),
]

jacobi = [
#    ('Jacobi Stencil',       'jacobi_stencil', '--size=313*4000*10'),
#    ('Jacobi Stencil',       'jacobi_stencil', '--size=625*4000*10'),
#    ('Jacobi Stencil',       'jacobi_stencil', '--size=1250*4000*10'),
#    ('Jacobi Stencil',       'jacobi_stencil', '--size=2500*4000*10'),
#    ('Jacobi Stencil',       'jacobi_stencil', '--size=5000*4000*10'),
    ('Jacobi Stencil',       'jacobi_stencil', '--size=10000*4000*10'),
]

knn = [
#    ('KNN', 'knn', '--size=62500*10*3'),
#    ('KNN', 'knn', '--size=125000*10*3'),
#    ('KNN', 'knn', '--size=250000*10*3'),
#    ('KNN', 'knn', '--size=500000*10*3'),
#    ('KNN', 'knn', '--size=1000000*10*3'),
    ('KNN', 'knn', '--size=2000000*10*3'),
]

mc = [
#    ('Monte Carlo PI', 'mc', '--size=625000*10'),
#    ('Monte Carlo PI', 'mc', '--size=1250000*10'),
#    ('Monte Carlo PI', 'mc', '--size=2500000*10'),
#    ('Monte Carlo PI', 'mc', '--size=5000000*10'),
#    ('Monte Carlo PI', 'mc', '--size=10000000*10'),
    ('Monte Carlo PI', 'mc', '--size=20000000*10'),
]

nbody = [
#    ('NBody', 'nbody', '--size=125*10'),
#    ('NBody', 'nbody', '--size=250*10'),
#    ('NBody', 'nbody', '--size=500*10'),
#    ('NBody', 'nbody', '--size=1000*10'),
#    ('NBody', 'nbody', '--size=2000*10'),
    ('NBody', 'nbody', '--size=4000*10')
]

shallow = [
#    ('Shallow Water',        'shallow_water',   '--size=94*94*5'),
#    ('Shallow Water',        'shallow_water',   '--size=188*188*5'),
#    ('Shallow Water',        'shallow_water',   '--size=375*375*5'),
#    ('Shallow Water',        'shallow_water',   '--size=750*750*5'),
#    ('Shallow Water',        'shallow_water',   '--size=1500*1500*5'),
    ('Shallow Water',        'shallow_water',   '--size=3000*3000*5'),
]

swaption = [
#    ('Swaption', 'LMM_swaption_vec', '--size=1250'),
#    ('Swaption', 'LMM_swaption_vec', '--size=2500'),
#    ('Swaption', 'LMM_swaption_vec', '--size=5000'),
#    ('Swaption', 'LMM_swaption_vec', '--size=10000'),
#    ('Swaption', 'LMM_swaption_vec', '--size=20000'),
    ('Swaption', 'LMM_swaption_vec', '--size=1000'),
]

bolz = [
#    ('Bolzmann D2Q9', 'lattice_boltzmann_D2Q9', '--size=94*94*5'),
#    ('Bolzmann D2Q9', 'lattice_boltzmann_D2Q9', '--size=188*188*5'),
#    ('Bolzmann D2Q9', 'lattice_boltzmann_D2Q9', '--size=375*375*5'),
#    ('Bolzmann D2Q9', 'lattice_boltzmann_D2Q9', '--size=750*750*5'),
#    ('Bolzmann D2Q9', 'lattice_boltzmann_D2Q9', '--size=1500*1500*5'),
    ('Bolzmann D2Q9', 'lattice_boltzmann_D2Q9', '--size=800*800*5'),
]

bolz3d = [
    ('Bolzmann 3D', 'lbm.3d', '--size=120*100*100*5'),
]

mxmul = [
    ('Matrix Mul', 'mxmul', '--size=800')        
]

sor = [
    ('SOR', 'sor', '--size=4000*4000*5')
]

wworld = [
    ('Wire World', 'wireworldnumpy', '--size=5000*5000*5')
]


fft = [
    ('FFT', 'fftex', '--size=18')
]

lu = [
    ('LU Factor.', 'lu', '--size=10000*10')
]

cloth = [
    ('Cloth.', 'cloth', '--size=3000*3000*1')
]

scripts = scholes + jacobi + knn + mc + nbody + shallow + swaption + bolz + bolz3d + mxmul + sor + wworld + lu +fft + cloth

numpy = {
    'bridges':  [
        ('NumPy/Native', 'python benchmark/Python/{script}.py {args}',
            {'VCACHE_LINES': "0", 'VCACHE_BYTES': "0"}),
        ('NumPy/VCache_100M', 'python benchmark/Python/{script}.py {args}',
            {'VCACHE_LINES': "10",'VCACHE_BYTES': "104857600"} ),
        ('NumPy/VCache_512M', 'python benchmark/Python/{script}.py {args}',
            {'VCACHE_LINES': "10",'VCACHE_BYTES': "536870912"} ),
        ('NumPy/VCache_1G', 'python benchmark/Python/{script}.py {args}',
            {'VCACHE_LINES': "10",'VCACHE_BYTES': "1048576000"} ),
#        ('NumPy/VCache_2G', 'python benchmark/Python/{script}.py {args}',
#            {'VCACHE_LINES': "20",'VCACHE_BYTES': "2147483648"} ),

    ],
    'scripts':  scripts,
}

suites = [
    numpy
]

