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
rm -v log/log_unf*.txt || true
rm -v log/logMC_unf*.txt || true
rm -v log/log_fit*.txt || true
rm -v log/logMC_fit*.txt || true

rm -v log/log_unf*.txt.gz || true
rm -v log/logMC_unf*.txt.gz || true
rm -v log/log_fit*.txt.gz || true
rm -v log/logMC_fit*.txt.gz || true

bsub -q 1nd -J FIT_UNF -o $PWD/log/log_submit.txt <<EOF
cd $PWD
export SCRAM_ARCH=slc5_amd64_gcc462
eval \`scramv1 runtime -sh\`
 python python/step2_fit.py --inputDat=data/config.dat --inputDatMC=data/configMC.dat 2>&1 | gzip > log/log_fit.txt.gz ;
 python python/step3_Unfolding.py  --inputDat=data/config.dat --inputDatMC=data/configMC.dat --inputDatMC2=data/configMC_pythia.dat 2>&1 | gzip > log/log_unf.txt.gz
 python test/makeAllPlots.py --inputDat=data/config.dat

echo *********************
echo *      DONE         *
echo *********************
echo "DONE" | mail -c "" -s FIT_UNF amarini@cern.ch
EOF

bsub -q 1nd -J FIT_UNF_MC -o $PWD/log/logMC_submit.txt <<EOF
cd $PWD
export SCRAM_ARCH=slc5_amd64_gcc462
eval \`scramv1 runtime -sh\`
 python python/step2_fit.py --inputDat=data/configMC.dat --inputDatMC=data/configMC.dat 2>&1 | gzip > log/logMC_fit.txt.gz ;
 python python/step3_Unfolding.py --doUnfoldStudies --inputDat=data/configMC.dat --inputDatMC=data/configMC.dat 2>&1 | gzip >log/logMC_unf.txt.gz
 python test/makeAllPlots.py --inputDat=data/configMC.dat

echo *********************
echo *      DONE         *
echo *********************
echo "DONE" | mail -c "" -s FIT_UNF_MC amarini@cern.ch
EOF

rm -v log/logMCpythia_fit*.txt || true
rm -v log/logMCpythia_unf*.txt || true
bsub -q 1nd -J FIT_UNF_MC_PYTHIA -o $PWD/log/logMCpythia_submit.txt <<EOF
cd $PWD
export SCRAM_ARCH=slc5_amd64_gcc462
eval \`scramv1 runtime -sh\`
 python python/step2_fit.py --checkTime --inputDat=data/configMC_pythia.dat --inputDatMC=data/configMC_pythia.dat 2>&1 | gzip > log/logMCpythia_fit.txt.gz ;
 python python/step3_Unfolding.py --inputDat=data/configMC_pythia.dat --inputDatMC=data/configMC_pythia.dat 2>&1 | gzip >log/logMCpythia_unf.txt.gz
 python test/makeAllPlots.py --inputDat=data/configMC_pythia.dat

echo *********************
echo *      DONE         *
echo *********************
echo "DONE" | mail -c "" -s FIT_UNF_MC_PYTHIA amarini@cern.ch
EOF


cd $RCWD
