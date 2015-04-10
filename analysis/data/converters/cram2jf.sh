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

source jopts

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
