 1242  1410449694 mkdir Bos_taurus
 1243  1410449695 cd Bos_taurus/
 1244  1410449701 wget ftp://ftp.ncbi.nih.gov/genomes/Bos_taurus/Assembled_chromosomes/seq/bt_ref_Bos_taurus_UMD_3.1_chr*.fa.gz
 1251  1410450194 cd ../Bos_taurus/
 1252  1410450199 wget ftp://ftp.ncbi.nih.gov/genomes/Bos_taurus/Assembled_chromosomes/seq/bt_ref_Bos_taurus_UMD_3.1_unplaced.fa.gz
 1253  1410450215 gunzip -kc *.gz > ../Bos_taurus.fasta

