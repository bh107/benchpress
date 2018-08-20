# By  Natalino Busa <https://gist.github.com/natalinobusa/4633275>
from __future__ import print_function
from benchpress.benchmarks import util
import numpy as np

bench = util.Benchmark("Snakes and Ladders", "size*iterations")


def nullgame(size, dtype):
    p = np.zeros((size + 1, size + 1), dtype=dtype)

    for i in range(size + 1):
        for j in range(6):
            if i + j < size:
                p[i][i + j + 1] = 1.0 / 6.0

    p[size][size] = 1
    p[size - 1][size] = 6.0 / 6.0
    p[size - 2][size] = 5.0 / 6.0
    p[size - 3][size] = 4.0 / 6.0
    p[size - 4][size] = 3.0 / 6.0
    p[size - 5][size] = 2.0 / 6.0
    p[size - 6][size] = 1.0 / 6.0
    return p


def main():
    size, iterations = bench.args.size

    if bench.args.visualize:
        from matplotlib import pyplot

    a = np.array(np.zeros(size + 1, dtype=bench.dtype))
    p = np.array(nullgame(size, dtype=bench.dtype))
    m = p  # Initial matrix is p
    pr_end = np.array(np.zeros(iterations, dtype=bench.dtype))

    bench.start()
    for k in range(iterations):
        if bench.args.visualize:
            # Plot the probability distribution at the k-th iteration
            pyplot.figure(1)
            pyplot.plot(m[0][0:size])

        # Store the probability of ending after the k-th iteration
        pr_end[k] = m[0][size]

        # Store/plot the accumulated marginal probability at the k-th iteration
        a = a + m[0]

        bench.flush()
        if bench.args.visualize:
            pyplot.figure(2)
            pyplot.plot(a[0:size])

        # calculate the stocastic matrix for iteration k+1
        if util.bh_is_loaded_as_np and bench.args.no_extmethods:
            m = np.array(np.dot(m.copy2numpy(), p.copy2numpy()))
        else:
            m = np.dot(m, p)
    bench.stop()
    bench.pprint()

    # plot the probability of ending the game
    # after k iterations
    if bench.args.visualize:
        pyplot.figure(3)
        pyplot.plot(pr_end[0:iterations - 1])

        # show the three graphs
        pyplot.show()


if __name__ == "__main__":
    main()
