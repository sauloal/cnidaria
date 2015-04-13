set -xeu
SPP=Candida_albicans_uid14005
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/Fungi/Candida_albicans_uid14005/
if [[ -f "$SPP.fasta" ]]; then exit 0; fi
mkdir -p $SPP
cd $SPP
wget ${PREFIX}*.fna
cat *.fna > ../$SPP.fasta
