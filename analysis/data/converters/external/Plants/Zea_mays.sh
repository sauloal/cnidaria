SPP=Zea_mays
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/Zea_mays/Assembled_chromosomes/seq/zm_ref_B73_RefGen_v3_
mkdir $SPP
cd $SPP
wget ${PREFIX}*.fa.gz
gunzip -kc *.gz > ../$SPP.fasta
