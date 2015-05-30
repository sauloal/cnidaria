#!/usr/bin/python
import os
import sys
import copy
import ast
import argparse
from pprint import pformat

#./gen_test_mkfile.py 4 1000
#
#rm tmp/core; TESTNUM=4; (FDL=$PWD; cd tmp; max=10; mmax=$(($max-1)); for p in $(seq 0 $mmax); do echo max $max p $p; $FDL/cnidaria $TESTNUM $max $p 2>&1 | tee test${TESTNUM}_${p}_${max}.log &\ ; done )
#rm tmp/core; TESTNUM=4; (FDL=$PWD; cd tmp; max=10; mmax=$(($max+1)); $FDL/cnidaria $TESTNUM $max $mmax 2>&1 | tee test${TESTNUM}_${p}_${max}.log )


#./gen_mkfile.py /home/aflit001/dev/phylogenomics4/analysis/data/filelist.csv test_def.csv /tmp/test_21_50 21 50 -h

#./gen_mkfile.py /home/aflit001/dev/phylogenomics4/analysis/data/filelist.csv test_def.csv /tmp/test_21_50 21 50
#./gen_mkfile.py /home/aflit001/dev/phylogenomics4/analysis/data/filelist.csv test_def.csv /tmp/test_21_50 21 50 --export-complete
#./gen_mkfile.py /home/aflit001/dev/phylogenomics4/analysis/data/filelist.csv test_def.csv /tmp/test_21_50 21 50 --separate

#./gen_mkfile.py /home/aflit001/dev/phylogenomics4/analysis/data/filelist.csv test_def.csv ~/scratch/nobackup/phylogenomics_tmp_11/ 11 20 --export-complete


EXE_DIR = os.path.abspath(os.path.dirname(__file__))
DRY_RUN = False

def main():
    parser = argparse.ArgumentParser(   description='Cnidaria Merger Makefile Creator', formatter_class=argparse.ArgumentDefaultsHelpFormatter )
    
    parser.add_argument('file_list' , type=str, help='file name mapping list')
    parser.add_argument('def_file'  , type=str, help='definition file'       )
    parser.add_argument('out_dir'   , type=str, help='output dir'            )
    parser.add_argument('kmer_size' , type=int, help='kmer size'             )
    parser.add_argument('num_pieces', type=int, help='number of pieces'      )
    
    parser.add_argument('-thr'   ,              '--threads'         , dest='num_threads'    , default=1            , type=int , nargs='?',                       help='Number of threads. Not compatible with COMPLETE')
    parser.add_argument('-min'   ,              '--minval'          , dest='minVal'         , default=2            , type=int , nargs='?',                       help='Minimum number of shared species to start counting')
    parser.add_argument('-se'    ,              '--save-every'      , dest='save_every'     , default=1            , type=int , nargs='?',                       help='Count every N k-mers. Speeds analysis while skipping data')
    parser.add_argument('-me'    , '-merge'   , '--merge-only'      , dest='merge_only'     ,                                              action='store_true' , help='Merge only')
    parser.add_argument('-nm'    , '-nomerge' , '--do-not-merge'    , dest='do_merge'       ,                                              action='store_false', help='Do not merge')
    parser.add_argument('-ec'    , '-complete', '--export-complete' , dest='export_complete',                                              action='store_true' , help='Export COMPLETE database')
    parser.add_argument('-nem'   , '-nomatrix', '--no-export-matrix', dest='export_matrix'  ,                                              action='store_false', help='DO NOT Export MATRIX database')
    parser.add_argument('-nimg'  , '-noimage' , '--no-gen-image'    , dest='gen_image'      ,                                              action='store_false', help='DO NOT Generage PNG images')

    args = parser.parse_args()
    
    gen_global(args)


def read_def( defs, def_file, selected_proj_name=None ):
    projs = {}
    
    with open( def_file, 'r' ) as fhd:
        for line in fhd:
            line = line.strip()
            
            if len(line) == 0:
                continue
        
            if line[0] == '#':
                cols = line[1:].split('=')
                
                if len(cols) != 2:
                    continue
                
                print line
            
                k, v = cols
                
                if k[0] == '_':
                    print "k", k, "v", v,
                    r = ast.literal_eval( v % defs )
                    print "r", r
                    defs[k] = r
                
                else:
                    r = v % defs
                    print "k", k, "r", r
                    defs[k] = r
                    
                continue

            #print line
            
            try:
                proj_name, file_name = line.split("\t")
            except:
                print "wrong formated line"
                print line
                sys.exit(1)
            
            if ( selected_proj_name is not None ) and ( proj_name != selected_proj_name ):
                print '*'
                continue
            
            if proj_name not in projs:
                projs[ proj_name ] = []
                
            file_name = os.path.abspath( file_name % defs )
            projs[ proj_name ].append( file_name )
            print proj_name, file_name
            
            if file_name in projs:
                if proj_name not in defs["_verify"]:
                    defs["_verify"].append( proj_name )
                    
                if proj_name not in defs["_reqs"]:
                    defs["_reqs"][proj_name] = []

                defs["_reqs"][proj_name].append( file_name )

    if len(defs["_verify"]) > 0:
        to_check = defs["_verify"]
        for proj_name in to_check:
            reqs = defs["_reqs"][proj_name]
            if not all([req in projs for req in reqs]):
                defs["_verify"].remove(proj_name)

    print "defs" , pformat(defs        )
    print "projs", pformat(projs.keys())

    return projs


def verify_args( args ):
    file_list  = args.file_list
    def_file   = args.def_file
    out_dir    = args.out_dir
    kmer_size  = args.kmer_size
    num_pieces = args.num_pieces

    if not os.path.exists(file_list):
        print "file list %s does not exists" % file_list
        sys.exit(1)
        
    if not os.path.exists(def_file):
        print "def file %s does not exists" % def_file
        sys.exit(1)

    if not os.path.exists(out_dir):
        print "out dir %s does not exists" % out_dir, "creating"
        
        os.makedirs(out_dir)
        
    else:
        if not os.path.isdir( out_dir ):
            print "tmp path %s is a directory" % out_dir
            sys.exit(1)

    cnidaria_opts = ""
    if args.num_threads != 1:
        cnidaria_opts += ' --threads %d' % args.num_threads
        
    if args.minVal != 2:
        cnidaria_opts += ' --min-val %d' % args.minVal

    if args.save_every != 1:
        cnidaria_opts += ' --save-every %d' % args.save_every

    if args.merge_only:
        cnidaria_opts += ' --merge-only'

    if not args.do_merge:
        cnidaria_opts += ' --do-not-merge'

    if args.export_complete:
        cnidaria_opts += ' --export-complete'

    if not args.export_matrix:
        cnidaria_opts += ' --no-export-matrix'

    if DRY_RUN:
        cnidaria_opts += ' --dry-run'

    file_list = os.path.abspath(file_list)
    out_dir   = os.path.abspath(out_dir  )

    return file_list, def_file, out_dir, kmer_size, num_pieces, cnidaria_opts, args.export_complete


def gen_global( args ):
    file_list, def_file, out_dir, kmer_size, num_pieces, cnidaria_opts, export_complete = verify_args( args )

    out_file = os.path.join(out_dir, 'Makefile')

    defs     = {
        "verifier_exe"      : os.path.join( EXE_DIR, "verify_merge.py"  ),
        "cnidaria_exe"      : os.path.join( EXE_DIR, "cnidaria.py"      ),
        "newick_to_png_exe" : os.path.join( EXE_DIR, "newick_to_png.py" ),
        "verify_csvs_exe"   : os.path.join( EXE_DIR, "verify_csvs.py"   ),
        "cnidaria_stats_exe": os.path.join( EXE_DIR, "cnidaria_stats.py"),

        "file_list"         : file_list ,  #"/home/aflit001/dev/phylogenomics4/analysis/data/filelist.csv",
        "def_file"          : def_file  ,  #"/home/aflit001/dev/phylogenomics4/analysis/data/filelist.csv",
        "kmer_size"         : kmer_size ,
        "num_pieces"        : num_pieces,
        "out_dir"           : out_dir   ,  #"/home/aflit001/nobackup/phylogenomics_tmp",

        "_reqs"             : {},
        "_verify"           : [],
        "_projs"            : {},
    }

    if not os.path.exists( defs["cnidaria_exe"] ):
        print "executable %s does not exists" % defs["cnidaria_exe"]
        sys.exit(1)

    if not os.path.exists( defs["verifier_exe"] ):
        print "executable %s does not exists" % defs["verifier_exe"]
        sys.exit(1)


    projs    = read_def( defs, def_file )

    makefile = []
    
    makefile.append("\n")
    makefile.append("\n.SUFFIXES:\n")
    makefile.append("\n")
    #makefile.append("\n.DELETE_ON_ERROR:\n")
    #makefile.append("\n")

    makefile.append( "all: " + " ".join(sorted(projs.keys()))  + "\n\n" )

    if len(defs["_verify"]) > 0:
        makefile.append( "verify: " + " ".join( [ "verify_" + x for x in sorted(defs["_verify"]) ] ) + "\n" )

    makefile.append( "\n" )

    makefile.append( "clean: " + " ".join([ "clean_" + x for x in sorted(projs.keys()) ]) + "\n\n")
    
    for proj_name in sorted(projs):
        defs["proj_name"] = proj_name
        line = "clean_%(proj_name)s:\n\t$(MAKE) -k -C %(out_dir)s/%(proj_name)s clean\n\n" % defs
        makefile.append( line )

    makefile.append( "\n" )

    for proj_name in sorted(projs):
        reqs = " ".join( projs[proj_name] )
        defs["proj_name"] = proj_name
        defs["reqs"     ] = reqs
        line = "%(proj_name)s: %(reqs)s\n\t$(MAKE) -k -C %(out_dir)s/%(proj_name)s\n\n" % defs
        makefile.append( line )

    makefile.append( "\n" )

    if len(defs["_verify"]) > 0:
        for proj_name in sorted(defs["_verify"]):
            defs["proj_name"] = proj_name
            defs["csvs"     ] = " ".join([ os.path.join(defs["out_dir"], x, x) + ".json.csv" for x in sorted(defs["_reqs"][proj_name]) ]) + " " + os.path.join(defs["out_dir"], proj_name, proj_name) + ".json.csv"

            line = "verify_%(proj_name)s: %(proj_name)s\n\t%(verifier_exe)s %(csvs)s\n\n" % defs

            makefile.append( line )
            

    open(out_file, "w").write( "".join(makefile) )

    proj_names = sort_projs(defs, projs)

    for proj_name in sorted(proj_names):
        print "creating project", proj_name
        p_out_dir = os.path.join(out_dir, proj_name)
        infiles   = projs[ proj_name ]
        gen_local( file_list, kmer_size, num_pieces, p_out_dir, defs, proj_name, infiles, cnidaria_opts, export_complete, args )
    
def sort_projs(defs, projs):
    ordered   = []
    no_change = True
    while ( no_change ):
        no_change = False
        for proj_name in projs:
            for infile in projs[proj_name]:
                if infile in projs:
                    if infile not in ordered:
                        ordered.append( infile )
                        no_change = True
                    
                    file_index = ordered.index( infile )

                    if proj_name not in ordered:
                        ordered.append( proj_name )
                        no_change = True
                    
                    proj_index = ordered.index( proj_name )
                    
                    if proj_index < file_index:
                        ordered.remove( proj_name )
                        ordered.append( proj_name )
                        no_change = True

    for proj in projs:
        if proj not in ordered:
            ordered.insert(0, proj)

    print  "oredered", ordered
    return ordered

def gen_local( file_list, kmer_size, num_pieces, out_dir, defs, proj_name, infiles, cnidaria_opts, export_complete, args ):
    out_file   = os.path.join(    out_dir, "Makefile" )

    if not os.path.exists(out_dir):
        print "  tmp folder %s does not exists" % out_dir, "creating"
        os.makedirs(out_dir)

    else:
        if not os.path.isdir( out_dir ):
            print "  tmp path %s is a directory" % out_dir
            sys.exit(1)

    print "  saving to out_file %s" % out_file


    for p, infile in enumerate(infiles):
        if infile in defs["_projs"]:
            infiles[p] = defs["_projs"][infile]["out_db"]
    


    gdata   = copy.deepcopy(defs)

    gdata["piece_num"    ] = num_pieces+1
    gdata["out_dir"      ] = out_dir
    gdata["proj_name"    ] = proj_name
    gdata["cnidaria_opts"] = cnidaria_opts
    gdata["infiles"      ] = " ".join( infiles )


    makefile = []

    makefile.append("\n")
    makefile.append("\n.SUFFIXES:\n")
    makefile.append("\n")
    #makefile.append("\n.DELETE_ON_ERROR:\n")
    #makefile.append("\n")

    gdata["bn"       ] = os.path.join( out_dir, proj_name )
    gdata["suffix"   ] = proj_name
    gdata["out_db"   ] = ""
    gdata["out_mat"  ] = gdata["bn"      ] + ".cnm"
    gdata["out_json" ] = gdata["bn"      ] + ".json"
    gdata["out_log"  ] = gdata["bn"      ] + ".log"
    gdata["out_ok"   ] = gdata["bn"      ] + ".ok"
    gdata["out_err"  ] = gdata["bn"      ] + ".err"
    gdata["prefix"   ] = gdata["bn"      ] + "_*"
    gdata["all_csv"  ] = gdata["bn"      ] + ".all.csv"
    gdata["all_ccsv" ] = gdata["bn"      ] + ".all.count.csv"
    gdata["out_csv"  ] = gdata["out_json"] + ".csv"
    gdata["out_ccsv" ] = gdata["out_json"] + ".count.csv"
    gdata["out_png"  ] = gdata["out_json"] + ".pngok"

    if export_complete:
        gdata["out_db"   ] = gdata["bn"      ] + ".cne"
        


    global_vars = """
CNIDARIA_EXE=%(cnidaria_exe)s
NEWICK_TO_PNG_EXE=%(newick_to_png_exe)s
CNIDARIA_STATS_EXE=%(cnidaria_stats_exe)s
VERIFY_CSVS_EXE=%(verify_csvs_exe)s

INFILES=%(infiles)s


""" % gdata 

    makefile.append(global_vars)



    if args.gen_image:
        makefile.append("all: %(out_ok)s %(all_csv)s %(out_png)s\n\n" % gdata )

    else:
        makefile.append("all: %(out_ok)s %(all_csv)s\n\n" % gdata )



    makefile.append("clean:\n\trm %(out_dir)s/test* %(all_csv)s || true\n\n" % gdata )

    img_rules = """


%(out_dir)s/%%.nj.png: %(out_dir)s/%%.nj
	$(NEWICK_TO_PNG_EXE) $<

%(out_dir)s/%%.upgma.png: %(out_dir)s/%%.upgma
	$(NEWICK_TO_PNG_EXE) $<

    
""" % gdata

    makefile.append( img_rules )
    


    oks   = []
    csvs  = []
    pngs  = []
    metas = []

    for piece_num in xrange(1, num_pieces+1):
        lmakefile = []
        
        data              = copy.copy( gdata )
        data["piece_num"] = piece_num
        data["suffix"   ] = "%(proj_name)s_%(piece_num)04d_%(num_pieces)04d" % data
        bn                = os.path.join( out_dir, "%(suffix)s" % data )
        data["bn"       ] = bn
        data["out_db"   ] = ""
        data["out_mat"  ] = bn + ".cnm"
        data["out_json" ] = bn + ".json"
        data["out_csv"  ] = bn + ".json.csv"
        data["out_png"  ] = bn + ".json.pngok"
        data["out_log"  ] = bn + ".log"
        data["out_ok"   ] = bn + ".ok"
        data["out_err"  ] = bn + ".err"

        if export_complete:
            data["out_db"   ] = bn + ".cne"

        oks  .append( data["out_ok" ] )
        csvs .append( data["out_csv"] )
        pngs .append( data["out_png"] )
        metas.append( data["suffix" ] )




        meta = """

.PHONY: %(suffix)s
%(suffix)s: %(out_ok)s %(out_csv)s %(out_png)s

""" % data

        lmakefile.append( meta )




        line            = """%(out_ok)s: $(INFILES)
\trm %(out_err)s %(out_db)s %(out_mat)s %(out_json)s %(out_csv)s %(out_log)s 2>&1 || true
\t( ulimit -c unlimited && time $(CNIDARIA_EXE) %(cnidaria_opts)s --num-pieces %(num_pieces)d --piece-num %(piece_num)d --outfile %(proj_name)s $^ 2>&1 && touch %(out_ok)s ) | tee %(out_log)s
\tif [ ! -f %(out_ok)s ]; then echo ERROR RUNNING %(out_json)s; touch %(out_err)s; rm %(out_db)s %(out_mat)s %(out_json)s %(out_csv)s %(out_log)s 2>&1 || true; false; else echo SUCCESS RUNNING %(out_json)s; fi\n\n""" % data

        lmakefile.append( line )





        cmd_csv = """
%(out_csv)s: %(out_ok)s
\t$(CNIDARIA_STATS_EXE) %(out_json)s %(file_list)s
\n\n\n\n""" % data

        lmakefile.append( cmd_csv )





        cmd_png = """

TREE_NJ_%(suffix)s=$(wildcard %(out_dir)s/%(suffix)s.*.nj)
TREE_UP_%(suffix)s=$(wildcard %(out_dir)s/%(suffix)s.*.upgma)
PNGS_NJ_%(suffix)s=$(patsubst %%.nj,%%.nj.png,$(TREE_NJ_%(suffix)s))
PNGS_UP_%(suffix)s=$(patsubst %%.upgma,%%.upgma.png,$(TREE_UP_%(suffix)s))

%(out_png)s: %(out_csv)s
\t$(MAKE) -k %(out_png)s2

.PHONY: %(out_png)s2

%(out_png)s2: %(out_csv)s $(PNGS_NJ_%(suffix)s) $(PNGS_UP_%(suffix)s)
\ttouch %(out_png)s
\n\n\n\n
""" % data
        lmakefile.append( cmd_png )




        makefile.extend( lmakefile )
        
        #if separate:
        #    loutfile = "%s_%04d_%04d" % ( out_file, piece_num, num_pieces )
        #    print "  saving to local out file %s" % loutfile
        #    with open(loutfile, "w") as fhd:
        #        fhd.write( global_vars        )
        #        fhd.write( img_rules          )
        #        fhd.write( "all: %s\n\n" % " ".join( [ data[x] for x in ( "out_ok", "out_csv", "out_png" ) ] ) )
        #        fhd.write( "".join(lmakefile) )




    gdata["ok_files"  ] = " ".join(oks  )
    gdata["png_files" ] = " ".join(pngs )
    gdata["meta_files"] = " ".join(metas)
    gdata["csv_files" ] = " ".join(csvs )
    gdata["ccsv_files"] = " ".join([ x.replace('.csv', '.count.csv') for x in csvs ])




    all_res_files = """


OK_FILES=%(ok_files)s


CSV_FILES=%(csv_files)s


PNG_FILES=%(png_files)s


CCSV_FILES=%(ccsv_files)s


META_FILES=%(meta_files)s


""" % gdata

    makefile.append( all_res_files   )



#    if num_pieces == 1:
#        all_k             = """
#%(out_ok)s: $(OK_FILES)
#\ttouch %(out_ok)s
#\n""" % gdata
#
#        makefile.append( all_k   )
#
#    else:
    all_k             = """

%(out_ok)s: $(OK_FILES)
\techo GENERATING %(out_ok)s. DELETING OLD FILES
\trm %(out_err)s %(out_db)s %(out_mat)s %(out_json)s %(out_csv)s %(out_log)s 2>&1 || true
\t( ulimit -c unlimited && time $(CNIDARIA_EXE) --merge-only %(cnidaria_opts)s --num-pieces %(num_pieces)d --outfile %(proj_name)s $(INFILES) 2>&1 && touch %(out_ok)s ) | tee %(out_log)s
\tif [ ! -f %(out_ok)s ]; then echo ERROR RUNNING %(out_json)s; touch %(out_err)s; rm %(out_db)s %(out_mat)s %(out_json)s %(out_csv)s 2>&1 || true; false; else echo SUCCESS RUNNING %(out_json)s; fi\n""" % gdata

    makefile.append( all_k   )





    all_s              = """

\n%(out_csv)s: %(out_ok)s
\t$(CNIDARIA_STATS_EXE) %(out_json)s %(file_list)s\n\n
""" % gdata

    makefile.append( all_s )




    cmd_png = """
TREE_NJ_%(suffix)s=$(wildcard %(out_dir)s/%(suffix)s*.nj)
TREE_UP_%(suffix)s=$(wildcard %(out_dir)s/%(suffix)s*.upgma)
PNGS_NJ_%(suffix)s=$(patsubst %%.nj,%%.nj.png,$(TREE_NJ_%(suffix)s))
PNGS_UP_%(suffix)s=$(patsubst %%.upgma,%%.upgma.png,$(TREE_UP_%(suffix)s))

%(out_png)s: %(out_ok)s %(out_csv)s $(PNG_FILES)
\t$(MAKE) -k %(out_png)s2

.PHONY: %(out_png)s2

%(out_png)s2: %(out_ok)s %(out_csv)s $(PNGS_NJ_%(suffix)s) $(PNGS_UP_%(suffix)s)
\ttouch %(out_png)s
\n\n\n\n
""" % gdata

    makefile.append( cmd_png )





    all_csv = """\n
%(all_csv)s: $(CSV_FILES) %(out_csv)s %(out_ok)s
\t$(VERIFY_CSVS_EXE) $(CSV_FILES) %(out_csv)s
\tcat $(CSV_FILES)  %(out_csv)s  > %(all_csv)s
\tcat $(CCSV_FILES) %(out_ccsv)s > %(all_ccsv)s
""" % gdata

    makefile.append( all_csv )




    if os.path.exists( out_file ):
        print "  out file %s exists. deleting" % out_file
        os.remove( out_file )

    open(out_file, "w").write( "".join(makefile) )

    defs["_projs"][proj_name] = gdata




if __name__ == "__main__":
    main()
