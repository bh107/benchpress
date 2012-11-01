from vcache_all import vcache_engines
from default import scripts, engines

suite = {
    'scripts':  [script for script in scripts if 'Shallow' in script[0]],
    'engines':  engines[0:3] + vcache_engines
}
