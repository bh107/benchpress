#!/bin/bash
sleep 1
export LD_LIBRARY_PATH=~/.local
export OMP_NUM_THREADS=4
echo mpiexec -ppn 4 -np 1 ~/.local/bh_proxy_client -a 10.10.0.100 -p 4200 : -np 31 ~/.local/bh_vem_cluster_slave
mpiexec -ppn 4 -np 1 ~/.local/bh_proxy_client -a 10.10.0.100 -p 4200 : -np 7 ~/.local/bh_vem_cluster_slave
