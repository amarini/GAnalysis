#!/bin/bash

CWD=$PWD
DIR=$0

LIST=$1
[ "${LIST}" == "" ] && LIST="all"

cd ${DIR%/*}
./submit_main.sh data/configMC.dat 8nh logMC_ 500 $LIST
cd $CWD
exit 0

