A Benchmark a day keeps the Professor at bay
============================================

Below are speedup graphs of the most current benchmark results available. All benchmark results are available in json-format from [here](https://bitbucket.org/cphvb/benchpress/raw/master/results).

To compare different benchmark-results, download an run this [html](https://bitbucket.org/cphvb/cphvbbuildgraphs/raw/master/compare.html).

Akira
-----

![Jacobi Fixed  ](https://bitbucket.org/cphvb/benchpress/raw/master/graphs/akira/latest/jacobi%20fixed_speedup.png)
![kNN           ](https://bitbucket.org/cphvb/benchpress/raw/master/graphs/akira/latest/knn_speedup.png)
![Monte Carlo   ](https://bitbucket.org/cphvb/benchpress/raw/master/graphs/akira/latest/monte$20carlo_speedup.png)
![Stencil       ](https://bitbucket.org/cphvb/benchpress/raw/master/graphs/akira/latest/stencil%20synth_speedup.png)
![Shallow Water ](https://bitbucket.org/cphvb/benchpress/raw/master/graphs/akira/latest/shallow%20water_speedup.png)

Marge
-----

![Jacobi Fixed  ](https://bitbucket.org/cphvb/benchpress/raw/master/graphs/marge/latest/jacobi%20fixed_speedup.png)
![kNN           ](https://bitbucket.org/cphvb/benchpress/raw/master/graphs/marge/latest/knn_speedup.png)
![Monte Carlo   ](https://bitbucket.org/cphvb/benchpress/raw/master/graphs/marge/latest/monte$20carlo_speedup.png)
![Stencil       ](https://bitbucket.org/cphvb/benchpress/raw/master/graphs/marge/latest/stencil%20synth_speedup.png)
![Shallow Water ](https://bitbucket.org/cphvb/benchpress/raw/master/graphs/marge/latest/shallow%20water_speedup.png)


P31sd
-----

![Jacobi Fixed  ](https://bitbucket.org/cphvb/benchpress/raw/master/graphs/p31sd/latest/jacobi%20fixed_speedup.png)
![kNN           ](https://bitbucket.org/cphvb/benchpress/raw/master/graphs/p31sd/latest/knn_speedup.png)
![Monte Carlo   ](https://bitbucket.org/cphvb/benchpress/raw/master/graphs/p31sd/latest/monte$20carlo_speedup.png)
![Stencil       ](https://bitbucket.org/cphvb/benchpress/raw/master/graphs/p31sd/latest/stencil%20synth_speedup.png)
![Shallow Water ](https://bitbucket.org/cphvb/benchpress/raw/master/graphs/p31sd/latest/shallow%20water_speedup.png)

Deploying the Buildbot
======================

Log into the machine you want to run benchmarks on. Then do the following::

    cd ~
    mkdir buildbot
    cd buildbot
    git archive --remote=ssh://git@bitbucket.org/cphvb/benchpress.git HEAD: --format=tar build-n-test.sh -o build-n-test.sh.tar
    tar xf build-n-test.sh.tar
    chmod +x build-n-test.sh

Then adjust the "build-n-test.sh" script to match the local environment.
Run it once, inspect the $MACHINE.log file, then add it to a cron-job or something like that.

