from default import engines, scripts

mcache_engines = [
    ('score_mcache_%s' % (mcache_size),
    'score',
    {
        "CPHVB_CORE_VCACHE_SIZE":   str(mcache_size),
    }) for mcache_size in range(1, 20)
]
mcache_engines += [
    ('naive_mcache_%s' % (mcache_size),
    'naive',
    {
        "CPHVB_CORE_VCACHE_SIZE":   str(mcache_size),
    }) for mcache_size in range(1, 20)
]

suite = {
    'scripts':  scripts,
    'engines':  engines[0:4] + mcache_engines
}
