set -xeu
SPP=Aspergillus_nidulans_FGSC_A4_uid13961
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/Fungi/Aspergillus_nidulans_FGSC_A4_uid13961/
if [[ -f "$SPP.fasta" ]]; then exit 0; fi
mkdir -p $SPP
cd $SPP
wget --no-clobber --continue --timeout=5 --tries=2 --random-wait ${PREFIX}*.fna
cat *.fna > ../$SPP.fasta