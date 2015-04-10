SPP=Malus_domestica
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/Malus_domestica/Assembled_chromosomes/seq/mdo_ref_MalDomGD1.0_chr
mkdir $SPP
cd $SPP
wget ${PREFIX}*.fa.gz
gunzip -kc *.gz > ../$SPP.fasta
