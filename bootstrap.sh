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

if [ ! -d "$BENCH_SRC" ]; then
    git clone git@bitbucket.org:cphvb/benchpress.git $BENCH_SRC
fi

cd $BENCH_SRC
git pull
source $BENCH_SRC/build-n-test.sh
