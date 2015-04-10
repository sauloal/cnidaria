find . -name '*.bam'  | sort | xargs -P  5 -n 1 ./bam2jf.sh
find . -name '*.cram' | sort | xargs -P  5 -n 1 ./cram2jf.sh
find . -name "*.fa" -o -name "*.fasta" -o -name "*.fas" -o -name "*.seq" | sort | xargs -P 5 -n 1 ./fasta2jf.sh

