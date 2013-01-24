#!/usr/bin/env bash
#
# This file is part of Bohrium and copyright (c) 2013 the Bohrium team:
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
# Modify the lines below to reflect the local environment. 
#
MACHINE="unknown"
BUILD_ROOT="$HOME/buildbot"
BENCH_SRC="$BUILD_ROOT/benchpress"
BOHRIUM_SRC="$BUILD_ROOT/bohrium"
BOHRIUM_LIB="$BUILD_ROOT/bohrium.lib"
SUITE="default"
BOHRIUM_BRANCH="master"

#
# Do not modify anything beow this line.
# Unless you want to change the bootstrap-script...
#
if [ "$MACHINE" == "unknown" ]; then
    echo "Please set the MACHINE variable, and make sure that the other variables are sane."
    exit
fi

if [ ! -d "$BENCH_SRC" ]; then
    git clone git@bitbucket.org:bohrium/benchpress.git $BENCH_SRC
fi

cd $BENCH_SRC
git pull
source $BENCH_SRC/build-n-test.sh
