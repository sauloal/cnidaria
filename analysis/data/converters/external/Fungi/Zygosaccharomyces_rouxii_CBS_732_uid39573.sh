SPP=Zygosaccharomyces_rouxii_CBS_732_uid39573
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/Fungi/Zygosaccharomyces_rouxii_CBS_732_uid39573/
mkdir $SPP
cd $SPP
wget ${PREFIX}*.fna
cat *.fna > ../$SPP.fasta
