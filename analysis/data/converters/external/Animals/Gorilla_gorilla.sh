SPP=Gorilla_gorilla
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/Gorilla_gorilla/Assembled_chromosomes/seq/ggo_ref_gorGor3.1_
mkdir $SPP
cd $SPP
wget ${PREFIX}*.fa.gz
gunzip -kc *.gz > ../$SPP.fasta
