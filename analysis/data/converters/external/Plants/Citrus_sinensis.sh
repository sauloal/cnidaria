mkdir Citrus_sinensis
cd Citrus_sinensis
wget ftp://ftp.ncbi.nih.gov/genomes/Citrus_sinensis/Assembled_chromosomes/seq/csi_ref_Csi_valencia_1.0_*.fa.gz
gunzip -kc *.gz > ../Citrus_sinensis.fasta
