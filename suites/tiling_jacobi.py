from default import scripts, engines

block_sizes = [str((2**i-(2**(i-2)/2))) for i in xrange(7,21) ]
base_maxes  = [str(j) for j in xrange(1,10)]

subset = [
    ('score_blksize%s' % (blksize),
    'score',
    {
        "CPHVB_VE_SCORE_BLOCKSIZE": str(blksize),
        "CPHVB_VE_SCORE_BINMAX":    str(20),
        "CPHVB_VE_SCORE_BASEMAX":   str(5),
        "CPHVB_CORE_MCACHE_SIZE":   str(10)
    }) for blksize in block_sizes
]

suite = {
    'scripts': [script for script in scripts if 'Jacobi Iterative - Reduce' in script[0]],
    'engines': [engines[0:2]] + subset
}
