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
rm -v log/logHLT_*.txt || true
rm -v log/logHLT_*.txt.gz || true
rm -v log/logHLT_*.log || true
rm -v log/logHLT_*.done || true
rm -v log/logHLT_*.fail || true

for i in `seq 0 100` ; do
bsub -q 8nh -o $PWD/log/logHLT_$i.log <<EOF
cd $PWD
export SCRAM_ARCH=slc5_amd64_gcc462
eval \`scramv1 runtime -sh\`
rm $PWD/log/log_$i.done || true
python python/step1_makeHisto.py --inputDat=data/configHLT.dat --nJobs=100 --jobId=$i 2>&1 | gzip > $PWD/log/logHLT_$i.txt.gz && touch $PWD/log/logHLT_$i.done || { touch $PWD/log/logHLT_$i.fail ; exit 1; }

echo "************************"
echo "*          DONE        *"
echo "************************"

EOF

done

rm -v log/logHLTMC_*.txt || true
rm -v log/logHLTMC_*.txt.gz || true
rm -v log/logHLTMC_*.log || true
rm -v log/logHLTMC_*.done || true

for i in `seq 0 100` ; do
bsub -q 8nh -o $PWD/log/logHLTMC_$i.log <<EOF
cd $PWD
export SCRAM_ARCH=slc5_amd64_gcc462
eval \`scramv1 runtime -sh\`
rm $PWD/log/log_$i.done || true
python python/step1_makeHisto.py --inputDat=data/configHLTMC.dat --nJobs=100 --jobId=$i 2>&1 | gzip >  $PWD/log/logHLTMC_$i.txt.gz  && touch $PWD/log/logHLTMC_$i.done || { touch $PWD/log/logHLTMC_$i.fail ;exit 1; }

echo "************************"
echo "*          DONE        *"
echo "************************"

EOF

done

cd $RCWD
