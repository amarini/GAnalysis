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
rm -v log/logHLT_unf*.txt || true
rm -v log/logHLTMC_unf*.txt || true
rm -v log/logHLT_fit*.txt || true
rm -v log/logHLTMC_fit*.txt || true

rm -v log/logHLT_unf*.txt.gz || true
rm -v log/logHLTMC_unf*.txt.gz || true
rm -v log/logHLT_fit*.txt.gz || true
rm -v log/logHLTMC_fit*.txt.gz || true

bsub -q 1nd -o $PWD/log/log_submit.txt <<EOF
cd $PWD
export SCRAM_ARCH=slc5_amd64_gcc462
eval \`scramv1 runtime -sh\`
 python python/step2_fit.py --inputDat=data/configHLT.dat --inputDatMC=data/configHLTMC.dat 2>&1 | gzip> log/logHLT_fit.txt.gz ;
 python python/step3_Unfolding.py --doUnfoldStudies --inputDat=data/configHLT.dat --inputDatMC=data/configHLTMC.dat 2>&1| gzip> log/logHLT_unf.txt.gz
 python test/makeAllPlots.py --inputDat=data/configHLT.dat

echo *********************
echo *      DONE         *
echo *********************
EOF

bsub -q 1nd -o $PWD/log/logMC_submit.txt <<EOF
cd $PWD
export SCRAM_ARCH=slc5_amd64_gcc462
eval \`scramv1 runtime -sh\`
 python python/step2_fit.py --inputDat=data/configHLTMC.dat --inputDatMC=data/configHLTMC.dat 2>&1 | gzip > log/logHLTMC_fit.txt.gz ;
 python python/step3_Unfolding.py --doUnfoldStudies --inputDat=data/configHLTMC.dat --inputDatMC=data/configHLTMC.dat 2>&1 | gzip >log/logHLTMC_unf.txt.gz
 python test/makeAllPlots.py --inputDat=data/configHLTMC.dat

echo *********************
echo *      DONE         *
echo *********************
EOF


cd $RCWD
