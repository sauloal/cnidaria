set -xeu
SPP=Zygosaccharomyces_rouxii_CBS_732_uid39573
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/Fungi/Zygosaccharomyces_rouxii_CBS_732_uid39573/
if [[ -f "$SPP.fasta" ]]; then exit 0; fi
mkdir -p $SPP
cd $SPP
wget ${PREFIX}*.fna
cat *.fna > ../$SPP.fasta