#!/bin/bash

CWD=$PWD
RCWD=$PWD

#example
CONFIG=data/config.dat
QUEUE=8nh
LOG=log_
NJOBS=100
LIST=""

CONFIG=$1
QUEUE=$2
LOG=$3
NJOBS=$4
LIST=$5
[ "$LIST" == "all" ] && LIST=""

while(true);do
	TMP_CWD=${CWD##*/}
	[ "${TMP_CWD}" == "GAnalysis" ] && break;
	[ "${TMP_CWD}" == "" ] && echo "No GAnalysis directory on the top of $PWD" && exit 0 
	CWD=${CWD%/*}
done

echo "Analysis base Dir=$CWD"
cd $CWD

mkdir -p $PWD/log


NAME=$(echo -n "${CONFIG}" | sed 's:data/config::'| sed 's:.dat::')
[ "$NAME" != "" ] && NAME="_${NAME}"

[ "${LIST}" == "" ] && LIST=`seq 0 ${NJOBS}` 
LIST=$(echo -n "${LIST}" | tr ',' ' ')

for i in ${LIST} ; do
bsub -q ${QUEUE} -J Job${NAME}_$i -o $PWD/log/${LOG}$i.log <<EOF
cd $PWD
rm -v log/${LOG}${i}.txt || true
rm -v log/${LOG}${i}.txt.gz || true
rm -v log/${LOG}${i}.log || true
rm -v log/${LOG}${i}.done || true
rm -v log/${LOG}${i}.fail || true
export SCRAM_ARCH=slc5_amd64_gcc462
eval \`scramv1 runtime -sh\`
python python/step1_makeHisto.py --inputDat=${CONFIG} --nJobs=${NJOBS} --jobId=$i 2>&1 | gzip > $PWD/log/${LOG}$i.txt.gz 
EXITSTATUS=${PIPESTATUS[0]}
[ "${EXITSTATUS}" == "0" ] && touch $PWD/log/${LOG}$i.done || { echo ${EXITSTATUS}} > $PWD/log/${LOG}$i.fail; exit 1; }

echo "************************"
echo "*          DONE        *"
echo "************************"

EOF

done
cd $RCWD
