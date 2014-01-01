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
rm -v log/logMC*.txt || true
rm -v log/logMC_*.txt.gz || true
rm -v log/logMC_*.log || true
rm -v log/logMC_*.done || true
rm -v log/logMC_*.fail || true

for i in `seq 0 500` ; do
bsub -q 1nd -J Job_MC_$i -o $PWD/log/logMC_$i.log <<EOF
cd $PWD
export SCRAM_ARCH=slc5_amd64_gcc462
eval \`scramv1 runtime -sh\`
echo "*** MC ***"
rm $PWD/log/logMC_$i.done || true
python python/step1_makeHisto.py --inputDat=data/configMC.dat --nJobs=500 --jobId=$i 2>&1 | gzip >$PWD/log/logMC_$i.txt.gz ;
declare -a PS=${PIPESTATUS[@]} ;
[ "${PS[0]}" == "0" ] && touch $PWD/log/logMC_$i.done || { touch $PWD/log/logMC_$i.fail; exit 1; }

echo "************************"
echo "*          DONE        *"
echo "************************"

EOF

done

cd $RCWD
