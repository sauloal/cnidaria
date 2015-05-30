find . -name '*.bam'                                                     | sort | xargs -P 5 -n 1 jf_from_bam.sh
find . -name '*.cram'                                                    | sort | xargs -P 5 -n 1 jf_from_cram.sh
find . -name "*.fa" -o -name "*.fasta" -o -name "*.fas" -o -name "*.seq" | sort | xargs -P 5 -n 1 jf_from_fasta.sh
find . -name "*.fq" -o -name "*.fastq"                                   | sort | xargs -P 5 -n 1 jf_from_fastq.sh

