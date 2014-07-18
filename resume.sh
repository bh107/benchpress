#!/usr/bin/env bash
./press.py --suite cpu --output /tmp/ --runs 1 --no-perf --slurm --no-time ~/buildbot/bohrium/ --resume $1
python times.py $1
