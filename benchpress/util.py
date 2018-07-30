from __future__ import print_function
import argparse
import pprint
import time
import sys
import numpy as np
import atexit
import gzip

gfx_handle = None

# Check whether the numpy module is overruled by Bohrium
bh_is_loaded_as_np = np.__name__ == "bohrium"

# In order to support runs without bohrium installed, we need some import hacks
try:
    import numpy_force as np
except ImportError:
    import numpy as np


class VisualArgs:
    def __init__(self, args):
        self.count = -1
        self.rate = args.visualize_rate
        self.param = args.visualize_param
        self.trace = {'org': [], 'zip': []}
        self.trace_fname = args.visualize_trace  # When None, no tracing
        self.dry = args.visualize_dry


_visual_args = None  # When None, no visualization


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
    if _visual_args.trace_fname is None and not _visual_args.dry:
        if sys.version_info[0] == 2:
            raw_input(msg)
        else:
            input(msg)


def plot_surface_wrapper(*args):
    global _visual_args
    from bohrium import visualization

    _visual_args.count += 1
    if not (_visual_args.count % _visual_args.rate == 0):
        return

    if _visual_args.dry:  # We force the visualization process on a dry run
        visualization.compressed_copy(args[0], param=_visual_args.param).copy2numpy()
    else:
        if _visual_args.trace_fname is None:  # We don't show visualization when tracing
            if _visual_args.param is None:
                visualization.plot_surface(*args)
            else:
                visualization.plot_surface(*args, param=_visual_args.param)
        else:
            org = args[0].copy2numpy()
            compressed = visualization.compressed_copy(args[0], param=_visual_args.param).copy2numpy()
            _visual_args.trace['org'].append(org)
            _visual_args.trace['zip'].append(compressed)
            print("plot_surface %s: %s" % (_visual_args.count, len(_visual_args.trace['org'])), file=sys.stderr)


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
        global _visual_args

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
        p.add_argument('--seed',
                       default=42,
                       help="The seed to use when using random data."
                       )
        p.add_argument('--inputfn',
                       default=None,
                       help="Input file to use as data.",
                       metavar="FILE",
                       type=str,
                       )
        p.add_argument('--outputfn',
                       default=None,
                       help="Output file to store results in (.npz extension will "
                            "be appended to the file name if it is not already there).",
                       metavar="FILE",
                       type=str,
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
        p.add_argument('--visualize-rate',
                       default=1,
                       type=int,
                       help="The rate of visualization (Default: 1, which means all frame)"
                       )
        p.add_argument('--visualize-param',
                       default=None,
                       help="Set visualization parameters."
                       )
        p.add_argument('--visualize-trace',
                       default=None,
                       type=str,
                       help="Dump frames to files instead of showing them"
                       )
        p.add_argument('--visualize-dry',
                       default=False,
                       action='store_true',
                       help="Do the data process but don't show any visualization"
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
        self.inputfn = args.inputfn
        self.outputfn = args.outputfn
        self.seed = int(args.seed)
        randseed(self.seed)

        if len(self.size) == 0:
            raise argparse.ArgumentTypeError('Size must be specified e.g. --size=100*10*1')

        if bh_is_loaded_as_np:
            self.bohrium = True
        else:
            self.bohrium = False

        self.no_extmethods = args.no_extmethods
        self.verbose = args.verbose
        self.visualize = args.visualize
        if self.visualize:
            _visual_args = VisualArgs(args)

    def start(self):
        flush()
        self.__elapsed = time.time()

    def stop(self):
        flush()
        self.__elapsed = time.time() - self.__elapsed

    def save_data(self, data_dict):
        """Save `data_dict` as a npz archive when --outputfn is used"""
        assert (isinstance(data_dict, dict))
        if self.outputfn is not None:
            # Clean `data_dict` for Bohrium arrays
            nobh_data = {"_bhary_keys": []}
            for k in data_dict.keys():
                if hasattr(data_dict[k], "copy2numpy"):
                    nobh_data[k] = data_dict[k].copy2numpy()
                    nobh_data["_bhary_keys"].append(k)
                else:
                    nobh_data[k] = data_dict[k]
            np.savez_compressed(self.outputfn, **nobh_data)

    def load_data(self):
        """Load the npz archive specified by --inputfn or None is not set"""
        if self.inputfn is None:
            return None
        else:
            nobh_data = np.load(self.inputfn)
            bhary_keys = nobh_data["_bhary_keys"].tolist()
            ret = {}
            for k in nobh_data.keys():
                if k == "_bhary_keys":
                    continue
                # Convert numpy arrays into bohrium arrays
                if bh_is_loaded_as_np and k in bhary_keys:
                    a = nobh_data[k]
                    ret[k] = bh.array(a, bohrium=True)
                else:
                    ret[k] = nobh_data[k]
            return ret

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
        func.__globals__['get_iterator'] = lambda x=0: i + x

        def get_grid(*args):
            assert(len(args) > 0)
            grid = args[::-1]
            iterators = ()
            for dim, iterations in enumerate(grid):
                it = int(i/step_delay) % iterations
                step_delay *= iterations
                iterators = (it,) + iterators
            return iterators

        func.__globals__['get_grid'] = lambda args: get_grid(args)

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


def dump_visualization_trace_file(visual_args, field):
    fname = "%s_%s.npy.gz" % (visual_args.trace_fname, field);
    data = np.stack(visual_args.trace[field])
    del visual_args.trace[field]

    print("Writing visualization trace file: %s (%s)" % (fname, data.shape))
    f = gzip.GzipFile("%s" % fname, "w")
    np.save(f, data)
    del data
    f.close()


@atexit.register
def goodbye():
    if _visual_args is not None \
            and _visual_args.trace_fname is not None \
            and bh_is_loaded_as_np:
        dump_visualization_trace_file(_visual_args, "org")
        dump_visualization_trace_file(_visual_args, "zip")

        from bohrium import _bh
        msg = _bh.message("statistics-detail")
        with open("%s_stat.txt" % _visual_args.trace_fname, "w") as f:
            f.write(msg)
