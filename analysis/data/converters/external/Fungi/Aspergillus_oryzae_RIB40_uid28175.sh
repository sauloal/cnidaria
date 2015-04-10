SPP=Aspergillus_oryzae_RIB40_uid28175
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/Fungi/Aspergillus_oryzae_RIB40_uid28175/
mkdir $SPP
cd $SPP
wget ${PREFIX}*.fna
cat *.fna > ../$SPP.fasta
