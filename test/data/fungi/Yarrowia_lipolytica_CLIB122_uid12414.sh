set -xeu
SPP=Yarrowia_lipolytica_CLIB122_uid12414
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/Fungi/Yarrowia_lipolytica_CLIB122_uid12414/
if [[ -f "$SPP.fasta" ]]; then exit 0; fi
mkdir -p $SPP
cd $SPP
wget ${PREFIX}*.fna
cat *.fna > ../$SPP.fasta
