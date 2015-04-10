SPP=Candida_glabrata_CBS138_uid12376
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/Fungi/Candida_glabrata_CBS138_uid12376/
mkdir $SPP
cd $SPP
wget ${PREFIX}*.fna
cat *.fna > ../$SPP.fasta
