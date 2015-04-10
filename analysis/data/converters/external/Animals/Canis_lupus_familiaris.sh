mkdir Canis_lupus_familiaris
cd Canis_lupus_familiaris/
wget ftp://ftp.ncbi.nih.gov/genomes/Canis_lupus_familiaris/Assembled_chromosomes/seq/cfa_ref_CanFam3.1_chr*.fa.gz
wget ftp://ftp.ncbi.nih.gov/genomes/Canis_lupus_familiaris/Assembled_chromosomes/seq/cfa_ref_CanFam3.1_unplaced.fa.gz
gunzip -kc *.gz > ../Canis_lupus_familiaris.fasta

