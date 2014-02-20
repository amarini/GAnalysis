#!/bin/bash

CWD=$PWD
DIR=$0

LIST=$1
[ "${LIST}" == "" ] && LIST="all"

cd ${DIR%/*}
./submit_main.sh data/configMC.dat 1nd logMC_ 2000 $LIST
cd $CWD
exit 0

