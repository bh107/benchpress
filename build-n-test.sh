# Support for invoking with su
cd ~/buildbot

if [ "$1" == "FULL" ]
then
    echo "Cleaning repo: $1"
    rm -rf cphvb
    rm -rf cphvbbuildgraphs
    git clone git@bitbucket.org:cphvb/cphvb.git
    git clone git@bitbucket.org:cphvb/cphvbbuildgraphs.git
    cd cphvb
    git submodule init
    cd ..
fi

cd cphvb

CURDIR=`pwd`
INSTALLDIR="$CURDIR/test_install"

echo "Pulling updates"
git pull
git submodule update

echo "Rebuilding cphVB"
python build.py rebuild

echo "Installing cphVB"
python build.py install --prefix="$INSTALLDIR"

echo "Running unittest"
OLDPP=$PYTHONPATH
OLDLD=$LD_LIBRARY_PATH
export PYTHONPATH="$INSTALLDIR/lib/python2.6/site-packages":$PYTHONPATH
export LD_LIBRARY_PATH="$INSTALLDIR":$LD_LIBRARY_PATH
python test/numpy/numpytest.py

echo "Running benchmarks"
cd doc/benchpress
python press.py > ../../../cphvbbuildgraphs/log.txt

cd results
BENCHFILE=`ls -t1 benchmark-* | head -n1`
cd ..
echo "Generating diagrams from results/$BENCHFILE"
export PYTHONPATH=$OLDPP
export LD_LIBRARY_PATH=$OLDLD
python gen.diagrams.py "results/$BENCHFILE"

cd ../../../cphvbbuildgraphs
git pull
cp ../cphvb/doc/benchpress/gfx/*speedup.png .
cp "../cphvb/doc/benchpress/results/$BENCHFILE" ./datafile.json

git add .
git commit -m "Daily update"
git push -u origin master

