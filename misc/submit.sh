#!/usr/bin/env bash
./press.py --suite $1 --output /tmp/ --runs 4 --no-perf --slurm --no-time ~/buildbot/bohrium
