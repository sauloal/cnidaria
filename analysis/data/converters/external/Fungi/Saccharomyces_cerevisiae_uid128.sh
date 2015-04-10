SPP=Saccharomyces_cerevisiae_uid128
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/Fungi/Saccharomyces_cerevisiae_uid128/
mkdir $SPP
cd $SPP
wget ${PREFIX}*.fna
cat *.fna > ../$SPP.fasta
