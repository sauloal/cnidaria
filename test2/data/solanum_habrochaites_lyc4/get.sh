wget -q -O - ftp://ftp.sra.ebi.ac.uk/vol1/fastq/ERR410/ERR410237/ERR410237_1.fastq.gz | gunzip -c | head -400000 | pigz -1c > 1.fq.gz
wget -q -O - ftp://ftp.sra.ebi.ac.uk/vol1/fastq/ERR410/ERR410237/ERR410237_2.fastq.gz | gunzip -c | head -400000 | pigz -1c > 2.fq.gz
