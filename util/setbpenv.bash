# bash shell script to set environment variables
# needed to run Benchpress out of clone / tarball

# shallow test to see if we are in the correct directory
# Just probe to see if we have a few essential subdirectories --
# indicating that we are probably in a Benchpress root directory.
if [ -d "benchmarks" ] && [ -d "benchpress" ] && [ -d "doc" ] && [ -d "suites" ]
   then
      echo "Updating PATH to include $PWD"
      export PATH="$PWD":"$PATH"

      echo "Updating PYTHONPATH to include $PWD"
      export PYTHONPATH="$PWD":"$PYTHONPATH"
   else
      echo "Error: setbpenv must be sourced from within the Benchpress root directory"
fi
