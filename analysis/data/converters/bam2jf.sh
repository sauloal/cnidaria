#!/bin/bash

#find . -name '*.bam' | sort | xargs -P 5 -n 1 ./bam2jf.sh

set -xeu

INFILE=$1

source jopts

JF=$INFILE.$MER_SIZE.jf
#JELLYFISH=/home/aflit001/dev/phylogenomics2/jellyfish
#MER_SIZE=31
#HASH_SIZE=4G
#COUNTER_LEN=1
#OUT_COUNTER_LEN=1


if [[ ! -f "${JF}" ]]; then
    echo "CONVERTING $INFILE TO ${JF}"

    TMP=${JF}.tmp
    FQ=${JF}.bfq

    if [[ -f "${TMP}" ]]; then
        rm ${TMP}
    fi

    if [[ -e "${FQ}" ]]; then
        rm ${FQ}
    fi


    #mkfifo ${FQ}

    #bamToFastq -i ${INFILE} -fq /dev/stdout > ${FQ} &

    #${JELLYFISH} count -m ${MER_SIZE} -s ${HASH_SIZE} --disk --counter-len=${COUNTER_LEN} --out-counter-len=${OUT_COUNTER_LEN} --canonical -o ${TMP} ${FQ} && mv ${TMP} ${JF}
    ${JCMD} -o ${TMP} --timing=${JF}.timming <(bamToFastq -i ${INFILE} -fq /dev/stdout) && mv ${TMP} ${JF}

    #rm ${FQ}

else
    echo "INFILE $INFILE ALREADY CONVERTED TO ${JF}"

fi
