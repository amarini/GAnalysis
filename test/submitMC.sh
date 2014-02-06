#!/bin/bash

CWD=$PWD
DIR=$0

cd ${DIR%/*}
./submit_main.sh data/configMC.dat 1nd logMC_ 200 all
cd $CWD
exit 0

