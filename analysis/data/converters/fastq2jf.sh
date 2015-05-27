#!/bin/bash

#find . -name "*.fastq" -o -name "*.fq"  | sort | xargs -P 5 -n 1 ./fastq2jf.sh


set -xeu

INFILE=$1

source jopts

JF=$INFILE.$MER_SIZE.jf
#JELLYFISH=/home/aflit001/dev/phylogenomics2/jellyfish
#MER_SIZE=31
#HASH_SIZE=100000
#COUNTER_LEN=1
#OUT_COUNTER_LEN=1

source jopts

if [[ ! -f "${JF}" ]]; then
    echo "CONVERTING $INFILE TO ${JF}"

    TMP=${JF}.tmp

    if [[ -f "${TMP}" ]]; then
        rm ${TMP}
    fi

    #${JELLYFISH} count -m ${MER_SIZE} -s ${HASH_SIZE} --counter-len=${COUNTER_LEN} --out-counter-len=${OUT_COUNTER_LEN} --canonical -o ${TMP} ${INFILE} && mv ${TMP} ${JF}
    ${JCMD} -o ${TMP} --timing=${JF}.timming ${INFILE} && mv ${TMP} ${JF}

else
    echo "INFILE $INFILE ALREADY CONVERTED TO ${JF}"

fi
