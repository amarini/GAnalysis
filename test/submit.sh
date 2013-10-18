#!/bin/bash

CWD=$PWD
RCWD=$PWD

while(true);do
	TMP_CWD=${CWD##*/}
	[ "${TMP_CWD}" == "GAnalysis" ] && break;
	[ "${TMP_CWD}" == "" ] && echo "No GAnalysis directory on the top of $PWD" && exit 0 
	CWD=${CWD%/*}
done

echo "Analysis base Dir=$CWD"
cd $CWD

mkdir -p $PWD/log
rm log/log_*.txt || true

for i in `seq 0 100` ; do
bsub -q 1nd -o $PWD/log/log_$i.txt <<EOF
cd $PWD
export SCRAM_ARCH=slc5_amd64_gcc462
eval \`scramv1 runtime -sh\`
rm $PWD/log/log_$i.done || true
python python/step1_makeHisto.py --inputDat=data/config.dat --nJobs=100 --jobId=$i && touch $PWD/log/log_$i.done

echo "************************"
echo "*          DONE        *"
echo "************************"

EOF

done


cd $RCWD
