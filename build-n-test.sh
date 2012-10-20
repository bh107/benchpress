#
# This file is part of cphVB and copyright (c) 2012 the cphVB team:
# http://cphvb.bitbucket.org
#
# cphVB is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as 
# published by the Free Software Foundation, either version 3 
# of the License, or (at your option) any later version.
# 
# cphVB is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the 
# GNU Lesser General Public License along with cphVB. 
#
# If not, see <http://www.gnu.org/licenses/>.
#

#
#   This script clones, compiles, installs, tests and benchmarks cphvb.
#   Another script produces graphs based on the results produced in this script.
#
[[ $BUILD_ROOT ]] && echo "** Benchmarking" || (echo "Exiting, you must run via bootstrap.sh"; exit)

cd $BUILD_ROOT

OLDPP=$PYTHONPATH
OLDLD=$LD_LIBRARY_PATH
PYTHONVER=`python -c 'import sys; (major,minor, _,_,_) = sys.version_info; print "%d.%d" % (major, minor)'`
START=`date`

SKIP_PURGE="0" 
SKIP_UPDATE="0"

if [ -z "$CPHVB_BRANCH" ]; then
    CPHVB_BRANCH="master"
fi

#
#   GRAB THE LATEST AND GREATEST
#
if [ "$SKIP_PURGE" != "1" ]
then
  echo "Grabbing repos $1"
  cd $BUILD_ROOT
  rm -rf $CPHVB_LIB
  rm -rf $CPHVB_SRC

  mkdir $CPHVB_LIB
  git clone git@bitbucket.org:cphvb/cphvb.git $CPHVB_SRC
  cd $CPHVB_SRC
  git submodule init
  git checkout $CPHVB_BRANCH
fi

if [ "$SKIP_UPDATE" != "1" ]
then
  cd $CPHVB_SRC
  git checkout $CPHVB_BRANCH
  echo "Updating repos."
  git submodule update
  git pull
fi

#
#   BUILD AND INSTALL
#
cd $CPHVB_SRC
REV=`git log --format=%H -n 1`

echo "** Rebuilding cphVB"
python build.py rebuild

echo "** Installing cphVB"
python build.py install --prefix="$CPHVB_LIB"

echo "** Testing cphVB installation."

export PYTHONPATH="$PYTHONPATH:$CPHVB_LIB/lib/python$PYTHONVER/site-packages"
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:$CPHVB_LIB"
source $BENCH_SRC/envs/$MACHINE.sh
python $CPHVB_SRC/test/numpy/numpytest.py

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
python press.py "$CPHVB_SRC" --output "$BENCH_SRC/results/$MACHINE/$REV" --suite "$SUITE" > "$BENCH_SRC/results/$MACHINE/$MACHINE.log"
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

#
#   Commit & Push benchmark results
#
cd $BENCH_SRC
git pull
git add results/$MACHINE/$MACHINE.log
git add results/$MACHINE/$REV/$BENCHFILE
git add results/$MACHINE/benchmark-latest.json
git commit -m "Results from running '$SUITE' of cphvb rev '$REV' on branch '$CPHVB_BRANCH' on '$MACHINE'."
git push -u origin master

