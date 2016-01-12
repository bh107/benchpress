from benchpress.default import *
import copy
import os

def fuse_cache(value):
    envs = ["BH_SINGLETON_FUSE_CACHE", "BH_TOPOLOGICAL_FUSE_CACHE",\
            "BH_GREEDY_FUSE_CACHE", "BH_OPTIMAL_FUSE_CACHE", "BH_GENTLE_FUSE_CACHE"]
    ret = {}
    for env in envs:
        ret[env] = value
    return ret

homedir = os.path.expanduser('~')
mfe_input = os.path.join(homedir,"benchpress","benchmarks","idl_init_explode","idl_input-float64_512*512.npz")

scripts_gpu = [
    ('X-ray 50^3 20^2',  'xraysim',          '--size=50*20*1'),
    ('X-ray 50^3 40^2',  'xraysim',          '--size=50*40*1'),
    ('X-ray 50^3 80^2',  'xraysim',          '--size=50*80*1'),
    ('X-ray 50^3 160^2',  'xraysim',          '--size=50*160*1'),
]
scripts_gpu_no_xsweep = [
    ('MC Pi 10^6',       'montecarlo_pi',    '--size=1000000*1'),
    ('MFE 32^2',         'idl_init_explode', '--size=32*32 --inputfn=%s'%mfe_input),

    ('MC Pi 40^6',       'montecarlo_pi',    '--size=4000000*1'),
    ('MC Pi 80^6',       'montecarlo_pi',    '--size=8000000*1'),
    ('MC Pi 120^6',      'montecarlo_pi',    '--size=12000000*1'),

    ('MFE 64^2',         'idl_init_explode', '--size=64*64   --inputfn=%s'%mfe_input),
    ('MFE 128^2',        'idl_init_explode', '--size=128*128 --inputfn=%s'%mfe_input),
    ('MFE 256^2',        'idl_init_explode', '--size=256*256 --inputfn=%s'%mfe_input),
]

stack_gpu = [
    [('default',    'bridge',    None)],
    [('bcexp_gpu',  'bcexp_gpu', None)],
    [('dimclean',   'dimclean',  None)],
    [('Greedy',     'greedy',    None)],
    [('filecache',  'node',      fuse_cache("true"))],
    [('gpu',        'gpu',       {"BH_GPU_KERNEL"  : "both",
                                  "BH_GPU_COMPILE" : "sync"})],
    [('cpu',        'cpu',       {"BH_CPU_JIT_LEVEL": "3", "OMP_NUM_THREADS":4})],
]

stack_gpu_no_xsweep = [
    [('default',    'bridge',    None)],
    [('bcexp_gpu',  'bcexp_gpu', None)],
    [('dimclean',   'dimclean',  None)],
    [('Greedy',     'greedy',    None)],
    [('filecache',  'node',      fuse_cache("true"))],
    [('gpu',        'gpu',       {"BH_FUSE_MODEL"  : "NO_XSWEEP_SCALAR_SEPERATE",
                                  "BH_GPU_KERNEL"  : "both",
                                  "BH_GPU_COMPILE" : "sync"})],
    [('cpu',        'cpu',       {"BH_CPU_JIT_LEVEL": "3", "OMP_NUM_THREADS":4})],
]

suite_gpu = {
    'scripts': scripts_gpu,
    'launchers':  [python_bohrium],
    'bohrium': stack_gpu
}

suite_gpu_no_xsweep = {
    'scripts': scripts_gpu_no_xsweep,
    'launchers':  [python_bohrium],
    'bohrium': stack_gpu_no_xsweep
}

suite_numpy = {
    'scripts': scripts_gpu[:1] + scripts_gpu_no_xsweep[:2],
    'launchers': [python_numpy],
    'bohrium':  bh_stack_none
}

suites = [
    suite_gpu, suite_gpu_no_xsweep, suite_numpy
]

