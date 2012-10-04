A Benchmark a day keeps the Professor at bay
============================================

The speedup graphs below represent the latest results (raw form available [here](https://bitbucket.org/cphvb/benchpress/raw/master/results/akira/benchmark-latest.json)) of running benchmarks on akira.

All benchmark results are stored in json-format and are available [here](https://bitbucket.org/cphvb/benchpress/raw/master/results).

To compare benchmark-results from different machines and revisions, download an run this [html](https://bitbucket.org/cphvb/benchpress/raw/master/compare.html).

![Jacobi Fixed   ](https://bitbucket.org/cphvb/benchpress/raw/master/graphs/akira/latest/jacobi%20fixed_speedup.png)
![1D 4way-Stencil](https://bitbucket.org/cphvb/benchpress/raw/master/graphs/akira/latest/1d%204way%20stencil_speedup.png)
![kNN            ](https://bitbucket.org/cphvb/benchpress/raw/master/graphs/akira/latest/knn_speedup.png)
![Monte Carlo    ](https://bitbucket.org/cphvb/benchpress/raw/master/graphs/akira/latest/monte%20carlo_speedup.png)
![Stencil        ](https://bitbucket.org/cphvb/benchpress/raw/master/graphs/akira/latest/stencil%20synth_speedup.png)
![Shallow Water  ](https://bitbucket.org/cphvb/benchpress/raw/master/graphs/akira/latest/shallow%20water_speedup.png)


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

Auth to repos
-------------

If you do not already have it set up then you need to set up a ssh-agent with keys to the benchpress repos.
U could a script similar to::

    agent_pid="$(ps -ef | grep "ssh-agent" | grep -v "grep" | awk '{print($2)}')"
    if [[ -z "$agent_pid" ]]
    then
        eval "$(ssh-agent)"
        ssh-add
    else
        #agent_ppid="$(ps -ef | grep "ssh-agent" | grep -v "grep" | awk '{print($3)}')"
        agent_ppid="$(($agent_pid - 1))"
     
        agent_sock="$(find /tmp -path "*ssh*" -type s -iname "agent.$agent_ppid")"
     
        echo "Agent pid $agent_pid"
        export SSH_AGENT_PID="$agent_pid"
        export SSH_AUTH_SOCK="$agent_sock"
    fi

