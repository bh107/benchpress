from default import engines, scripts

block_sizes = [str((2**i-(2**(i-2)/2))) for i in xrange(7,21) ]
base_maxes  = [str(j) for j in xrange(1,10)]

subset = [
    ('score_blksize%s_basemax%s' % (blksize, basemax),
    'score',
    {
        "CPHVB_VE_SCORE_BLOCKSIZE": blksize,
        "CPHVB_VE_SCORE_BINMAX":    str(20),
        "CPHVB_VE_SCORE_BASEMAX":   basemax,
        "CPHVB_CORE_MCACHE_SIZE":   10
    }) for basemax in base_maxes for blksize in block_sizes
]

suite = {
    'scripts': scripts[0:3],
    'engines': engines[0:3] + subset
}

