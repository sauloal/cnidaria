set -xeu
SPP=Candida_dubliniensis_CD36_uid38659
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/Fungi/Candida_dubliniensis_CD36_uid38659/
if [[ -f "$SPP.fasta" ]]; then exit 0; fi
mkdir -p $SPP
cd $SPP
wget ${PREFIX}*.fna
cat *.fna > ../$SPP.fasta