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
rm log/logHLT_*.txt || true

for i in `seq 0 100` ; do
bsub -q 8nh -o $PWD/log/logHLT_$i.txt <<EOF
cd $PWD
export SCRAM_ARCH=slc5_amd64_gcc462
eval \`scramv1 runtime -sh\`
rm $PWD/log/log_$i.done || true
python python/step1_makeHisto.py --inputDat=data/configHLT.dat --nJobs=100 --jobId=$i && touch $PWD/log/logHLT_$i.done || exit 1

echo "************************"
echo "*          DONE        *"
echo "************************"

EOF

done

rm log/logHLTMC_*.txt || true

for i in `seq 0 100` ; do
bsub -q 8nh -o $PWD/log/logHLTMC_$i.txt <<EOF
cd $PWD
export SCRAM_ARCH=slc5_amd64_gcc462
eval \`scramv1 runtime -sh\`
rm $PWD/log/log_$i.done || true
python python/step1_makeHisto.py --inputDat=data/configHLTMC.dat --nJobs=100 --jobId=$i && touch $PWD/log/logHLTMC_$i.done || exit 1

echo "************************"
echo "*          DONE        *"
echo "************************"

EOF

done

cd $RCWD
