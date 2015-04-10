SPP=Pan_troglodytes
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/Pan_troglodytes/Assembled_chromosomes/seq/ptr_ref_Pan_troglodytes-2.1.4_
mkdir $SPP
cd $SPP
wget ${PREFIX}*.fa.gz
gunzip -kc *.gz > ../$SPP.fasta
