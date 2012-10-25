from default import scripts, engines

block_sizes = [str((2**i-(2**(i-2)/2))) for i in xrange(7,21) ]
base_maxes  = [str(j) for j in xrange(1,10)]

score_engines = [('score_blks%d_binm%d' % ((2**i-(2**(i-2)/2)), j), 'score', {"CPHVB_VE_SCORE_BLOCKSIZE": str((2**i-(2**(i-2)/2))), "CPHVB_VE_SCORE_BINMAX": str(j)})  for j in xrange(2,24) for i in xrange(7,21)]

suite = {
    'scripts':  [script for script in scripts if 'Shallow' in script[0]],
    'engines':  engines[0:3] + score_engines
}

