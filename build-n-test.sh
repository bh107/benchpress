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
# Modify the lines below to reflect the local environment. 
#
MACHINE="unknown"
BUILD_ROOT="$HOME/buildbot"
BENCH_SRC="$BUILD_ROOT/benchpress"
CPHVB_SRC="$BUILD_ROOT/cphvb"
CPHVB_LIB="$BUILD_ROOT/cphvb.lib"
SUITE="default"

#
# STOP: Do not modify anything below unless you want to change the functionality of the build-n-test script.
#
cd $BUILD_ROOT

OLDPP=$PYTHONPATH
OLDLD=$LD_LIBRARY_PATH
PYTHONVER=`python -c 'import sys; (major,minor, _,_,_) = sys.version_info; print "%d.%d" % (major, minor)'`
START=`date`

SKIP_PURGE="0" 
SKIP_UPDATE="0" 
 
if [ "$1" == "1" ] 
then 
    SKIP_PURGE="1" 
fi 
 
if [ "$2" == "1" ] 
then 
    SKIP_UPDATE="1" 
fi

#
#   GRAB THE LATEST AND GREATEST
#
if [$SKIP_PURGE != "1"]
then
  echo "Grabbing repos $1"
  cd $BUILD_ROOT
  rm -rf $CPHVB_LIB
  rm -rf $CPHVB_SRC
  rm -rf $BENCH_SRC

  mkdir $CPHVB_LIB
  git clone git@bitbucket.org:cphvb/cphvb.git $CPHVB_SRC
  git clone git@bitbucket.org:cphvb/benchpress.git $BENCH_SRC
  cd $CPHVB_SRC
  git submodule init
fi

if [$SKIP_UPDATE != "1"]
then
  cd $CPHVB_SRC
  echo "Updating repos."
  git submodule update
  git pull
  cd $BENCH_SRC
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
python press.py $CPHVB_SRC --output "$BENCH_SRC/results/$MACHINE/$REV" --suite $SUITE > "$BENCH_SRC/$MACHINE.log"
cd "$BENCH_SRC/results/$MACHINE/$REV"
BENCHFILE=`ls -t1 benchmark-* | head -n1`

echo "** Copying results."
cp "$BENCH_SRC/results/$MACHINE/$REV/$BENCHFILE" "$BENCH_SRC/results/$MACHINE/latest.json"

RETURN=$?
if [ $RETURN -ne 0 ]; then
  echo "!!!EXITING: Something went wrong while bencmarking."
  exit
fi


#
#   Commit & Push benchmark results
#
cd $BENCH_SRC
git add $MACHINE.log
git add results/$MACHINE/$REV/$BENCHFILE
git commit -m "Results from running '$SUITE' on '$MACHINE'."
git push -u origin master

#
#   GRAPHS
#
echo "** Generating graphs from $BENCH_SRC/results/$MACHINE/$REV/$BENCHFILE"
export PYTHONPATH=$OLDPP
export LD_LIBRARY_PATH=$OLDLD

mkdir -p $BENCH_SRC/graphs/$MACHINE/$REV
mkdir -p $BENCH_SRC/graphs/$MACHINE/latest
rm $BENCH_SRC/graphs/$MACHINE/latest/*
python "$BENCH_SRC/gen.graphs.py" "$BENCH_SRC/results/$MACHINE/$REV/$BENCHFILE" --output "$BENCH_SRC/graphs/$MACHINE/$REV"
cp "$BENCH_SRC/graphs/$MACHINE/$REV/*" "$BENCH_SRC/graphs/$MACHINE/latest/"

RETURN=$?
if [ $RETURN -ne 0 ]; then
  echo "!!!EXITING: Something went wrong while generating graphs."
  exit
fi

#
#   Commit & Push
#
cd $BENCH_SRC
git add graphs/$MACHINE/$REV/*
git commit -m "Graphs from running '$SUITE' on '$MACHINE'."
git push -u origin master
