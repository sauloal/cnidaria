set -xeu
SPP=Aspergillus_oryzae_RIB40_uid28175
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/Fungi/Aspergillus_oryzae_RIB40_uid28175/
if [[ -f "$SPP.fasta" ]]; then exit 0; fi
mkdir -p $SPP
cd $SPP
wget --no-clobber --continue --timeout=60 --tries=2 --random-wait ${PREFIX}*.fna
cat *.fna > ../$SPP.fasta
