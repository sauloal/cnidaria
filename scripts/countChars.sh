#!/bin/bash
set -xeu

infile=$1

EXE=~/dev/phylogenomics4/scripts/countChars
SAMTOOLS=/home/aflit001/dev/phylogenomics4/data/raw/samtools/samtools-1.1/samtools

#find . -name '*.fasta'   | xargs -P 30 -n 1 ~/dev/phylogenomics4/countChars.sh
#find . -name '*.fa'      | xargs -P 30 -n 1 ~/dev/phylogenomics4/countChars.sh
#find . -name '*.seq'     | xargs -P 30 -n 1 ~/dev/phylogenomics4/countChars.sh
#find . -name '*.bam'     | xargs -P 10 -n 1 ~/dev/phylogenomics4/countChars.sh
#find . -name '*.cram'    | xargs -P 10 -n 1 ~/dev/phylogenomics4/countChars.sh


#if [[ ! -f "$EXE" ]]; then
#    echo compiling
#    echo 'unsigned long long int cache[256],x,y;char buf[4096],letters[]="tacgnTAGCN>-"; int main(){while((x=read(0,buf,sizeof buf))>0)for(y=0;y<x;y++)cache[(unsigned)buf[y]]++;for(x=0;x<sizeof letters-1;x++)printf("%c: %llu\n",letters[x],cache[letters[x]]);}' | gcc -march=native -O3 -w -xc -o $EXE -
#    exit 0
#fi

echo running $infile
if [[ ! -f "$infile.stats" ]]; then
    if [[ "$infile" == *bam ]]; then
        echo BAM
        time bamToFastq -i $infile -fq >( tee ) | sed -n '2~4p' | $EXE | tee $infile.stats.tmp
        mv $infile.stats.tmp $infile.stats

        time samtools flagstat sa.fa.bam.filtered.bam

    elif [[ "$infile" == *cram ]]; then
        echo CRAM
        $SAMTOOLS view -h $infile | grep -v ^@ | awk '{print $10}' | $EXE | tee $infile.stats.tmp
        mv $infile.stats.tmp $infile.stats

    else
        echo FASTA
        time $EXE < <(grep -v ">" $infile) | tee $infile.stats.tmp
        mv $infile.stats.tmp $infile.stats
    fi
else
    echo $infile already done
fi

#rm a.out;
