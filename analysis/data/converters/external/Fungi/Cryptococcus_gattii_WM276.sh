SPP=Cryptococcus_gattii_WM276
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/Fungi/Cryptococcus_gattii_WM276/
mkdir $SPP
cd $SPP
wget ${PREFIX}*.fna
cat *.fna > ../$SPP.fasta
