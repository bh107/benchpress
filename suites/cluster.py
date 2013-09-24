def get_setup(nnode, nproc, nthread, bynode=True):
    bynode = "-bynode" if bynode else ""
    return ('clusterN%dP%02dT%02d'%(nnode,nproc,nthread), 'cluster',
            'mpiexec -npernode %d -np 1 {bridge} : -np %d ./vem/cluster/bh_vem_cluster_slave'%(nproc,nnode*nproc-1),
           {'BH_SLURM_NNODES':nnode, 'OMP_NUM_THREADS':nthread})

def cluster_bynode(node_max=8, proc_max=8, thd_max=32):
    ret = []
    i = 1
    while i <= node_max * proc_max * thd_max:
        nnode = min(i,node_max)
        nproc = min(max(i/node_max,1),node_max)
        nthd  = max(i/(node_max*proc_max),1)
        ret.append(get_setup(nnode, nproc, nthd, True))
        i *= 2
    return ret

def cluster_bythread(node_max=8, proc_max=8, thd_max=32):
    ret = []
    i = 1
    while i <= node_max * proc_max * thd_max:
        nnode = max(i/(proc_max*thd_max),1)
        nproc = min(max(i/thd_max,1),thd_max)
        nthd  = min(i,thd_max)
        ret.append(get_setup(nnode, nproc, nthd, False))
        i *= 2
    return ret

#cluster_bynode()
#cluster_bythread()


managers = cluster_bynode() + cluster_bythread()

engines = [('cpu',  'cpu',   None)]

python_script = [('N-body 150*10', 'nbody', '--size=150*10')]

python = {
    'bridges': [('numpy', 'python benchmark/Python/{script}.py {args} --bohrium=True', None)],
    'engines':  engines,
    'managers': managers,
    'scripts':  python_script
}

suites = [python]
