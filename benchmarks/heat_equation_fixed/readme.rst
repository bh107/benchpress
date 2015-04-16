Simulates the dissipation of heat using an iterative Jacobi method on a two-dimensional grid of size H * W for a fixed number of I iterations.

The benchmark performs one major computational tasks, applying the stencil-update :math:`0.2*(x_1, x_2, x_3, x_4, x_4)`.
Invoke with::

  --size=H*W*I

Use ``--verbose`` to print number of iterations executed and a subset of the grid.

+-------------------------------------------+-------------------------------------------+-------------------------------------------+
| ``--size=100*100*1 --visualize``          | ``--size=100*100*100 --visualize``        |  ``--size=100*100*1000 --visualize``      |  
+-------------------------------------------+-------------------------------------------+-------------------------------------------+
| .. image:: _static/heat_equation_0001.png | .. image:: _static/heat_equation_0100.png | .. image:: _static/heat_equation_1000.png |
+-------------------------------------------+-------------------------------------------+-------------------------------------------+

See :ref:`heat_equation` for a variation of the benchmark that also computes convergence criteria.
