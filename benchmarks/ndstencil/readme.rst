Creates a `dense` stencil and applies in an N-Dimensional world for I iterations.
The size of the world is cubic matching :math:`size^2`.
Params(size*iterations*dimensions)::

  --size=25*10*1
  --size=25*10*2
  --size=25*10*3
  ...
  --size=25*10*N

It it similar to :ref:`heat_equation` when applying the stencil in two dimensions:

+--------------------------------------------+--------------------------------------------+--------------------------------------------+
| ``--size=16*1*2 --visualize``              | ``--size=16*100*2 --visualize``            |  ``--size=16*1000*2 --visualize``          |  
+--------------------------------------------+--------------------------------------------+--------------------------------------------+
| .. image:: _static/ndstencil_16_0001_2.png | .. image:: _static/ndstencil_16_0100_2.png | .. image:: _static/ndstencil_16_1000_2.png |
+--------------------------------------------+--------------------------------------------+--------------------------------------------+

