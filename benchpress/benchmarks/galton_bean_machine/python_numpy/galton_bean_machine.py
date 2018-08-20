from __future__ import print_function
from benchpress.benchmarks import util
import numpy as np

bench = util.Benchmark("Galton Bean Machine", "<num_of_beans>*<height>")


def bean(num_beans, height):
    return np.sum(np.sign(bench.random_array((num_beans, height)) - 0.5), axis=1)


def main():
    num_beans, height = bench.args.size

    bench.start()
    R = bean(num_beans, height)
    bench.stop()
    bench.save_data({'res': R})
    bench.pprint()

    if bench.args.visualize:
        from matplotlib import pyplot
        bins = 100
        pyplot.hist(R, bins)
        pyplot.title("Galton Normal distribution")
        pyplot.xlabel("Value")
        pyplot.ylabel("Frequency")
        pyplot.show()


if __name__ == "__main__":
    main()
