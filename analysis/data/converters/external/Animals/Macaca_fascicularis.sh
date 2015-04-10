SPP=Macaca_fascicularis
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/Macaca_fascicularis/Assembled_chromosomes/seq/mfa_ref_Macaca_fascicularis_5.0_
mkdir $SPP
cd $SPP
wget ${PREFIX}*.fa.gz
gunzip -kc *.gz > ../$SPP.fasta
