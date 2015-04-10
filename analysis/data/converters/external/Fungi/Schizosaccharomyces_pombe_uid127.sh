SPP=Schizosaccharomyces_pombe_uid127
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/Fungi/Schizosaccharomyces_pombe_uid127/
mkdir $SPP
cd $SPP
wget ${PREFIX}*.fna
cat *.fna > ../$SPP.fasta
