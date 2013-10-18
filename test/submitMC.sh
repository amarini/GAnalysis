#!/bin/bash

mkdir -p $PWD/log
rm $PWD/logMC*.txt || true

for i in `seq 0 100` ; do
bsub -q 1nd -o $PWD/log/logMC_$i.txt <<EOF
cd $PWD
export SCRAM_ARCH=slc5_amd64_gcc462
eval \`scramv1 runtime -sh\`
echo "*** MC ***"
python python/step1_makeHisto.py --inputDat=data/configMC.dat --nJobs=100 --jobId=$i

echo "************************"
echo "*          DONE        *"
echo "************************"

EOF

done

