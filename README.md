A Benchmark a'day keeps the Professor at bay
--------------------------------------------

These are the most current benchmark results for cphVB generated from Marge.

To compare two builds, download an run this [html](https://bitbucket.org/cphvb/cphvbbuildgraphs/raw/master/compare.html).

![Jacobi fixed Speedup](https://bitbucket.org/cphvb/cphvbbuildgraphs/raw/master/jacobi%20fixed_speedup.png)
![kNN Speedup](https://bitbucket.org/cphvb/cphvbbuildgraphs/raw/master/knn_speedup.png)
![Monte Carlo Speedup](https://bitbucket.org/cphvb/cphvbbuildgraphs/raw/master/monte%20carlo_speedup.png)
![Stencil Speedup](https://bitbucket.org/cphvb/cphvbbuildgraphs/raw/master/stencil%20synth_speedup.png)
![Shallow Water Speedup](https://bitbucket.org/cphvb/cphvbbuildgraphs/raw/master/shallow%20water_speedup.png)

Results
-------

The raw benchmark results are available from https://bitbucket.org/cphvb/benchpress/raw/master/results.

Deploying the Buildbot
----------------------

Log into the machine you want to run benchmarks on. Then do the following::

    cd ~
    mkdir buildbot
    cd buildbot
    git archive --remote=ssh://git@bitbucket.org/cphvb/benchpress.git HEAD: --format=tar build-n-test.sh -o build-n-test.sh.tar
    tar xf build-n-test.sh.tar
    chmod +x build-n-test.sh

Then adjust the "build-n-test.sh" script to match the local environment.
Run it once, inspect the $MACHINE.log file, then add it to a cron-job or something like that.

