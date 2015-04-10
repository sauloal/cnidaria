 1293  1410451673 mkdir Canis_familiaris
 1294  1410451675 cd Canis_familiaris/
 1295  1410451686 wget ftp://ftp.ncbi.nih.gov/genomes/Canis_familiaris/Assembled_chromosomes/seq/cfa_ref_CanFam3.1_chr*.fa.gz
 1297  1410452127 wget ftp://ftp.ncbi.nih.gov/genomes/Canis_familiaris/Assembled_chromosomes/seq/cfa_ref_CanFam3.1_unplaced.fa.gz
 1298  1410452147 gunzip -kc *.gz > ../Canis_familiaris.fasta
 1300  1410452211 history | grep is_fa | tee Canis_familiaris.sh
