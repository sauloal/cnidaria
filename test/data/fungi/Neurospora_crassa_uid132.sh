set -xeu
SPP=Neurospora_crassa_uid132
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/Fungi/Neurospora_crassa_uid132/
if [[ -f "$SPP.fasta" ]]; then exit 0; fi
mkdir -p $SPP
cd $SPP
wget --no-clobber --continue --timeout=5 --tries=2 --random-wait ${PREFIX}*.fna
cat *.fna > ../$SPP.fasta