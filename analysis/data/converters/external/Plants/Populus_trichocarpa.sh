SPP=Populus_trichocarpa
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/Populus_trichocarpa/
mkdir $SPP
cd $SPP
wget ${PREFIX}LG{I,II,III,IV,V,VI,VII,VIII,IX,X,XI,XII,XIII,XIV,XV,XVI,XVII,XVIII,XIX}/*.fna
cat *.fna > ../$SPP.fasta
