#
# This file is part of Bohrium and copyright (c) 2012 the Bohrium team:
# http://bohrium.bitbucket.org
#
# Bohrium is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as 
# published by the Free Software Foundation, either version 3 
# of the License, or (at your option) any later version.
# 
# Bohrium is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the 
# GNU Lesser General Public License along with Bohrium. 
#
# If not, see <http://www.gnu.org/licenses/>.
#

#
#   This script clones, compiles, installs, tests and benchmarks Bohrium.
#   Another script produces graphs based on the results produced in this script.
#
[[ $BUILD_ROOT ]] && echo "** Benchmarking" || (echo "Exiting, you must run via bootstrap.sh"; exit)

cd $BUILD_ROOT

OLDPP=$PYTHONPATH
OLDLD=$LD_LIBRARY_PATH
OLDDYLD=$DYLD_LIBRARY_PATH

PYTHONVER=`python -c 'import sys; (major,minor, _,_,_) = sys.version_info; print "%d.%d" % (major, minor)'`
START=`date`

if [ -z "$SKIP_PURGE" ]; then
    SKIP_PURGE="0" 
fi

if [ -z "$SKIP_PURGE" ]; then
    SKIP_UPDATE="0"
fi

source $BENCH_SRC/envs/$MACHINE.sh

if [ -z "$BOHRIUM_BRANCH" ]; then
    BOHRIUM_BRANCH="master"
fi

if [ -z "$SUITE" ]; then
    SUITE="default"
fi

if [ -z "$RUNS" ]; then
    RUNS="5"
fi

if [ -z "$PARALLEL" ]; then
    PARALLEL="1"
fi

#
#   GRAB THE LATEST AND GREATEST
#
if [ "$SKIP_PURGE" != "1" ]
then
  echo "Grabbing repos $1 on branch '$BOHRIUM_BRANCH'."
  cd $BUILD_ROOT
  rm -rf $BOHRIUM_LIB
  rm -rf $BOHRIUM_SRC

  mkdir $BOHRIUM_LIB
  git clone git@bitbucket.org:bohrium/bohrium.git $BOHRIUM_SRC
  cd $BOHRIUM_SRC
  git checkout $BOHRIUM_BRANCH
  git submodule init
fi

if [ "$SKIP_UPDATE" != "1" ]
then
  cd $BOHRIUM_SRC
  git checkout $BOHRIUM_BRANCH
  echo "Updating repos."
  git submodule update
  git pull
fi

#
#   BUILD AND INSTALL
#
cd $BOHRIUM_SRC
REV=`git log --format=%H -n 1`

echo "** Rebuilding Bohrium"
python build.py rebuild

echo "** Installing Bohrium"
python build.py install --prefix="$BOHRIUM_LIB"

echo "** Testing Bohrium installation."

export PYTHONPATH="$PYTHONPATH:$BOHRIUM_LIB/lib/python$PYTHONVER/site-packages"
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:$BOHRIUM_LIB"
export DYLD_LIBRARY_PATH="$DYLD_LIBRARY_PATH:$BOHRIUM_LIB"

# Make sure we test with simple, as the others may be broken
# or missing
python $BENCH_SRC/select_ve.py simple

python $BOHRIUM_SRC/test/numpy/numpytest.py

RETURN=$?
if [ $RETURN -ne 0 ]; then
  echo "!!!EXITING: Something is wrong with the installation."
  exit
fi

#
#   BENCHMARK-SUITE
#
cd $BENCH_SRC

echo "** Running benchmarks"
mkdir -p "$BENCH_SRC/results/$MACHINE/$REV"
python press.py "$BOHRIUM_SRC" --runs "$RUNS" --output "$BENCH_SRC/results/$MACHINE/$REV" --suite "$SUITE" --parallel "$PARALLEL" > "$BENCH_SRC/results/$MACHINE/$MACHINE.log"
cd "$BENCH_SRC/results/$MACHINE/$REV"
BENCHFILE=`ls -t1 benchmark-* | head -n1`

echo "** Copying results."
cp "$BENCH_SRC/results/$MACHINE/$REV/$BENCHFILE" "$BENCH_SRC/results/$MACHINE/benchmark-latest.json"

RETURN=$?
if [ $RETURN -ne 0 ]; then
  echo "!!!EXITING: Something went wrong while bencmarking."
  exit
fi

export PYTHONPATH=$OLDPP
export LD_LIBRARY_PATH=$OLDLD
export DYLD_LIBRARY_PATH=$OLDDYLD

#
#   Commit & Push benchmark results
#
cd $BENCH_SRC
git pull
git add results/$MACHINE/$MACHINE.log
git add results/$MACHINE/$REV/$BENCHFILE
git add results/$MACHINE/benchmark-latest.json
git commit -m "Results from running '$SUITE' of Bohrium rev '$REV' on branch '$BOHRIUM_BRANCH' on '$MACHINE'."
git push -u origin master

