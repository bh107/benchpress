from __future__ import print_function
import argparse
import pprint
import time
import sys
import numpy as np
import atexit


gfx_handle = None
visualization_param = None
visualization_trace = False

# Check whether the numpy module is overruled by Bohrium
bh_is_loaded_as_np = np.__name__ == "bohrium"

# In order to support runs without bohrium installed, we need some import hacks
try:
    import numpy_force as np
except ImportError:
    import numpy as np


def numpy_flush():
    return


def numpy_array(ary, bohrium=False, dtype=np.float64):
    return np.array(ary, dtype=dtype)


def numpy_plot_surface(ary, mode="2d", colormap=0, lowerbound=-200, upperbound=200):
    def surface2d():
        global gfx_handle
        if not gfx_handle:
            import matplotlib.pyplot as plt
            plt.figure()
            img = plt.imshow(ary, interpolation="nearest", cmap=plt.cm.gray)
            plt.show(False)
            gfx_handle = {
                "plt": plt,
                "img": img
            }
        else:
            plt = gfx_handle["plt"]
            img = gfx_handle["img"]

        plt.ion()
        img.set_data(ary)
        plt.draw()

    def surface3d():
        global gfx_handle
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D
        from matplotlib.ticker import LinearLocator, FormatStrFormatter
        from matplotlib import cm

        if not gfx_handle:
            gfx_handle = {
                "fig": plt.figure()
            }
            plt.show(False)

        fig = gfx_handle["fig"]

        ax = fig.gca(projection='3d')

        H, W = ary.shape
        X = np.arange(0, W, 1)
        Y = np.arange(0, H, 1)
        X, Y = np.meshgrid(X, Y)

        surf = ax.plot_surface(
            X, Y, ary, rstride=1, cstride=1, cmap='winter',
            linewidth=0, antialiased=False
        )
        if "surf" in gfx_handle:
            gfx_handle["surf"].remove()

        gfx_handle["surf"] = surf
        ax.set_zlim(0, 10)

        ax.zaxis.set_major_locator(LinearLocator(10))
        ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

        plt.ion()
        plt.draw()

    if mode.lower() == "2d":
        surface2d()
    elif mode.lower() == "3d":
        surface3d()
    else:
        raise Exception("Invalid mode.")


def confirm_exit(msg="Hit Enter to exit..."):
    if visualization_param is None:
        if sys.version_info[0] == 2:
            raw_input(msg)
        else:
            input(msg)


def plot_surface_wrapper(*args):
    global visualization_trace
    from bohrium import visualization

    if visualization_param is None:
        visualization.plot_surface(*args)
    #else:
    #    visualization.plot_surface(*args, param=visualization_param)

    if visualization_trace or isinstance(visualization_trace, dict):
        if not isinstance(visualization_trace, dict):
            visualization_trace = {'org': [], 'zip': []}

        org = args[0].copy2numpy()
        compressed = visualization.compressed_copy(args[0], param=visualization_param).copy2numpy()
        visualization_trace['org'].append(org)
        visualization_trace['zip'].append(compressed)


try:
    import bohrium as bh
    from bohrium import visualization

    toarray = bh.array
    flush = bh.flush
    rand = bh.random.random_sample
    randint = bh.random.random_integers
    randseed = bh.random.seed
    bh_module_exist = True
except ImportError:
    toarray = numpy_array
    flush = numpy_flush
    rand = np.random.random_sample
    randint = np.random.random_integers
    randseed = np.random.seed
    bh_module_exist = False

if bh_is_loaded_as_np:
    plot_surface = plot_surface_wrapper
else:
    plot_surface = numpy_plot_surface


def t_or_f(arg):
    """Helper function to parse "True/true/TrUe/False..." as bools."""

    ua = str(arg).lower()
    if ua == 'true'[:len(ua)]:
        return True
    elif ua == 'false'[:len(ua)]:
        return False
    else:
        return arg


class Benchmark:
    """
    Helper class to aid running Python/NumPy programs with and without npbackend.

    Use it to sample elapsed time using: start()/stop()
    Pretty-prints results using pprint().
    start()/stop() will send flush signals to npbackend, ensuring that only
    the statements in-between start() and stop() are measured.
    """

    def __init__(self):
        global visualization_param, visualization_trace

        self.__elapsed = 0.0  # The quantity measured
        self.__script = sys.argv[0]  # The script being run

        # Construct argument parser
        p = argparse.ArgumentParser(description='Benchmark runner for npbackend.')

        p.add_argument('--size',
                       help="Tell the script the size of the data to work on."
                       )
        p.add_argument('--dtype',
                       choices=["uint8", "float32", "float64"],
                       default="float64",
                       help="Tell the the script which primitive type to use."
                            " (default: %(default)s)"
                       )
        g1 = p.add_mutually_exclusive_group()
        g1.add_argument('--inputfn',
                        help="Input file to use as data. When not set, random data is used."
                        )
        g1.add_argument('--seed',
                        default=42,
                        help="The seed to use when using random data."
                        )
        p.add_argument('--dumpinput',
                       default=False,
                       action='store_true',
                       help="Dumps the benchmark input to file."
                       )
        p.add_argument('--outputfn',
                       help="Output file to store results in."
                       )

        p.add_argument('--bohrium',
                       choices=[True, False],
                       default=False,
                       type=t_or_f,
                       help="Enable npbackend using Bohrium."
                            " (default: %(default)s)"
                       )
        p.add_argument('--no-extmethods',
                       default=False,
                       action='store_true',
                       help="Disable extension methods."
                       )

        p.add_argument('--visualize',
                       default=False,
                       action='store_true',
                       help="Enable visualization in script."
                       )
        p.add_argument('--visualize-param',
                       default=None,
                       help="Set visualization parameters."
                       )
        p.add_argument('--visualize-trace',
                       default=False,
                       action='store_true',
                       help="Dump frames to files instead of showing them"
                       )
        p.add_argument('--verbose',
                       default=False,
                       action='store_true',
                       help="Print out misc. information from script."
                       )
        p.add_argument('--no-flush',
                       action='store_true',
                       help="Disable calls to flush within benchmark iterations."
                       )
        p.add_argument('--no-do_while',
                       action='store_true',
                       help="Disable Bohrium's optimized `do_while`."
                       )

        args, unknown = p.parse_known_args()  # Parse the arguments

        #
        # Conveniently expose options to the user
        #
        self.args = args
        self.size = [int(i) for i in args.size.split("*")] if args.size else []
        self.dtype = eval("np.%s" % args.dtype)
        self.dumpinput = args.dumpinput
        self.inputfn = args.inputfn
        self.outputfn = args.outputfn
        self.seed = int(args.seed)
        randseed(self.seed)

        if len(self.size) == 0:
            raise argparse.ArgumentTypeError('Size must be specified e.g. --size=100*10*1')

        if not bh_is_loaded_as_np and args.bohrium:
            print(
                """
                !!!!!!!

                WARNING:

                --bohrium does not enable Bohrium!

                Unless the benchmark does an explicit check (which it should not).
                To enable Bohrium, overload NumPy with 'python -m bohrium ...'

                !!!!!!!
                """
            )

        if bh_is_loaded_as_np:
            self.bohrium = True
        else:
            self.bohrium = False

        self.no_extmethods = args.no_extmethods
        self.visualize = args.visualize
        self.verbose = args.verbose
        visualization_param = args.visualize_param
        visualization_trace = args.visualize_trace

    def start(self):
        flush()
        self.__elapsed = time.time()

    def stop(self):
        flush()
        self.__elapsed = time.time() - self.__elapsed

    def tofile(self, filename, arrays):
        for k in arrays:
            arrays[k] = toarray(arrays[k], bohrium=False)
        np.savez(filename, **arrays)

    def dump_arrays(self, prefix, arrays):
        """
        Dumps a dict of arrays organized such as:

        arrays = {'lbl1': array1, 'lbl2': array2}

        Into a file using the following naming convention:
        "prefix_lbl1-DTYPE-SHAPE_lbl2-DTYPE-SHAPE"

        The arrays are stored as .npz files.
        """
        names = []
        for k in arrays:
            names.append("%s-%s-%s" % (
                k,
                arrays[k].dtype,
                '*'.join([str(x) for x in (arrays[k].shape)])))
        filename = "%s_%s" % (prefix, '_'.join(names))
        self.tofile(filename, arrays)

    def load_arrays(self, filename=None, dtype=None):
        """
        Load arrays from disk (npz-file) and ensure they
        are in the right "space", that is, Numpy or Bohrium.

        Optionally convert the array dtype.

        :filename: npz-file containing arrays.
        :dtype: Convert arrays to this dtype; None = No conversion.
        """

        if not filename:  # Default to the cmd-line parameter
            filename = self.inputfn

        npz = np.load(filename)  # Load the arrays from disk (npz-file)

        arrays = {}  # Make sure arrays are in the correct space
        for k in npz:
            if dtype:  # Convert type when requested
                arrays[k] = toarray(npz[k], bohrium=self.bohrium, dtype=dtype)
            else:  # Othervise, use format they are stored in.
                arrays[k] = toarray(npz[k], bohrium=self.bohrium)

        del npz  # We no longer need these

        return arrays

    def load_array(self, filename=None, label='input', dtype=None):

        if not filename:
            filename = self.inputfn

        return self.load_arrays(filename, dtype)[label]

    def pprint(self):
        print("%s - bohrium: %s, size: %s, elapsed-time: %f" % (
            self.__script,
            self.bohrium,
            '*'.join([str(s) for s in self.size]),
            self.__elapsed
        ))

    def random_array(self, shape, dtype=None):
        if dtype is None:
            dtype = self.dtype
        if issubclass(np.dtype(dtype).type, np.integer):
            if bh_module_exist:
                ret = randint(shape, bohrium=self.bohrium)
            else:
                ret = randint(shape)
        else:
            if bh_module_exist:
                ret = rand(shape, bohrium=self.bohrium)
            else:
                ret = rand(shape)
        return toarray(ret, dtype=dtype, bohrium=self.bohrium)

    def flush(self):
        """Executes the queued instructions when running through Bohrium"""
        if self.bohrium and not self.args.no_flush:
            import bohrium as bh
            bh.flush()

    def do_while(self, func, niters, *args, **kwargs):
        """Implements `bohrium.do_while()` for regular NumPy"""

        if self.bohrium and not self.visualize and not self.args.no_do_while:
            return bh.do_while(func, niters, *args, **kwargs)

        import sys
        i = 0
        if niters is None:
            niters = sys.maxsize
        while i < niters:
            cond = func(*args, **kwargs)
            if cond is not None and not cond:
                break
            i += 1
            self.flush()
        return i


def main():
    B = Benchmark()
    B.start()
    B.stop()
    if B.visualize:
        pprint.pprint(B.args)
    B.pprint()


if __name__ == "__main__":
    main()


@atexit.register
def goodbye():
    if visualization_trace and bh_is_loaded_as_np:
        orgs = np.stack(visualization_trace['org'])
        del visualization_trace['org']
        fname = "vtrace_org"
        print("Writing visualization trace file: %s.npy (%s)" % (fname, orgs.shape))
        np.save(fname, orgs)
        del orgs

        zips = np.stack(visualization_trace['zip'])
        del visualization_trace['zip']
        fname = "vtrace_zip"
        print("Writing visualization trace file: %s.npy (%s)" % (fname, zips.shape))
        np.save(fname, zips)
        del zips

        from bohrium import _bh
        msg = _bh.message("statistics-detail")
        with open("vtrace_stat.txt", "w") as f:
            f.write(msg)
