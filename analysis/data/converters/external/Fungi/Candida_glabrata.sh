SPP=Candida_glabrata
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/Fungi/Candida_glabrata/
mkdir $SPP
cd $SPP
wget ${PREFIX}*.fna
cat *.fna > ../$SPP.fasta
