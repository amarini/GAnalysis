#!/bin/bash

CWD=$PWD
DIR=$0

cd ${DIR%/*}
./submit_main.sh data/configMC.dat 1nd logMC_ 500 all
cd $CWD
exit 0

##### old

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

for i in `seq 0 500` ; do
bsub -q 1nd -J Job_MC_$i -o $PWD/log/logMC_$i.log <<EOF
cd $PWD
export SCRAM_ARCH=slc5_amd64_gcc462
eval \`scramv1 runtime -sh\`
rm -v log/logMC_${i}.txt || true
rm -v log/logMC_${i}.txt.gz || true
rm -v log/logMC_${i}.log || true
rm -v log/logMC_${i}.done || true
rm -v log/logMC_${i}.fail || true
echo "*** MC ***"
python python/step1_makeHisto.py --inputDat=data/configMC.dat --nJobs=500 --jobId=$i 2>&1 | gzip >$PWD/log/logMC_$i.txt.gz ;
[ "${PIPESTATUS[0]}" == "0" ] && touch $PWD/log/logMC_$i.done || { touch $PWD/log/logMC_$i.fail; exit 1; }

echo "************************"
echo "*          DONE        *"
echo "************************"

EOF

done

cd $RCWD
