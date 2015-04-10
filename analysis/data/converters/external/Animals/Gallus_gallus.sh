SPP=Gallus_gallus
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/Gallus_gallus/Assembled_chromosomes/seq/gga_ref_Gallus_gallus-4.0_
mkdir $SPP
cd $SPP
wget ${PREFIX}*.fa.gz
gunzip -kc *.gz > ../$SPP.fasta
