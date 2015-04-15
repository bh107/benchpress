#!/usr/bin/env python
import glob
import os

for root, dirs, filenames in os.walk("benchmarks"):
    path = root.split("/")
    if len(filenames) == 1 and \
        filenames[0] == "empty" and \
        path[-1] == "src" and \
        ("cpp11" in root or "c99" in root):

        print "git rm -r %s" % os.sep.join(path[:-1])
