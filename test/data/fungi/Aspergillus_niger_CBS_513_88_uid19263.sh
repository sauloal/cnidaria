set -xeu
SPP=Aspergillus_niger_CBS_513_88_uid19263
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/Fungi/Aspergillus_niger_CBS_513_88_uid19263/
if [[ -f "$SPP.fasta" ]]; then exit 0; fi
mkdir -p $SPP
cd $SPP
wget --no-clobber --continue --timeout=60 --tries=2 --random-wait ${PREFIX}*.fna
cat *.fna > ../$SPP.fasta
