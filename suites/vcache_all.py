from default import engines, scripts

vcache_engines = [
    ('score_vcache_%s' % (vcache_size),
    'score',
    {
        "CPHVB_CORE_VCACHE_SIZE":   str(vcache_size),
    }) for vcache_size in range(1, 20)
]
vcache_engines += [
    ('naive_vcache_%s' % (vcache_size),
    'naive',
    {
        "CPHVB_CORE_VCACHE_SIZE":   str(vcache_size),
    }) for vcache_size in range(1, 20)
]

suite = {
    'scripts':  scripts,
    'engines':  engines[0:4] + vcache_engines
}
