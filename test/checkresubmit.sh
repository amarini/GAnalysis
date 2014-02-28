#!/bin/bash

CWD=$PWD

LIST=$(ls *fail | grep  -v pythia | grep -v log_ | grep -v QCD | sed 's:logMC_::' | sed 's:.fail::' | while read num ; do bjobs -w | grep "Job_MC_$num\\>" >/dev/null || echo $num ; done | tr '\n' ',' | sed 's:,$::' )

LIST2=$(ls *fail | grep   pythia | grep -v log_ | grep -v QCD | sed 's:logMCpythia_::' | sed 's:.fail::' | while read num ; do bjobs -w | grep "Job_MC_pythia_$num\\>" >/dev/null || echo $num ; done | tr '\n' ',' | sed 's:,$::' )

LIST3=$(ls *fail | grep   QCD | sed 's:logMCQCD_::' | sed 's:.fail::' | while read num ; do bjobs -w | grep "QCD_$num\\>" >/dev/null || echo $num ; done | tr '\n' ',' | sed 's:,$::' )

LIST4=$(ls *fail | grep 'log\_'  | sed 's:log_::' | sed 's:.fail::' | while read num ; do bjobs -w | grep "Job_$num\\>" >/dev/null || echo $num ; done | tr '\n' ',' | sed 's:,$::' )

echo "cd ../test"
[ "$LIST"  == "" ] ||  echo "./submitMC.sh $LIST"
[ "$LIST2" == "" ] || echo "./submitMC_pythia.sh $LIST2"
[ "$LIST3" == "" ] || echo "./submitMC_QCD.sh $LIST3"
[ "$LIST4" == "" ] || echo "./submit.sh $LIST4"

echo "cd $CWD"
