set -xeu

cd data

function get {
    SPP=$1
    PREFIX=$2

    if [[ ! -f "$SPP/$SPP.fasta" ]]; then
        mkdir -p $SPP
        cd $SPP
        wget --quiet --no-clobber --continue --timeout=60 --tries=2 --random-wait ${PREFIX}*.fna
        cat *.fna > ../$SPP.fasta
        ls
        cd ..
    fi
}

SPP=Aspergillus_fumigatus_uid14003
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/Fungi/Aspergillus_fumigatus_uid14003/
get $SPP $PREFIX

SPP=Aspergillus_nidulans_FGSC_A4_uid13961
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/Fungi/Aspergillus_nidulans_FGSC_A4_uid13961/
get $SPP $PREFIX

SPP=Aspergillus_niger_CBS_513_88_uid19263
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/Fungi/Aspergillus_niger_CBS_513_88_uid19263/
get $SPP $PREFIX

SPP=Aspergillus_oryzae_RIB40_uid28175
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/Fungi/Aspergillus_oryzae_RIB40_uid28175/
get $SPP $PREFIX

SPP=Candida_dubliniensis_CD36_uid38659
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/Fungi/Candida_dubliniensis_CD36_uid38659/
get $SPP $PREFIX

SPP=Candida_glabrata
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/Fungi/Candida_glabrata/
get $SPP $PREFIX

SPP=Candida_glabrata_CBS138_uid12376
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/Fungi/Candida_glabrata_CBS138_uid12376/
get $SPP $PREFIX

SPP=Cryptococcus_gattii_WM276
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/Fungi/Cryptococcus_gattii_WM276/
get $SPP $PREFIX

SPP=Cryptococcus_neoformans_var_JEC21_uid10698
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/Fungi/Cryptococcus_neoformans_var_JEC21_uid10698/
get $SPP $PREFIX

SPP=Kluyveromyces_lactis_NRRL_Y-1140_uid12377
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/Fungi/Kluyveromyces_lactis_NRRL_Y-1140_uid12377/
get $SPP $PREFIX

SPP=Neurospora_crassa_uid132
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/Fungi/Neurospora_crassa_uid132/
get $SPP $PREFIX

SPP=Saccharomyces_cerevisiae_uid128
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/Fungi/Saccharomyces_cerevisiae_uid128/
get $SPP $PREFIX

SPP=Schizosaccharomyces_pombe_uid127
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/Fungi/Schizosaccharomyces_pombe_uid127/
get $SPP $PREFIX

SPP=Yarrowia_lipolytica_CLIB122_uid12414
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/Fungi/Yarrowia_lipolytica_CLIB122_uid12414/
get $SPP $PREFIX

SPP=Zygosaccharomyces_rouxii_CBS_732_uid39573
PREFIX=ftp://ftp.ncbi.nih.gov/genomes/Fungi/Zygosaccharomyces_rouxii_CBS_732_uid39573/
get $SPP $PREFIX


#find . -name *.fasta | xargs -I{} bash -c 'f={}; bn=`basename $f`; ap=`echo $f | sed "s/\.fasta//"`; echo $f $bn $ap; mkdir $ap; mv $f ap'

