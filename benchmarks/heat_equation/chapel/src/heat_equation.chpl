//The format of 'size' is two integers separated with a '*'.
//The first integer is the domain size squired and the second integer is
//the number of iterations.
config const size = "100*10";//Default, 100 by 100 domain and 10 iterations

//Stop condition in amount of change (ignored when 'iterations' are non-zero).
config const epsilon = 1.0e-10;

//Parse the --size argument into 'n' and 'iterations'
use Regexp;
const arg = size.matches(compile("(\\d+)*(\\d+)"));
const arg_n = arg[1][1];
const arg_i = arg[2][1];
const n = size[arg_n.offset+1..arg_n.offset+arg_n.length] : int;
const iterations = size[arg_i.offset+1..arg_i.offset+arg_i.length]: int;

//Initiate a Timer object
use Time;
var timer : Timer;

//Now, let's implement the heat equation!

//We will use the Block distribution
use BlockDist;

//A n+2 by n+2 domain.
const Grid = {0..n+1, 0..n+1} dmapped Block({1..n, 1..n});

//A n by n domain that represents the interior of 'Grid'
const Interior = {1..n, 1..n} dmapped Block({1..n, 1..n});

var A, T : [Grid] real;//Zero initialized as default

A[..,0] = -273.15;   //Left column
A[..,n+1] = -273.15; //Right column
A[n+1,..] = -273.15; //Bottom row
A[0,..] = 40.0;      //Top row

timer.start();
var iter_count = 0;
do{
  //Since all iterations are independent, we can use 'forall', which allows
  //the Chapel runtime system to calculate the iterations in parallel
  forall (i,j) in Interior do//Iterate over all non-border cells
  {
    //Assign each cell in 'T' the mean of its neighboring cells in 'A'
    T[i,j] = (A[i,j] + A[i-1,j] + A[i+1,j] + A[i,j-1] + A[i,j+1]) / 5;
  }

  //Delta is the total amount of change done in this iteration
  const delta = + reduce abs(A[Interior] - T[Interior]);

  //Copy back the non-border cells
  A[Interior] = T[Interior];

  iter_count += 1;

  //if 'iterations' is non-zero we stop after a fixed number of iterations
  //otherwise we stop when the calculation has converged, i.e. 'delta' is smaller than 'epsilon'.
  var stop = false;
  if(iterations > 0)
  {
    if iter_count >= iterations then
      stop = true;
  }
  else
  {
    if delta < epsilon then
      stop = true;
  }

} while (!stop);

timer.stop();
writeln("Heat Equation (Chapel) - n: ",n,
        ", iterations: ", iterations,
        ", elapsed-time: ", timer.elapsed(), " seconds");


