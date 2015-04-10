mkdir Caenorhabditis_elegans

cd Caenorhabditis_elegans

wget ftp://ftp.ncbi.nih.gov/genomes/Caenorhabditis_elegans/CHR_{I,II,III,IV,V,X}/*.fna

cat *.fna > ../Caenorhabditis_elegans.fasta

