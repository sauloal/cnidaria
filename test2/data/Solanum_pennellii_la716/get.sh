wget -q -O - ftp://ftp.sra.ebi.ac.uk/vol1/fastq/ERR410/ERR410247/ERR410247_1.fastq.gz | pigz -dc | head -8000000 | pigz -1c > 1.fq.gz
wget -q -O - ftp://ftp.sra.ebi.ac.uk/vol1/fastq/ERR410/ERR410247/ERR410247_2.fastq.gz | pigz -dc | head -8000000 | pigz -1c > 2.fq.gz
