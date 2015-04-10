import os
import sys
import time


#rm tree.cpp tree.h core; ../../lzz/lzz -e tree.lzz && python setup.py build

print "importing cnidariapy"
import cnidariapy
print "imported  cnidariapy"

print "importing libs"
import cnidaria_stats
print "imported  libs"

threads        = 1
binomialSample = 5


def main():
    if len( sys.argv ) > 1:
        outfile    = sys.argv[1 ]
        filetitles = sys.argv[2 ]
        infiles    = sys.argv[3:]

        process(outfile, infiles, filetitles=filetitles)
        
    else:
        test()

def test():
    print "test"
    outfile    = "python_test.bin"
    filetitles = "filetitles.csv"
    infiles    = [
        "/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/Arabidopsis_lyrata.fasta.jf",
        "/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/Arabidopsis_thaliana_TAIR10_genome.fas.jf",
        "/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/Citrus_sinensis.fasta.jf",
        "/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/Glycine_max.fasta.jf",
        "/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/Nicotiana_benthamiana_Niben.genome.v0.4.4.scaffolds.nrcontigs.fasta.jf",
        "/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/Nicotiana_tabacum_tobacco_genome_sequences_assembly.fasta.jf",
        "/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/Oryza_brachyantha.fasta.jf",
        "/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/Oryza_sativa_build_5.00_IRGSPb5.fa.jf",
        "/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/Populus_trichocarpa.fasta.jf",
        "/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/S_lycopersicum_chromosomes.2.40.fa.jf",
        "/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/Solanum_peruvianum_CSH_transcriptome.fasta.jf",
        "/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/Solanum_peruvianum_Speru_denovo.fa.jf",
        "/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/Solanum_tuberosum_PGSC_DM_v3_superscaffolds.fasta.jf",
        "/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/Spimpinellifolium_genome.contigs.fasta.jf",
        "/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/Vitis_vinifera_Genoscope_12X_2010_02_12_scaffolds.fa.jf",
        "/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/Zea_mays.fasta.jf",
    ]
    
    print "merging jfs"
    process(outfile, infiles)

def process(outfile, infiles, filetitles=None):
    print "exporting to:", outfile
    print "file titles :", filetitles
    print "input files :", infiles
    
    cni     = cnidariapy.cnidariapy()
    
    if not os.path.exists( outfile ):
        cni.merge_jfs( infiles, outfile, threads, binomialSample )
    
    if filetitles is not None:
        if not os.path.exists( filetitles ):
            filetitles = None
    
    cnidaria_stats.processBin( outfile, filetitles=filetitles )
    
    print "jfs merged"

if __name__ == "__main__":
    main()