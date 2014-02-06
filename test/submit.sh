#!/bin/bash
CWD=$PWD
DIR=$0

cd ${DIR%/*}
echo " cd in $PWD"
./submit_main.sh data/config.dat 8nh log_ 100 all
cd $CWD
echo " cd in $PWD"

