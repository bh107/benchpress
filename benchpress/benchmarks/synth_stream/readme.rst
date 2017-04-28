This synthetic benchmark constructs a streamable expression.

--size=N, I, S

N = Number of elements in the arrays.
I = Number of "trials" / "iterations" to run the expression
S = The generator used, 0 = ones, 1 = range, 2 = random.

Something like::

  --size=10000000*10*0
  --size=10000000*10*1
  --size=10000000*10*2

