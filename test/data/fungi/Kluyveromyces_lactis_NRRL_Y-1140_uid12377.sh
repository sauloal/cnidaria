set -xeu
SPP=Kluyveromyces_lactis_NRRL_Y-1140_uid12377
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/Fungi/Kluyveromyces_lactis_NRRL_Y-1140_uid12377/
if [[ -f "$SPP.fasta" ]]; then exit 0; fi
mkdir -p $SPP
cd $SPP
wget --no-clobber --continue --timeout=5 --tries=2 --random-wait ${PREFIX}*.fna
cat *.fna > ../$SPP.fasta