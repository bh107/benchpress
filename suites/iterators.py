from default import scripts, engines

suite = {
    'scripts':  scripts,
    'engines':  engines[0:4] + [('iterator', 'iterator', None)] + [('iterator2', 'iterator2', None)] + [('iterator3', 'iterator3', None)]
}
