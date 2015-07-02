#!/usr/bin/env bash
SIZE=20000000*3
python synth_pow.py --size=$SIZE
BH_CPU_JIT_LEVEL=1 BH_BCEXP_CPU_POWK=0 python -m bohrium synth_pow.py --size=$SIZE
BH_CPU_JIT_LEVEL=1 BH_BCEXP_CPU_POWK=1 python -m bohrium synth_pow.py --size=$SIZE
BH_CPU_JIT_LEVEL=3 BH_BCEXP_CPU_POWK=0 python -m bohrium synth_pow.py --size=$SIZE
BH_CPU_JIT_LEVEL=3 BH_BCEXP_CPU_POWK=1 python -m bohrium synth_pow.py --size=$SIZE
