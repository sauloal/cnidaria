SPP=Candida_albicans_uid14005
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/Fungi/Candida_albicans_uid14005/
mkdir $SPP
cd $SPP
wget ${PREFIX}*.fna
cat *.fna > ../$SPP.fasta
