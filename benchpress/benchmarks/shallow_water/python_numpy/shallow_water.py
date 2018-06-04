from __future__ import print_function

"""
Shallow Water
-------------

So what does this code example illustrate?

Adapted from: http://people.sc.fsu.edu/~jburkardt/m_src/shallow_water_2d/
"""
import numpy as np
from benchpress.benchmarks import util

bench = util.Benchmark("Shallow Water", "height*width*iterations")
g = 9.80665  # gravitational acceleration


def droplet(height, width, data_type=np.float32):
    """Generate grid of droplets"""

    x = np.array(np.linspace(-1, 1, num=width, endpoint=True), dtype=data_type)
    y = np.array(np.linspace(-1, 1, num=width, endpoint=True), dtype=data_type)
    (xx, yy) = np.meshgrid(x, y)
    droplet = height * np.exp(-5 * (xx ** 2 + yy ** 2))
    return droplet


def model(height, width, dtype=np.float32):
    assert height >= 16
    assert width >= 16
    m = np.ones((height, width), dtype=dtype)
    D = droplet(8, 8)  # simulate a water drop
    droploc = height // 4
    (dropx, dropy) = D.shape
    m[droploc:droploc + dropx, droploc:droploc + dropy] += D
    droploc = height // 2
    (dropx, dropy) = D.shape
    m[droploc:droploc + dropx, droploc:droploc + dropy] += D
    return {"H": m, "U": np.zeros_like(m), "V": np.zeros_like(m)}


def simulate(state, timesteps):
    # FLOP count: i*(12*s + 4*s**2 + 14*s**2 + 9*s**2 + 4*s**2 + 9*s**2 + 14*s**2 + 6*s**2 + 19*s**2 + 19*s**2)
    # where s is size and i is iterations
    def loop_body(H, U, V, dt=0.02, dx=1.0, dy=1.0):
        # Reflecting boundary conditions
        H[:, 0] = H[:, 1];
        U[:, 0] = U[:, 1];
        V[:, 0] = -V[:, 1]
        H[:, -1] = H[:, -2];
        U[:, -1] = U[:, -2];
        V[:, -1] = -V[:, -2]
        H[0, :] = H[1, :];
        U[0, :] = -U[1, :];
        V[0, :] = V[1, :]
        H[-1, :] = H[-2, :];
        U[-1, :] = -U[-2, :];
        V[-1, :] = V[-2, :]

        # First half step

        # height
        Hx = (H[1:, 1:-1] + H[:-1, 1:-1]) / 2 - dt / (2 * dx) * (U[1:, 1:-1] - U[:-1, 1:-1])

        # x momentum
        Ux = (U[1:, 1:-1] + U[:-1, 1:-1]) / 2 - \
             dt / (2 * dx) * ((U[1:, 1:-1] ** 2 / H[1:, 1:-1] + g / 2 * H[1:, 1:-1] ** 2) -
                              (U[:-1, 1:-1] ** 2 / H[:-1, 1:-1] + g / 2 * H[:-1, 1:-1] ** 2))

        # y momentum
        Vx = (V[1:, 1:-1] + V[:-1, 1:-1]) / 2 - \
             dt / (2 * dx) * ((U[1:, 1:-1] * V[1:, 1:-1] / H[1:, 1:-1]) -
                              (U[:-1, 1:-1] * V[:-1, 1:-1] / H[:-1, 1:-1]))

        # height
        Hy = (H[1:-1, 1:] + H[1:-1, :-1]) / 2 - dt / (2 * dy) * (V[1:-1, 1:] - V[1:-1, :-1])

        # x momentum
        Uy = (U[1:-1, 1:] + U[1:-1, :-1]) / 2 - \
             dt / (2 * dy) * ((V[1:-1, 1:] * U[1:-1, 1:] / H[1:-1, 1:]) -
                              (V[1:-1, :-1] * U[1:-1, :-1] / H[1:-1, :-1]))
        # y momentum
        Vy = (V[1:-1, 1:] + V[1:-1, :-1]) / 2 - \
             dt / (2 * dy) * ((V[1:-1, 1:] ** 2 / H[1:-1, 1:] + g / 2 * H[1:-1, 1:] ** 2) -
                              (V[1:-1, :-1] ** 2 / H[1:-1, :-1] + g / 2 * H[1:-1, :-1] ** 2))

        # Second half step

        # height
        H[1:-1, 1:-1] -= (dt / dx) * (Ux[1:, :] - Ux[:-1, :]) + (dt / dy) * (Vy[:, 1:] - Vy[:, :-1])

        # x momentum
        U[1:-1, 1:-1] -= (dt / dx) * ((Ux[1:, :] ** 2 / Hx[1:, :] + g / 2 * Hx[1:, :] ** 2) -
                                      (Ux[:-1, :] ** 2 / Hx[:-1, :] + g / 2 * Hx[:-1, :] ** 2)) + \
                         (dt / dy) * ((Vy[:, 1:] * Uy[:, 1:] / Hy[:, 1:]) -
                                      (Vy[:, :-1] * Uy[:, :-1] / Hy[:, :-1]))
        # y momentum
        V[1:-1, 1:-1] -= (dt / dx) * ((Ux[1:, :] * Vx[1:, :] / Hx[1:, :]) -
                                      (Ux[:-1, :] * Vx[:-1, :] / Hx[:-1, :])) + \
                         (dt / dy) * ((Vy[:, 1:] ** 2 / Hy[:, 1:] + g / 2 * Hy[:, 1:] ** 2) -
                                      (Vy[:, :-1] ** 2 / Hy[:, :-1] + g / 2 * Hy[:, :-1] ** 2))
        bench.plot_surface(H, "3d", 0, 0, 5.5)

    bench.do_while(loop_body, timesteps, state['H'], state['U'], state['V'])


def main():
    H = bench.args.size[0]
    W = bench.args.size[1]
    I = bench.args.size[2]

    state = bench.load_data()
    if state is None:
        state = model(H, W, dtype=bench.dtype)

    bench.start()
    simulate(state, I)
    bench.stop()
    bench.save_data(state)
    bench.pprint()


if __name__ == "__main__":
    main()
