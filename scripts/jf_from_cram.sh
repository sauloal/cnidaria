#!/bin/bash

#find . -name '*.cram' | sort | xargs -P 5 -n 1 jf_from_cram.sh

set -xeu

INFILE=$1

SCRIPT_PATH=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
source ${SCRIPT_PATH}/jf_opts

JF=$INFILE.$MER_SIZE.jf

if [[ ! -f "${JF}" ]]; then
    echo "CONVERTING $INFILE TO ${JF}"

    TMP=${JF}.tmp
    FA=${JF}.cfa

    if [[ -f "${TMP}" ]]; then
        rm ${TMP}
    fi

    if [[ -e "${FA}" ]]; then
        rm ${FA}
    fi


    #mkfifo ${FA}

#    $SAMTOOLS view -h $INFILE | grep -v ^@ | awk '{print "@"$1"\n"$10"\n+\n"$11}' > unmapped/samplename.fastq
    #$SAMTOOLS view -h $INFILE | grep -v ^@ | awk '{print ">"$1"\n"$10"\n"}' > $FA &

    #${JELLYFISH} count -m ${MER_SIZE} -s ${HASH_SIZE} --disk --counter-len=${COUNTER_LEN} --out-counter-len=${OUT_COUNTER_LEN} --canonical -o ${TMP} ${FQ} && mv ${TMP} ${JF}
    ${JCMD} -o ${TMP} --timing=${JF}.timming <($SAMTOOLS view -h $INFILE | grep -v ^@ | awk '{print ">"$1"\n"$10"\n"}') && mv ${TMP} ${JF}

    #rm ${FA}

else
    echo "INFILE $INFILE ALREADY CONVERTED TO ${JF}"

fi
