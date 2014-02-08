#!/bin/bash

CWD=$PWD
DIR=$0

LIST=$1
[ "${LIST}" == "" ] && LIST="all"
cd ${DIR%/*}
./submit_main.sh data/configMC_pythia.dat 2nd logMCpythia_ 200 ${LIST}
cd $CWD
exit 0

