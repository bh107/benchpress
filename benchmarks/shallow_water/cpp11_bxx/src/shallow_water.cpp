/*
This file is part of Bohrium and Copyright (c) 2012 the Bohrium team:
http://bohrium.bitbucket.org

Bohrium is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as
published by the Free Software Foundation, either version 3
of the License, or (at your option) any later version.

Bohrium is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the
GNU Lesser General Public License along with bohrium.

If not, see <http://www.gnu.org/licenses/>.
*/
#include <iostream>
#include <vector>
#include <bxx/bohrium.hpp>
#include <bp_util.h>

using namespace std;
using namespace bxx;

static double g = 9.80665;  // Gravitational acceleration

template <typename T>
void step(multi_array<T>& H, multi_array<T>& U, multi_array<T>& V, T dt, T dx, T dy)
{
    multi_array<T> Hx, Ux, Vx, Hy, Uy, Vy;

    // Reflecting boundary conditions
    H[_ALL()][0]   =       H[_ALL()][1];
    U[_ALL()][0]   =       U[_ALL()][1];
    V[_ALL()][0]   = (T)-1*V[_ALL()][1];

    H[_ALL()][-1]  =       H[_ALL()][-2];
    U[_ALL()][-1]  =       U[_ALL()][-2];
    V[_ALL()][-1]  = (T)-1*V[_ALL()][-2];

    H[0][_ALL()]   =       H[1][_ALL()];
    U[0][_ALL()]   = (T)-1*U[1][_ALL()];
    V[0][_ALL()]   =       V[1][_ALL()];

    H[-1][_ALL()]  =       H[-2][_ALL()];
    U[-1][_ALL()]  = (T)-1*U[-2][_ALL()];
    V[-1][_ALL()]  =       V[-2][_ALL()];

    // First half step
    // height
    Hx = (H[_ABF()][_INNER()] + H[_ABL()][_INNER()]) / (T)2 - dt/((T)2*dx) * (U[_ABF()][_INNER()] - U[_ABL()][_INNER()]);

    // x momentum
    Ux =                (U[_ABF()][_INNER()]       + U[_ABL()][_INNER()]) / (T)2 -
    dt/((T)2*dx) * ((pow(U[_ABF()][_INNER()], 2.0) / H[_ABF()][_INNER()] + g / (T)2 * pow(H[_ABF()][_INNER()], 2.0)) -
                    (pow(U[_ABL()][_INNER()], 2.0) / H[_ABL()][_INNER()] + g / (T)2 * pow(H[_ABL()][_INNER()], 2.0)));
    
    // y momentum
    Vx =            (V[_ABF()][_INNER()] + V[_ABL()][_INNER()]) / (T)2 -
    dt/((T)2*dx) * ((U[_ABF()][_INNER()] * V[_ABF()][_INNER()]  / H[_ABF()][_INNER()]) -
                    (U[_ABL()][_INNER()] * V[_ABL()][_INNER()]  / H[_ABL()][_INNER()]));

    // height
    Hy = (H[_INNER()][_ABF()] + H[_INNER()][_ABL()]) / (T)2 - dt/((T)2*dy) * (V[_INNER()][_ABF()] - V[_INNER()][_ABL()]);

    // x momentum
    Uy =          (U[_INNER()][_ABF()] + U[_INNER()][_ABL()]) / (T)2 -
    dt/((T)2*dy)*((V[_INNER()][_ABF()] * U[_INNER()][_ABF()]  / H[_INNER()][_ABF()]) -
                  (V[_INNER()][_ABL()] * U[_INNER()][_ABL()]  / H[_INNER()][_ABL()]));

    // y momentum
    Vy =              (V[_INNER()][_ABF()] +     V[_INNER()][_ABL()]) / (T)2 -
    dt/((T)2*dy)*((pow(V[_INNER()][_ABF()],2.0)/ H[_INNER()][_ABF()] + g/(T)2*pow(H[_INNER()][_ABF()],2.0)) -
                  (pow(V[_INNER()][_ABL()],2.0)/ H[_INNER()][_ABL()] + g/(T)2*pow(H[_INNER()][_ABL()],2.0)));
    //
    // Second half step

    // height
    H[_INNER()][_INNER()] -= (dt/dx)*(Ux[_ABF()][_ALL()] - Ux[_ABL()][_ALL()]) + (dt/dy) * (Vy[_ALL()][_ABF()] - Vy[_ALL()][_ABL()]);

    // x momentum
    U[_INNER()][_INNER()] -= (dt/dx)*((pow(Ux[_ABF()][_ALL()],2.0) / Hx[_ABF()][_ALL()] + g/(T)2*pow(Hx[_ABF()][_ALL()],2.0)) -
                                      (pow(Ux[_ABL()][_ALL()],2.0) / Hx[_ABL()][_ALL()] + g/(T)2*pow(Hx[_ABL()][_ALL()],2.0))) +
                             (dt/dy)*((Vy[_ALL()][_ABF()] * Uy[_ALL()][_ABF()] / Hy[_ALL()][_ABF()]) -
                                      (Vy[_ALL()][_ABL()] * Uy[_ALL()][_ABL()] / Hy[_ALL()][_ABL()]));
    // y momentum
    V[_INNER()][_INNER()] -= (dt/dx)*((    Ux[_ABF()][_ALL()] *      Vx[_ABF()][_ALL()] /            Hx[_ABF()][_ALL()]) -
                                      (    Ux[_ABL()][_ALL()] *      Vx[_ABL()][_ALL()] /            Hx[_ABL()][_ALL()])) +
                             (dt/dy)*((pow(Vy[_ALL()][_ABF()],2.0) / Hy[_ALL()][_ABF()] + g/(T)2*pow(Hy[_ALL()][_ABF()],2.0)) -
                                      (pow(Vy[_ALL()][_ABL()],2.0) / Hy[_ALL()][_ABL()] + g/(T)2*pow(Hy[_ALL()][_ABL()],2.0)));
}

template <typename T>
void simulate(multi_array<T>& H, multi_array<T>& U, multi_array<T>& V, int64_t timesteps, int visualize)
{
    for(int timestep=0; timestep<timesteps; ++timestep) {
        step(H, U, V, 0.02, 1.0, 1.0);
        if (visualize) {
            plot_surface(H, 1, 0, 0, 5.5);
        }
    }
}

int main(int argc, char* argv[])
{
    bp_util_type bp = bp_util_create(argc, argv, 3);
    if (bp.args.has_error) {
        return 0;
    }
    const size_t height     = bp.args.sizes[0];
    const size_t width      = bp.args.sizes[1];
    const int64_t timesteps = bp.args.sizes[2];

    multi_array<double> H, U, V;

    H = ones<double>(height, width);
    U = zeros<double>(height, width);
    V = zeros<double>(height, width);

    multi_array<double> x, y, xx, yy, droplet;  // Create droplet
    x = linspace<double>(-1, 1, 8, true);
    y = linspace<double>(-1, 1, 8, true);
    xx = gridify(x, 0);
    yy = gridify(x, 1);
    
    droplet = 8.0 * exp(-5.0 * (pow(xx,2.0) + pow(yy,2.0)));
                                                // Let it drip into the water
    size_t droploc = height / 2;
    H[_(droploc,droploc+7)][_(droploc,droploc+7)] += droplet;
    droploc = height / 4;
    H[_(droploc,droploc+7)][_(droploc,droploc+7)] += droplet;

    Runtime::instance().flush();                // Run the simulation
    bp.timer_start();
    simulate(H, U, V, timesteps, (int)bp.args.visualize);
    Runtime::instance().flush();
    bp.timer_stop();
    
    bp.print("shallow_water(cpp11_bxx)");
    if (bp.args.verbose) {                      // and values.
        cout << ", output: " << endl;
    }

    return 0;
}

