SPP=Aspergillus_fumigatus_uid14003
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/Fungi/Aspergillus_fumigatus_uid14003/
mkdir $SPP
cd $SPP
wget ${PREFIX}*.fna
cat *.fna > ../$SPP.fasta
