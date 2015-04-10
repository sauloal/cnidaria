SPP=Kluyveromyces_lactis_NRRL_Y-1140_uid12377
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/Fungi/Kluyveromyces_lactis_NRRL_Y-1140_uid12377/
mkdir $SPP
cd $SPP
wget ${PREFIX}*.fna
cat *.fna > ../$SPP.fasta
