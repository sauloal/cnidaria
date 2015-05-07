#!/usr/bin/python
import os, sys

if sys.executable.endswith(os.path.join('', 'pypy')):
    pypy_path = os.path.realpath(os.path.abspath(sys.executable))
    pypy_lib  = os.path.realpath(os.path.abspath(os.path.join(pypy_path, '..', '..', 'site-packages')))
    print "pypy path", pypy_path
    print "pypy lib ", pypy_lib
    sys.path.insert(0, pypy_lib)

import time
import copy
import math
import argparse
from time import time

from bitarray import bitarray
import cnidaria_reader
from read_titles import readFilesTitles


#./cnidaria_cne_filter.py ../../phylogenomics4/analysis/tmp_31/test01/test01.cne --titles ../../phylogenomics4/analysis/data/filelist.csv --require "Arabidopsis lyrata" --forbids "Arabidopsis thaliana TAIR10" --requires "Nicotiana benthamiana Niben v0.4.4,Nicotiana tabacum tobacco"

#./cnidaria_cne_filter.py ../../phylogenomics4/analysis/tmp_31/test01/test01.cne --titles ../../phylogenomics4/analysis/data/filelist.csv --require "Arabidopsis lyrata"  --requires "Nicotiana benthamiana Niben v0.4.4,Nicotiana tabacum tobacco"

def fixTitles( titles, speciesNames, speciesPosition ):
    #print sorted(speciesPosition.keys())
    #print titles
    for fname in speciesPosition:
        for tname in titles:
            if tname in fname:
                fnewname                          = titles[ tname ]
                print " renaming", fname, "to", fnewname
                pos                               = speciesPosition[ fname    ]
                speciesNames[          pos      ] = fnewname
                speciesPosition[       fnewname ] = pos
                del speciesPosition[   fname    ]
                break



@cnidaria_reader.memoize0
def check_presence(presence, requires_bin, forbids_bin):
    if requires_bin is not None:
        required_present  = presence | requires_bin
        #print "requires", presence, requires_bin, required_present , "%2d" % required_present.count() , required_present.count() != numSpps, not required_present.all()
        #assert ( required_present.count() != numSpps ) == ( not required_present.all() ), "presence %s req %s count %d num spps %d neq %s not required_present.all %s and %s" % ( presence, required_present, required_present.count(), numSpps, ( required_present.count() != numSpps ), not required_present.all(), (( required_present.count() != numSpps ) == ( not required_present.all() )) )
        #if required_present.count() != numSpps:
        if not required_present.all():
            #print
            return False
    
    if forbids_bin is not None:
        forbidden_present = presence & forbids_bin
        #print "forbids ", presence, forbids_bin , forbidden_present, "%2d" % forbidden_present.count(), forbidden_present.count() != 0    , forbidden_present.any()
        #assert ( forbidden_present.count() != 0 ) == ( forbidden_present.any() )
        #if forbidden_present.count() != 0:
        if forbidden_present.any():
            #print
            return False
    
    return True

def print_fasta(fhd, pos, seq):
    fhd.write(">%d\n%s\n\n" % (pos, seq))

def print_lst(fhd, pos, seq):
    fhd.write(seq)
    fhd.write("\n")

def print_tab(fhd, pos, seq):
    fhd.write("%d\t%s\n" % (pos, seq))

formaters = {
    'fasta': print_fasta,
    'lst'  : print_lst,
    'tab'  : print_tab
}

def main():
    parser = argparse.ArgumentParser(description="Cnidaria CNE file filter")
    parser.add_argument("infile"    , type=str,                                                  help='Input CNE file'                     )
    parser.add_argument("--dry"     ,                                       action='store_true', help='Dry run'                            )
    parser.add_argument("--titles"  , type=str,            default=None   ,                      help='Titles file'                        )
    parser.add_argument("--sep"     , type=str,            default=','    ,                      help='List separator'                     )
    parser.add_argument("--out"     , type=str,            default=None   ,                      help='Output (default: out.[format])'     )
    parser.add_argument("--format"  , type=str,            default='fasta',                      help='Output Format (fasta, lst, tab)'    )
    parser.add_argument("--require" , type=str, nargs='+', default=None   ,                      help='Required sample'                    )
    parser.add_argument("--requires", type=str,            default=None   ,                      help='Required samples (comma separated)' )
    parser.add_argument("--forbid"  , type=str, nargs='+', default=None   ,                      help='Forbidden sample'                   )
    parser.add_argument("--forbids" , type=str,            default=None   ,                      help='Forbidden samples (comma separated)')

    args       = parser.parse_args()
    infile     = args.infile
    dry        = args.dry
    filetitles = args.titles
    list_sep   = args.sep
    out        = args.out
    out_fmt    = args.format
    
    arequire   = args.require
    arequires  = args.requires
    aforbid    = args.forbid
    aforbids   = args.forbids
    
    requires = []
    forbids  = []
    
    if arequire is not None:
        requires.extend(arequire)
    
    if arequires is not None:
        requires.extend(arequires.split(list_sep))

    if aforbid is not None:
        forbids.extend(aforbid)
    
    if aforbids is not None:
        forbids.extend(aforbids.split(list_sep))

    
    if out_fmt in formaters:
        out_fmt = formaters[out_fmt]
    else:
        print "invalid format", out_fmt
        sys.exit(1)
    
    if out is None:
        out = 'out.' + args.format
    
    out_fhd = open(out, 'w')

    print "Input File ", infile
    if not os.path.exists(infile):
        print "input file %s does not exists" % infile
        sys.exit(1)


    if filetitles is not None:
        print "Titles File ", filetitles
        if ( not os.path.exists( filetitles ) ):
            print "input file titles given %s but file does not exists" % (filetitles)
            sys.exit(1)

    print "Output File" , out
    print "Requires\n\t", "\n\t".join(requires)
    print "Forbids\n\t" , "\n\t".join(forbids )


    jfinst          = cnidaria_reader.reader(infile, verbose=False)

    filetype        = jfinst.getKey( "filetype"           )
    speciesNames    = jfinst.getKey( "in_filenames"       )
    speciesPosition = {}
    
    Total           = jfinst.getKey( "num_kmer_total_spp" )
    Valid           = jfinst.getKey( "num_kmer_valid_spp" )
    
    size            = jfinst.getSize()

    if   ( filetype != "cnidaria/complete" ):
        print "only complete file (.cne) can be used"
        sys.exit(0)

    for sppPos, sppName in enumerate( speciesNames ):
        speciesPosition[ sppName ] = sppPos

    if filetitles is not None:
        titles = readFilesTitles( filetitles, verbose=False )
        fixTitles( titles, speciesNames, speciesPosition )

    numSpps                        = len( speciesNames )


    print "filetype   : %s"    % filetype
    #print "total kmers: %s"    % ", ".join( [ "%12d" %x for x in Total ] )
    #print "valid kmers: %s"    % ", ".join( [ "%12d" %x for x in Valid ] )
    print "numSpps    : %d"    % numSpps
    print "size       : %d"    % size
    print "species    :"
    for sn in speciesNames:
        print "\t", 
        if   sn in requires:
            print '+',
        elif sn in forbids:
            print '-',
        else:
            print ' ',
        print sn
        

    
    if not all([x in speciesNames for x in requires]):
        print "not all required species is present in the file"
        for x in requires:
            if x not in speciesNames:
                print "\t", x
        sys.exit(1)

    if not all([x in speciesNames for x in forbids]):
        print "not all forbidden species is present in the file"
        for x in forbids:
            if x not in speciesNames:
                print "\t", x
        sys.exit(1)

    if len(set(requires).intersection(forbids)) != 0:
        print 'requires        ', requires
        print 'forbids         ', forbids
        print 'intersection    ', set(requires).intersection(forbids)
        print 'len intersection',len(set(requires).intersection(forbids))
        sys.exit(1)

    

    requires_bin = None
    if requires is not None and len(requires) > 0:
        requires_bin = numSpps * bitarray('0')
        for x, sn in enumerate(speciesNames):
            if sn not in requires:
                requires_bin[x] = True
    

    forbids_bin  = None
    if forbids is not None and len(forbids) > 0:
        forbids_bin  = numSpps * bitarray('0')
        for x, sn in enumerate(speciesNames):
            if sn in forbids:
                forbids_bin[x] = True
        
    print "requires_bin", requires_bin
    print "forbids_bin ", forbids_bin
    sys.stdout.flush()

    if dry:
        sys.exit(0)
    #sys.exit(0)
    #for kmer, presence in jfinst:
    count_total =  0
    count_valid =  0
    last_perc   =  0 
    start_time  = time()
    last_time   = start_time
    
    profile     = False
    
    if profile:
        import cProfile, pstats, StringIO
        pr = cProfile.Profile()
        pr.enable()


    parseCompleteRegisterData      = jfinst.parseCompleteRegisterData
    parseCompleteRegisterDataPiece = jfinst.parseCompleteRegisterDataPiece
    parseCompleteRegisterKmer      = jfinst.parseCompleteRegisterKmer
    parseCompleteRegisterKmerPiece = jfinst.parseCompleteRegisterKmerPiece
    nextCompletePair               = jfinst.nextCompletePair

    for kmer_str, data_str in nextCompletePair():
        count_total += 1
        
        curr_perc = int((count_total / (size * 1.0)) * 10000)
        if curr_perc != last_perc:
            curr_time     = time()
            elap_timeG    = curr_time - start_time
            last_perc     = curr_perc
            last_time     = curr_time
            speed         = count_total   / elap_timeG
            missing_count = size          - count_total
            etc           = missing_count / speed
            print '%6.2f %% | valid %12d | current %12d | total %12d | ela %8d sec | speed %7d reg/sec | etc %8d sec' % (curr_perc/100.0, count_valid, count_total, size, elap_timeG, speed, etc)
            sys.stdout.flush()
        
        presence = parseCompleteRegisterDataPiece(data_str)
        
        if not check_presence(presence, requires_bin, forbids_bin):
            continue
        
        kmer = parseCompleteRegisterKmerPiece(kmer_str)

        #print "%2d %-45s %-32s %s" % ( count_valid, repr(data), kmer, ", ".join( ["%-5s"%repr(x) for x in presence] ) )
        #print "presence", presence
        #if requires_bin is not None:
        #    print "requires", presence, requires_bin, required_present , "%2d" % required_present.count() , required_present.count() != numSpps, not required_present.all()
        #if forbids_bin is not None:
        #    print "forbids ", presence, forbids_bin , forbidden_present, "%2d" % forbidden_present.count(), forbidden_present.count() != 0     , forbidden_present.any()
        #print
        #sys.stdout.flush()

        out_fmt(out_fhd, count_valid, kmer)
        
        count_valid += 1
        if profile:
            if count_valid == 5:
                break
    
    out_fhd.flush()
    
    if profile:
        pr.disable()
        s = StringIO.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print s.getvalue()


if __name__ == '__main__':
    main()



#{
#    "num_infiles":22,
#    "num_srcfiles":22,
#    "num_combinations":0,
#    "complete_registers":171670564,
#    "min_val":2,
#    "max_val":22,
#    "save_every":1,
#    "num_pieces":1,
#    "piece_num":0,
#    "kmer_size":31,
#    "kmer_bytes":8,
#    "data_bytes":3,
#    "block_bytes":11,
#    "j_offset":1832,
#    "j_size":4294967296,
#    "j_matrices_size":1,
#    "j_matrices":[
#        {
#            "r":32,
#            "c":62,
#            "l":62,
#            "columns":[4076151366,]
#        }
#    ],
#    "version":8,
#    "filetype":"cnidaria/json_matrix",
#    "in_filenames":["/mnt/scratch/aflit001/nobackup/phylogenomics_raw/rna/Antirrhinum_majus_EST_cAMwp.seq.jf",],
#    "num_kmer_total_spp":[8012615,40192566,],
#    "num_kmer_valid_spp":[66907,38499746],
#    "matrix":[[[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]]
#}
    
