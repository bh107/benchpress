#!/usr/bin/env python
import json
import os
import couchdb

couch   = couchdb.Server()
db      = couch['benchpress']


for root, dirs, files in os.walk('results'):
    for fn in (fn for fn in files if 'json' in fn):
        base = os.path.splitext(fn)[0]
        path = "%s/%s" % (root, fn)

        hostname = root.split('/')[1]
        
        results = json.load(open(path))
        results['meta']['hostname'] = hostname
        db.save( results )

