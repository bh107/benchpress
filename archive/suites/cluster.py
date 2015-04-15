def get_setup(nnode, nproc, nthread):
    return ('clusterN%dP%02dT%02d'%(nnode,nproc,nthread), 'cluster',
            'mpiexec -ppn %d -np 1 {bridge} : -np %d ./vem/cluster/bh_vem_cluster_slave'%(nproc,nnode*nproc-1),
           {'BH_SLURM_NNODES':nnode, 'OMP_NUM_THREADS':nthread})

def cluster_bynode(node_max=8, proc_max=4, thd_max=8):
    ret = []
    i = 1
    while i <= node_max * proc_max * thd_max:
        nnode = min(i,node_max)
        nproc = min(max(i/node_max,1),proc_max)
        nthd  = max(i/(node_max*proc_max),1)
        ret.append(get_setup(nnode, nproc, nthd))
        i *= 2
    return ret

def cluster_bythread(node_max=8, proc_max=4, thd_max=8):
    ret = []
    i = 1
    while i <= node_max * proc_max * thd_max:
        nnode = max(i/(proc_max*thd_max),1)
        nproc = min(max(i/thd_max,1),proc_max)
        nthd  = min(i,thd_max)
        ret.append(get_setup(nnode, nproc, nthd))
        i *= 2
    return ret

def remove_duplicates(managers):
    s = set()
    ret = []
    for m in managers:
        if m[0] not in s:
            ret.append(m)
            s.add(m[0])
    return ret


managers = cluster_bynode(8,4,8) + cluster_bythread(8,4,8)
managers += cluster_bynode(8,1,32) + cluster_bythread(8,1,32)
managers += cluster_bynode(8,32,1) + cluster_bythread(8,32,1)
managers = remove_duplicates(managers)

engines = [('dynamite',  'dynamite',   None)]

python_script = [('N-body 15k*10', 'nbody', '--size=15000*10')]

python = {
    'bridges': [('numpy', 'python benchmark/python/{script}.py {args} --bohrium=True', None)],
    'engines':  engines,
    'managers': managers,
    'scripts':  python_script
}

suites = [python]
