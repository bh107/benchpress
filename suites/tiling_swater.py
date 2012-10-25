from default import scripts, engines
from tiling_search import subset

suite = {
    'scripts':  [script for script in scripts if 'Shallow' in script[0]],
    'engines':  engines[0:3] + subset
}

