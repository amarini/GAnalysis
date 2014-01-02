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
rm -v log/log_*.txt || true
rm -v log/log_*.txt.gz || true
rm -v log/log_*.log || true
rm -v log/log_*.done || true
rm -v log/log_*.fail || true

for i in `seq 0 100` ; do
bsub -q 8nh -J Job_$i -o $PWD/log/log_$i.log <<EOF
cd $PWD
export SCRAM_ARCH=slc5_amd64_gcc462
eval \`scramv1 runtime -sh\`
rm $PWD/log/log_$i.done || true
python python/step1_makeHisto.py --inputDat=data/config.dat --nJobs=100 --jobId=$i 2>&1 | gzip > $PWD/log/log_$i.txt.gz 
[ "${PIPESTATUS[0]}" == "0" ] && touch $PWD/log/log_$i.done || { touch $PWD/log/log_$i.fail; exit 1; }

echo "************************"
echo "*          DONE        *"
echo "************************"

EOF

done


cd $RCWD
