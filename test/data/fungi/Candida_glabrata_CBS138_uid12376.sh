set -xeu
SPP=Candida_glabrata_CBS138_uid12376
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/Fungi/Candida_glabrata_CBS138_uid12376/
if [[ -f "$SPP.fasta" ]]; then exit 0; fi
mkdir -p $SPP
cd $SPP
wget --no-clobber --continue --timeout=60 --tries=2 --random-wait ${PREFIX}*.fna
cat *.fna > ../$SPP.fasta
