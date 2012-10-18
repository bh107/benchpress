#!/usr/bin/env py

engines = [('score_bs%d_bm%d' % (2**i, j), 'score', {"CPHVB_VE_SCORE_BLOCKSIZE": 2**i, "CPHVB_VE_SCORE_BINMAX": j})  for j in xrange(1,20) for i in xrange(2,26)]

for e in engines:
    print e
print len(engines)
