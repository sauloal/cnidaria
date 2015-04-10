mkdir Drosophila_melanogaster
cd Drosophila_melanogaster
wget ftp://ftp.ncbi.nih.gov/genomes/Drosophila_melanogaster/RELEASE_5_48/CHR_{2,3,4,Un,X}/*.fna
wget ftp://ftp.ncbi.nih.gov/genomes/Drosophila_melanogaster/RELEASE_5_48/CHR_{2,3,4,Un,X}/*.fna.tgz
tar xvf *.tgz
cat *.fna > ../Drosophila_melanogaster.fasta
