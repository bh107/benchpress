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

def cache_path(value, out={}):
    envs = ["BH_SINGLETON_CACHE_PATH", "BH_TOPOLOGICAL_CACHE_PATH",\
            "BH_GREEDY_CACHE_PATH", "BH_OPTIMAL_CACHE_PATH", "BH_GENTLE_CACHE_PATH"]
    for env in envs:
        out[env] = value
    return out

homedir = os.path.expanduser('~')
mfe_input = os.path.join(homedir,"benchpress","benchmarks","idl_init_explode","idl_input-float64_512*512.npz")

scripts_gpu = [
    ('X-ray 50^3 020^2',  'xraysim',    '--size=50*20*10'),
    ('X-ray 50^3 040^2',  'xraysim',    '--size=50*40*10'),
    ('X-ray 50^3 080^2',  'xraysim',    '--size=50*80*10'),
    ('X-ray 50^3 160^2',  'xraysim',    '--size=50*160*10'),
    ('X-ray 50^3 320^2',  'xraysim',    '--size=50*320*10'),
    ('X-ray 50^3 640^2',  'xraysim',    '--size=50*640*10'),
]
scripts_gpu_no_xsweep = [
    ('MC Pi 0.1G',       'montecarlo_pi',    '--size=100000000*3'),
    ('MFE 032^2',        'idl_init_explode', '--size=32*32*5 --inputfn=%s'%mfe_input),

    ('MC Pi 0003.2G',    'montecarlo_pi',    '--size=3200000000*3'),
    ('MC Pi 0102.4G',    'montecarlo_pi',    '--size=102400000000*3'),
    ('MC Pi 3276.8G',    'montecarlo_pi',    '--size=3276800000000*3'),

    ('MFE 064^2',        'idl_init_explode', '--size=64*64*5   --inputfn=%s'%mfe_input),
    ('MFE 128^2',        'idl_init_explode', '--size=128*128*5 --inputfn=%s'%mfe_input),
    ('MFE 256^2',        'idl_init_explode', '--size=256*256*5 --inputfn=%s'%mfe_input),
]

stack_gpu = [
    [('default',    'bridge',    None)],
    [('bcexp_gpu',  'bcexp_gpu', None)],
    [('dimclean',   'dimclean',  None)],
    [('Greedy',     'greedy',    None)],
    [('memcache',   'node', cache_path("", fuse_cache("true")))],
    [('gpu',        'gpu',       {"BH_GPU_KERNEL"  : "both",
                                  "CUDA_CACHE_DISABLE"  : "1",
                                  "BH_GPU_COMPILE" : "sync"})],
    [('cpu',        'cpu',       {"BH_CPU_JIT_LEVEL": "3", "OMP_NUM_THREADS":4})],
]

stack_gpu_no_xsweep = [
    [('default',    'bridge',    None)],
    [('bcexp_gpu',  'bcexp_gpu', None)],
    [('dimclean',   'dimclean',  None)],
    [('Greedy',     'greedy',    None)],
    [('memcache',   'node',      None)],
    [('gpu',        'gpu',       {"BH_FUSE_MODEL"  : "NO_XSWEEP_SCALAR_SEPERATE",
                                  "BH_GPU_KERNEL"  : "both",
                                  "CUDA_CACHE_DISABLE"  : "1",
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

