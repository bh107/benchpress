#!/usr/bin/env bash

for CPU in 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15
do
    ./press.py --suite test --runs 1 --affinity $CPU ~/Desktop/cphvb &
done

for cpu in 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15
do
    wait
done
