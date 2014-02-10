#!/bin/bash

CWD=$PWD

LIST=$(ls *fail | grep  -v pythia | sed 's:logMC_::' | sed 's:.fail::' | while read num ; do bjobs -w | grep "Job_MC_$num\\>" >/dev/null || echo $num ; done | tr '\n' ',' | sed 's:,$::' )

LIST2=$(ls *fail | grep   pythia | sed 's:logMCpythia_::' | sed 's:.fail::' | while read num ; do bjobs -w | grep "Job_MC_pythia_$num\\>" >/dev/null || echo $num ; done | tr '\n' ',' | sed 's:,$::' )

echo "cd ../test"
[ "$LIST"  == "" ] ||  echo "./submitMC.sh $LIST"
[ "$LIST2" == "" ] || echo "./submitMC_pythia.sh $LIST2"

echo "cd $CWD"
