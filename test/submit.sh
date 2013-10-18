#!/bin/bash

mkdir -p $PWD/log
rm log/log_*.txt || true

for i in `seq 0 100` ; do
bsub -q 1nd -o $PWD/log/log_$i.txt <<EOF
cd $PWD
export SCRAM_ARCH=slc5_amd64_gcc462
eval \`scramv1 runtime -sh\`
python python/step1_makeHisto.py --inputDat=data/config.dat --nJobs=100 --jobId=$i

echo "************************"
echo "*          DONE        *"
echo "************************"

EOF

done

