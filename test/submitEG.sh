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
rm -v log/logEG.txt || true
rm -v log/logEG.txt.gz || true
rm -v log/logEG.log || true
rm -v log/logEG.done || true
rm -v log/logEG.fail || true

bsub -q 1nd -o $PWD/log/logEG.log <<EOF
cd $PWD
export SCRAM_ARCH=slc5_amd64_gcc462
eval \`scramv1 runtime -sh\`
python python/step0a_electronFakeSF.py --inputDat=data/config.dat --inputDatMC=data/configMC.dat 2>&1 | gzip > $PWD/log/logEG.txt.gz && touch $PWD/log/logEG.done || { touch $PWD/log/logEG.fail; exit 1; }

echo "************************"
echo "*          DONE        *"
echo "************************"

EOF

cd $RCWD
