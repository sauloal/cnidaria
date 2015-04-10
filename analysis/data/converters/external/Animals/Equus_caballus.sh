mkdir Equus_caballus
cd Equus_caballus
wget ftp://ftp.ncbi.nih.gov/genomes/Equus_caballus/Assembled_chromosomes/seq/eca_ref_EquCab2.0_*.fa.gz
gunzip -kc *.gz > ../Equus_caballus.fasta
