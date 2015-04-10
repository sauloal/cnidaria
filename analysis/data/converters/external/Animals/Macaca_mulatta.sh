SPP=Macaca_mulatta
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/Macaca_mulatta/Assembled_chromosomes/seq/mmu_
mkdir $SPP
cd $SPP
wget ${PREFIX}*.fa.gz
gunzip -kc *.gz > ../$SPP.fasta
