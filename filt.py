#!/usr/bin/env python
import re
import os

outputs = ['jacobi', 'mc', 'shallow']

for output in outputs:
    lines = open('/tmp/output_%s.txt' % output).read()

    print "Results for", output, "{"
    bases = {}
    views = {}

    for m in re.finditer('\{((.*,.*\n)+\n)\}.*\[(\d+)\]', lines):
        ops         = m.group(1)
        bin_size    = int(m.group(3))

        for line in (l for l in ops.split("\n")):
            try:
                base, view = line.split(",")
                bases[base] = True
                views[view] = True
            except:
                if bases:
                    print "Binsize %d\t[bases=%d, views=%d]" % ( bin_size, len(bases), len(views) )
                bases = {}
                views = {}
    print "}"
