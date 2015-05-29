set -xeu
SPP=Candida_glabrata
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/Fungi/Candida_glabrata/
if [[ -f "$SPP.fasta" ]]; then exit 0; fi
mkdir -p $SPP
cd $SPP
wget --no-clobber --continue --timeout=60 --tries=2 --random-wait ${PREFIX}*.fna
cat *.fna > ../$SPP.fasta
