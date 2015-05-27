set -xeu
SPP=Aspergillus_fumigatus_uid14003
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/Fungi/Aspergillus_fumigatus_uid14003/
if [[ -f "$SPP.fasta" ]]; then exit 0; fi
mkdir -p $SPP
cd $SPP
wget ${PREFIX}*.fna
cat *.fna > ../$SPP.fasta