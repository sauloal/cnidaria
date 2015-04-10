SPP=Neurospora_crassa_uid132
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/Fungi/Neurospora_crassa_uid132/
mkdir $SPP
cd $SPP
wget ${PREFIX}*.fna
cat *.fna > ../$SPP.fasta
