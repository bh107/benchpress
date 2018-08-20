Implementation of Conway's Game of Life Conway's, a zero player cellular automaton devised by the John Horton Conway in 1970.

The game has no players, the game is about observing the evolution of the initial state of a collection of cells in a grid.

The game is governed by these rules. Each cell has 2 states: live or dead. There are 4 simple rules that determine this:

 * Any live cell with fewer than two live neighbours dies, as if caused by under-population.
 * Any live cell with two or three live neighbours lives on to the next generation.
 * Any live cell with more than three live neighbours dies, as if by overcrowding.
 * Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

Params::

  height*width*iterations*rules

See below for examples.

+------------------------------------------------+------------------------------------------------+------------------------------------------------+
| ``100*100*1 --visualize``                      | ``100*100*100 --visualize``                    |  ``100*100*1000 --visualize``                  |
+------------------------------------------------+------------------------------------------------+------------------------------------------------+
| .. image:: _static/gameoflife_100_100_0001.png | .. image:: _static/gameoflife_100_100_0100.png | .. image:: _static/gameoflife_100_100_1000.png |
+------------------------------------------------+------------------------------------------------+------------------------------------------------+

