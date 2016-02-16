set -xeu

cd data

function get {
    SPP=$1
    PREFIX=$2
    EXT=$3

    if [[ ! -f "$SPP/$SPP.fasta" ]]; then
        mkdir -p $SPP
        cd $SPP
        wget --no-clobber --continue --timeout=60 --tries=2 --random-wait ${PREFIX}*${EXT}
        gunzip -c *.gz > $SPP.fasta
        rm *.gz
        cd ..
    fi
}

SPP=Aspergillus_fumigatus
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/refseq/fungi/Aspergillus_fumigatus/all_assembly_versions/GCF_000002655.1_ASM265v1/
EXT=_genomic.fna.gz
get $SPP $PREFIX $EXT

SPP=Aspergillus_nidulans
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/refseq/fungi/Aspergillus_nidulans/all_assembly_versions/GCF_000149205.1_ASM14920v1/
get $SPP $PREFIX $EXT

SPP=Aspergillus_niger
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/refseq/fungi/Aspergillus_niger/all_assembly_versions/GCF_000002855.3_ASM285v2/
get $SPP $PREFIX $EXT

SPP=Aspergillus_oryzae
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/refseq/fungi/Aspergillus_oryzae/all_assembly_versions/GCF_000184455.1_ASM18445v1/
get $SPP $PREFIX $EXT

SPP=Candida_dubliniensis
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/refseq/fungi/Candida_dubliniensis/all_assembly_versions/GCF_000026945.1_ASM2694v1/
get $SPP $PREFIX $EXT

SPP=Candida_glabrata
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/refseq/fungi/Candida_glabrata/all_assembly_versions/GCF_000002545.3_ASM254v2/
get $SPP $PREFIX $EXT

SPP=Cryptococcus_gattii
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/refseq/fungi/Cryptococcus_gattii/all_assembly_versions/GCF_000185945.1_ASM18594v1/
get $SPP $PREFIX $EXT

SPP=Cryptococcus_neoformans
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/refseq/fungi/Cryptococcus_neoformans/all_assembly_versions/GCF_000149385.1_ASM14938v1/
get $SPP $PREFIX $EXT

SPP=Kluyveromyces_lactis
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/refseq/fungi/Kluyveromyces_lactis/all_assembly_versions/GCF_000002515.2_ASM251v1/
get $SPP $PREFIX $EXT

SPP=Neurospora_crassa
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/refseq/fungi/Neurospora_crassa/all_assembly_versions/GCF_000182925.2_NC12/
get $SPP $PREFIX $EXT

SPP=Saccharomyces_cerevisiae
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/refseq/fungi/Saccharomyces_cerevisiae/all_assembly_versions/GCF_000146045.2_R64/
get $SPP $PREFIX $EXT

SPP=Schizosaccharomyces_pombe
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/refseq/fungi/Schizosaccharomyces_pombe/all_assembly_versions/GCF_000002945.1_ASM294v2/
get $SPP $PREFIX $EXT

SPP=Yarrowia_lipolytica
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/refseq/fungi/Yarrowia_lipolytica/all_assembly_versions/GCF_000002525.2_ASM252v1/
get $SPP $PREFIX $EXT

SPP=Zygosaccharomyces_rouxii
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/refseq/fungi/Zygosaccharomyces_rouxii/all_assembly_versions/GCF_000026365.1_ASM2636v1/
get $SPP $PREFIX $EXT


#find . -name *.fasta | xargs -I{} bash -c 'f={}; bn=`basename $f`; ap=`echo $f | sed "s/\.fasta//"`; echo $f $bn $ap; mkdir $ap; mv $f ap'

