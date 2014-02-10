#!/bin/bash
CWD=$PWD
DIR=$0

LIST=$1
[ "${LIST}" == "" ] && LIST="all"

cd ${DIR%/*}
echo " cd in $PWD"
./submit_main.sh data/config.dat 8nh log_ 100 ${LIST}
cd $CWD
echo " cd in $PWD"

