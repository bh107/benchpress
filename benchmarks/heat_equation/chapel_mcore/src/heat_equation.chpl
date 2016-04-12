//The format of 'size' is two integers separated with a '*'.
//The first integer is the domain size squired and the second integer is
//the number of iterations.
config const size = "100*10";//Default, 100 by 100 domain and 10 iterations
config const epsilon = 1.0e-10;//Stop condition in amount of change

//Parse the --size argument into 'n' and 'iterations'
use Regexp;
const arg = size.matches(compile("(\\d+)*(\\d+)"));
const n = size.substring(arg[1][1]) : int;
const iterations = size.substring(arg[2][1]) : int;

//Initiate a Timer object
use Time;
var timer : Timer;

//Now, let's implement the heat equation!

//A n+2 by n+2 domain.
const Grid = {0..n+1, 0..n+1};

//A n by n domain that represents the interior of 'Grid'
const Interior = {1..n, 1..n};

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

  //When 'delta' is smaller than 'epsilon' the calculation has converged
  iter_count += 1;
} while (delta > epsilon && iter_count >= iterations);

timer.stop();
writeln("Heat Equation (single machine) - n: ",n,
        ", iterations: ", iterations,
        ", elapsed-time: ", timer.elapsed(), " seconds");


