set -xeu
SPP=Cryptococcus_neoformans_var_JEC21_uid10698
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/Fungi/Cryptococcus_neoformans_var_JEC21_uid10698/
if [[ -f "$SPP.fasta" ]]; then exit 0; fi
mkdir -p $SPP
cd $SPP
wget --no-clobber --continue --timeout=5 --tries=2 --random-wait ${PREFIX}*.fna
cat *.fna > ../$SPP.fasta
