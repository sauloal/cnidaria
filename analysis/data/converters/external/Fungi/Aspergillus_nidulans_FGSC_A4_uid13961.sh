SPP=Aspergillus_nidulans_FGSC_A4_uid13961
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/Fungi/Aspergillus_nidulans_FGSC_A4_uid13961/
mkdir $SPP
cd $SPP
wget ${PREFIX}*.fna
cat *.fna > ../$SPP.fasta
