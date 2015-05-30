#!/bin/bash

#find . -name "*.fa" -o -name "*.fasta" -o -name "*.fas" -o -name "*.seq" | sort | xargs -P 5 -n 1 jf_from_fasta.sh


set -xeu

INFILE=$1

SCRIPT_PATH=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
source ${SCRIPT_PATH}/jf_opts

JF=$INFILE.$MER_SIZE.jf

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
