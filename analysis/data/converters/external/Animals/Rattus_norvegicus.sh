SPP=Rattus_norvegicus
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/R_norvegicus/Assembled_chromosomes/seq/rn_ref_Rnor_
mkdir $SPP
cd $SPP
wget ${PREFIX}*.fa.gz
gunzip -kc *.gz > ../$SPP.fasta
