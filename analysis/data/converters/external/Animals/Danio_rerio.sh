mkdir Danio_rerio
cd Danio_rerio
wget ftp://ftp.ncbi.nih.gov/genomes/D_rerio/Assembled_chromosomes/seq/dr_ref_Zv9_*.fa.gz
gunzip -kc *.gz > ../Danio_rerio.fasta
