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

namespace HeatEquation
{
	public static class HeatEquation
    {
		public static void Main (string[] args)
		{
			bool useIterationLimit = false;
			bool quadratic = false;

			// These compile directives add support for building the benchmark in various configurations
			#if HEATEQUATION_FIXED
			useIterationLimit = true;
			#endif

			var numArgs = 1 + (quadratic ? 0 : 1) + (useIterationLimit ? 1 : 0);

			Utilities.RunBenchmark.Run(args, numArgs,
				// Running the benchmark
				(input) => 
				{
					var arglist = new Queue<long>(input.sizes);

					var sizew = arglist.Dequeue();
					var sizeh = quadratic ? sizew : arglist.Dequeue();					
					long? iterations = useIterationLimit ? (long?)arglist.Dequeue() : null;
					int usedIterations;
					
					if (input.type == typeof(double)) {
						var data = HeatEquationSolverDouble.Create(sizew, sizeh);
						if (input.use_bohrium)
							NumCIL.Bohrium.Utility.Flush();
						using (new DispTimer(string.Format("HeatEquation (Double) {0}x{1}*{2}", sizew, sizeh, iterations)))
						{
							var r = HeatEquationSolverDouble.Solve(data, iterations);
							usedIterations = r.Item1;
							if (input.use_bohrium)
								NumCIL.Bohrium.Utility.Flush();
						}
					} else {
						var data = HeatEquationSolverSingle.Create (sizew, sizeh);
						if (input.use_bohrium)
							NumCIL.Bohrium.Utility.Flush();
						using (new DispTimer(string.Format("HeatEquation (Float) {0}x{1}*{2}", sizew, sizeh, iterations)))
						{
							var r = HeatEquationSolverSingle.Solve(data, iterations);
							usedIterations = r.Item1;
							if (input.use_bohrium)
								NumCIL.Bohrium.Utility.Flush();
						}
					}

					Console.WriteLine("Iterations: {0}", usedIterations);
				}
			);
		}
    }
}
