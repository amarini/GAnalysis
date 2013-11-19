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
rm log/log_unf*.txt || true
rm log/logMC_unf*.txt || true
rm log/log_fit*.txt || true
rm log/logMC_fit*.txt || true


bsub -q 1nd -o $PWD/log/log_submit.txt <<EOF
cd $PWD
export SCRAM_ARCH=slc5_amd64_gcc462
eval \`scramv1 runtime -sh\`
 python python/step2_fit.py --inputDat=data/config.dat --inputDatMC=data/configMC.dat &> log/log_fit.txt ;
 python python/step3_Unfolding.py --doUnfoldStudies --inputDat=data/config.dat --inputDatMC=data/configMC.dat &>log/log_unf.txt
 python test/makeAllPlots.py --inputDat=data/config.dat

echo *********************
echo *      DONE         *
echo *********************
EOF

bsub -q 1nd -o $PWD/log/logMC_submit.txt <<EOF
cd $PWD
export SCRAM_ARCH=slc5_amd64_gcc462
eval \`scramv1 runtime -sh\`
 python python/step2_fit.py --inputDat=data/configMC.dat --inputDatMC=data/configMC.dat &> log/logMC_fit.txt ;
 python python/step3_Unfolding.py --doUnfoldStudies --inputDat=data/configMC.dat --inputDatMC=data/configMC.dat &>log/logMC_unf.txt
 python test/makeAllPlots.py --inputDat=data/configMC.dat

echo *********************
echo *      DONE         *
echo *********************
EOF


cd $RCWD
