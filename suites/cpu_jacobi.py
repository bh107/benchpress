from default import scripts, engines

suite = {
    'scripts': [script for script in scripts if 'PS' in script[0]],
    'engines': engines[0:5]
}
