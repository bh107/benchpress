from default import scripts, engines

suite = {
    'scripts':  scripts,
    'engines':  engines[0:4] + [('iterator', 'iterator', None)]
}
