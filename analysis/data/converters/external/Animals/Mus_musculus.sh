SPP=Mus_musculus
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/Mus_musculus/Assembled_chromosomes/seq/mm_ref_GRCm38.p2
mkdir $SPP
cd $SPP
wget ${PREFIX}*.fa.gz
gunzip -kc *.gz > ../$SPP.fasta
