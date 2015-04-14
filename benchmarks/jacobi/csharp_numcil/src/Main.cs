#region Copyright
/*
This file is part of Bohrium and copyright (c) 2012 the Bohrium:
team <http://www.bh107.org>.

Bohrium is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as
published by the Free Software Foundation, either version 3
of the License, or (at your option) any later version.

Bohrium is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the
GNU Lesser General Public License along with Bohrium.

If not, see <http://www.gnu.org/licenses/>.
*/
#endregion

using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using NumCIL;
using Utilities;

namespace jacobi
{
	public static class Jacobi
    {
		public static void Main (string[] args)
		{
			bool solveDelta = true;
			bool useIterationLimit = false;
			bool quadratic = true;

			// These compile directives add support for building the benchmark in various configurations
			#if JACOBI_FIXED
			solveDelta = false;
			useIterationLimit = true;
			quadratic = true;
			#endif

			#if JACOBI_SOLVE
			solveDelta = true;
			useIterationLimit = true;
			quadratic = false;
			#endif

			#if JACOBI_STENCIL
			solveDelta = false;
			useIterationLimit = true;
			quadratic = false;
			#endif

			var numArgs = 1 + (quadratic ? 0 : 1) + (useIterationLimit ? 1 : 0);

			Utilities.RunBenchmark.Run(args, numArgs,
				// Running the benchmark
				(input) => 
				{
					var arglist = new Stack<long>(input.sizes);

					var sizew = arglist.Pop();
					var sizeh = quadratic ? sizew : arglist.Pop();					
					long? iterations = useIterationLimit ? (long?)arglist.Pop() : null;
					
					if (input.type == typeof(double)) {
						var data = JacobiSolverDouble.Create(sizew, sizeh);
						using (new DispTimer(string.Format("Jacobi (Double) {0}x{1}*{2}", sizew, sizeh, iterations)))
							JacobiSolverDouble.Solve(data, solveDelta, iterations);
					} else {
						var data = JacobiSolverSingle.Create (sizew, sizeh);
						using (new DispTimer(string.Format("Jacobi (Float) {0}x{1}*{2}", sizew, sizeh, iterations)))
							JacobiSolverSingle.Solve(data, solveDelta, iterations);
					}
				}
			);
		}
    }
}
