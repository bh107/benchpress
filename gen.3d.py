#!/usr/bin/env python
from collections import OrderedDict
import pprint
import json

from mpl_toolkits.mplot3d import Axes3D
import matplotlib
#matplotlib.use('GTKAgg')
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from pylab import clf, title, savefig, show

import math
import matplotlib.ticker as ticker

def avg( times ):
    return sum(times)/len(times)

def main():

    set01 = [
        'results/akira/benchmark-RP29oC.json',
        'results/akira/benchmark-av1GUr.json',
        'results/akira/benchmark-UWf6Gx.json'
    ] 
    set02 = ['results/akira/benchmark-TmMOCJ.json']

    results = {}
    for fn in set02:
        with open(fn) as fd:
            for bm, alias, eng, param, cmd, times in json.load(fd)["runs"]:
                run = (bm, alias, eng, param, cmd, times)
                if bm not in results:
                    results[bm] = [ run ]
                else:
                    results[bm].append( run )

    for name in results:

        runs = results[name]

        clf()
        fig = plt.figure()
        ax  = fig.add_subplot(111, projection='3d')

        score   = (r for r in runs if r[2] == "score")
        score_t = ((bm, alias, avg(times),  p["CPHVB_VE_SCORE_BLOCKSIZE"], p["CPHVB_VE_SCORE_BINMAX"]) for (bm, alias, _, p, _, times) in score)
        score_r = [(bm, alias, avg_time, int(blocksize), int(binmax) ) for (bm, alias, avg_time, blocksize, binmax) in score_t]

        scatter = [(bs, bm, at) for _,_, at, bs, bm in score_r]
        
        # Ranking the results
        rank_elapsed    = sorted(score_r, key= lambda a: [a[2]])        # By elapsed time
        rank_bins       = sorted(score_r, key= lambda a: [a[4], a[3]])  # By BINMAX
        rank_blocks     = sorted(score_r, key= lambda a: [a[3], a[4]])  # By BLOCKSIZE

        bin_sizes   = list(OrderedDict.fromkeys([i[4] for i in rank_bins]))
        blk_sizes   = list(OrderedDict.fromkeys([i[3] for i in rank_blocks]))

        bin_len = len(bin_sizes)
        blk_len = len(blk_sizes)

        best = []
        for i in xrange(0,3):
            _,_,best_time, best_blk_size, best_binmax = rank_elapsed[i]
            best_blk_size = [c for c,x in enumerate(blk_sizes) if x == best_blk_size][0]
            best.append( [best_blk_size, best_binmax, best_time] )

        x = []
        s = rank_bins[0][4]
        l = []
        for _,_, at, lock_size, bin_size in rank_bins:
            
            if s != bin_size:
                x.append(l)
                l = [at]
            else:
                l.append( at )
            
            s = bin_size
        x.append(l)

        z = np.array( x )

        x = np.arange(0, blk_len)
        y = bin_sizes
        X, Y = np.meshgrid(x,y)
        ax.set_xlabel('Blocksize')
        ax.set_ylabel('Binsize')
        ax.set_zlabel('Runtime')
        title(name)

        ax.scatter(*best[0], color='red',   s=50)
        ax.scatter(*best[1], color='green', s=50)
        ax.scatter(*best[2], color='blue',  s=50)
        ax.plot_wireframe(X,Y,z, rstride=1, cstride=1)
        ax.legend()

        labels = ax.get_xticklabels()
        ax.set_xticklabels([blk_sizes[i] for i in xrange(0, blk_len-1, int((blk_len-1)/4))])
        show()

        fn = "/tmp/%s" % name
        savefig("%s.pdf" % ( fn ))
        savefig("%s.eps" % ( fn ))
        savefig("%s.png" % ( fn ))

if __name__ == "__main__":
    main()
