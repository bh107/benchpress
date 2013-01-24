#!/usr/bin/env python
import bohrium as np
import bohriumbridge as bb
import json
import time
import sys
import util
import tempfile


ttup = [
    ('BH_BOOL',   np.bool),

    ('BH_INT8',   np.int8),
    ('BH_INT16',  np.int16),
    ('BH_INT32',  np.int32),
    ('BH_INT64',  np.int64),

#    ('BH_FLOAT16',  np.float16),
    ('BH_FLOAT32',  np.float32),
    ('BH_FLOAT64',  np.float64),

    ('BH_UINT8',   np.uint8),
    ('BH_UINT16',  np.uint16),
    ('BH_UINT32',  np.uint32),
    ('BH_UINT64',  np.uint64),

    ('BH_COMPLEX64', np.complex64),
    ('BH_COMPLEX128', np.complex128)
]
tmap = dict(ttup)

def main( B, runs=5 ):

    N = B.size.pop()

    print "Loading Bohrium-opcodes."
    instructions    = json.load(open('../../core/codegen/opcodes.json'))
    ufuncs          = [ufunc for ufunc in instructions if not ufunc['system_opcode']]

    ignore_t = ['BH_COMPLEX64']
    ignore_f = ['BH_IDENTITY']
    
    print "Allocating operands."
    operands = {}                   # Setup operands of various types
    for bh_type, np_type in ttup:

        if 'bool' in bh_type.lower():
            operands[ bh_type ] = (
                np.ones([N],            dtype=np_type, bohrium=B.bohrium),
                np.array([ True  ] * N, dtype=np_type, bohrium=B.bohrium),
                np.array([ False ] * N, dtype=np_type, bohrium=B.bohrium),
            )
        elif 'int' in bh_type.lower():
            operands[ bh_type ] = (
                np.ones([N],         dtype=np_type, bohrium=B.bohrium),
                np.array([ 3 ] * N,  dtype=np_type, bohrium=B.bohrium),
                np.array([ 2 ] * N,  dtype=np_type, bohrium=B.bohrium),
            )
        elif 'float' in bh_type.lower():
            operands[ bh_type ] = (
                np.ones([N],             dtype=np_type, bohrium=B.bohrium),
                np.array([ 3.75 ] * N,   dtype=np_type, bohrium=B.bohrium),
                np.array([ 2.0  ] * N,   dtype=np_type, bohrium=B.bohrium),
            )
        elif 'complex' in bh_type.lower():
            operands[ bh_type ] = (
                np.ones([N],             dtype=np_type, bohrium=B.bohrium),
                np.array([ 3.75 ] * N,   dtype=np_type, bohrium=B.bohrium),
                np.array([ 2.0  ] * N,   dtype=np_type, bohrium=B.bohrium),
            )
    bb.flush()
    
    print ""
    print "Executing %d ufuncs" % len(ufuncs)
    error_count = 0
    results     = []
    for ufunc in ufuncs:

        opcode  = ufunc['opcode']
        if opcode in ignore_f:
            continue

        types   = ufunc['types']
        nop     = ufunc['nop']
        fp      = np.__dict__[opcode.replace('BH_','').lower()]

        for typesig in types:

            params = []
            if nop == 2:
                params.append( operands[typesig[1]][1] )
                params.append( operands[typesig[0]][0] )
            elif nop == 3:
                params.append( operands[typesig[1]][1] )
                params.append( operands[typesig[2]][2] )
                params.append( operands[typesig[0]][0] )
            else:
                print "WHAT!!!? "+nop

            invocation_err = ""
            times = []
            for _ in xrange(0, runs):
                s = elapsed = 0.0
                try:
                    bb.flush()
                    s = time.time()
                    for _ in xrange(0,10):
                        fp( *params )
                    bb.flush()
                    elapsed = time.time() - s
                    times.append( elapsed )
                except Exception as e:
                    invocation_err = str(e)
                    error_count += 1

            val = params[-1][0] if str(params[-1][0]) else '?'
            results.append( [opcode, typesig, times, str(val), invocation_err, B.bohrium] )

    print "%d successful invocations %s with error." % (len(ufuncs)-error_count, error_count)

    return results

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Runs a benchmark suite and stores the results in a json-file.')
    parser.add_argument(
        'src',
        help='Path to the Bohrium source-code.'
    )
    parser.add_argument(
        '--output',
        default="results",
        help='Where to store benchmark results.'
    )
    args = parser.parse_args()

    B = util.Benchmark()
    B.start()
    results = main( B, 3 )
    B.stop()
    B.pprint()

    with tempfile.NamedTemporaryFile(delete=False, dir='/tmp', prefix='res-', suffix='.json') as fd:
        print "Running micro-benchmark; results are written to '%s'." % fd.name
        json.dump(results, fd, indent=4)

