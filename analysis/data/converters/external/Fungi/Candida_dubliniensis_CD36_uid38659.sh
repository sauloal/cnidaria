SPP=Candida_dubliniensis_CD36_uid38659
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/Fungi/Candida_dubliniensis_CD36_uid38659/
mkdir $SPP
cd $SPP
wget ${PREFIX}*.fna
cat *.fna > ../$SPP.fasta
