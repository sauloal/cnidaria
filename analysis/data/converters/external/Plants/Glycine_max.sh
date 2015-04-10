SPP=Glycine_max
mkdir $SPP
cd $SPP
wget ftp://ftp.ncbi.nih.gov/genomes/Glycine_max/Assembled_chromosomes/seq/gma_ref_V1.1_*.fa.gz
gunzip -kc *.gz > ../$SPP.fasta
