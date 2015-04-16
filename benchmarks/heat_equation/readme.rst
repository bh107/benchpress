Simulates the dissipation of heat in a grid of size H * W until it converges with a max of I iterations. An iterative Jacobi method performing a stencil operation of a two-dimensional rectangular grid until it converges or until max iterations is reached.

Runs Jacobi on a rectangular grid for until it converges or until max iterations is reached::

  --size=3000*3000*100

Use ``--verbose`` to print number of iterations executed and a subset of the grid.
Set iterations = 0 to disable max_iterations.
