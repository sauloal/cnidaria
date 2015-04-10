SPP=Cryptococcus_neoformans_var_JEC21_uid10698
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/Fungi/Cryptococcus_neoformans_var_JEC21_uid10698/
mkdir $SPP
cd $SPP
wget ${PREFIX}*.fna
cat *.fna > ../$SPP.fasta
