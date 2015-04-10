SPP=Oryza_brachyantha
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/Oryza_brachyantha/Assembled_chromosomes/seq/obr_ref_Oryza_brachyantha.v1.4b_
mkdir $SPP
cd $SPP
wget ${PREFIX}*.fa.gz
gunzip -kc *.gz > ../$SPP.fasta
