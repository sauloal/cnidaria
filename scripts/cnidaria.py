#!/usr/bin/python

import os
import sys
import argparse

basedir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(basedir, 'build'))

print basedir
import cnidariapy

print cnidariapy.fact(3)

#for i in `seq 1 20`; do
#    echo $i
#    ../../cnidaria.py -n -thr 3 -np 20 -pn $i ../../tmp_21/test10/test10.cne ../../data/raw/external/new/*.21.jf &
#done

#../../cnidaria.py -np 20 --merge_only ../../tmp_21/test10/test10.cne ../../data/raw/external/new/*.21.jf


#def send_data(*args):
#def merge_data(*args):

class cnidaria(object):
    EXT_COMPLETE  = '.cne'
    EXT_SUMMARY   = '.cns'
    EXT_MATRIX    = '.cnm' 
    EXT_MATRIXJ   = '.json'
    EXT_JELLYFISH = '.jf'

    def __init__(self, infiles, out_file, num_threads=1, minVal=2, save_every=1, export_complete=False, export_summary=False, export_matrix=True, num_pieces=1, piece_num=None, dry_run=False):
        self.infiles           = infiles
        self.out_file          = out_file
        self.num_threads       = num_threads
        self.minVal            = minVal
        self.save_every        = save_every
        self.export_complete   = export_complete
        self.export_summary    = export_summary
        self.export_matrix     = export_matrix
        self.num_pieces        = num_pieces
        self.piece_num         = piece_num
        self.dry_run           = dry_run

        self.prefixes          = []
        self.srcfiles_complete = []
        self.srcfiles_matrix   = []
        self.srcfiles_matrixj  = []
        self.ofiles            = []
        
        self.gen_names()
        
        print "prefixes         " , self.prefixes
        print "srcfiles_complete" , self.srcfiles_complete
        print "srcfiles_matrix  " , self.srcfiles_matrix
        print "srcfiles_matrixj " , self.srcfiles_matrixj
        
        if self.piece_num is not None:
            if self.piece_num == -1:
                self.merge_pieces()
            else:
                self.run_piece(piece_num)
            

    def dump(self):
        cnidariapy.dump(self.infiles)

    def run(self, do_merge=True):
        for piece in xrange(self.num_pieces):
            self.run_piece(piece)

        if do_merge:
            self.merge_pieces()

    def run_piece(self, piece_num):
        exists = True
        for files, exp in [[self.srcfiles_complete,self.export_complete], [self.srcfiles_matrix, self.export_matrix], [self.srcfiles_matrixj, self.export_matrix]]:
            if exp:
                fn     = files[piece_num-1]
                e      = os.path.exists(fn)
                exists = exists and e
                print "piece %d output file %s: " % (piece_num, fn), ("" if e else "does not"), "exists"
        
        if not exists:
            print "piece num %d does not exists exists. running" % piece_num
            
            if not self.dry_run:
                cnidariapy.send_data(self.infiles, self.prefixes[piece_num-1], self.num_threads, self.minVal, self.save_every, self.export_complete, self.export_summary, self.export_matrix, self.num_pieces, piece_num-1)
        
        else:
            print "piece num %d already exists" % piece_num
            
    
    def merge_pieces(self):
        if self.num_pieces == 1:
            print "one piece. no merging needed"
            return

        exists = True
        for piece_num in xrange(1, self.num_pieces+1):
            for files, exp in [[self.srcfiles_complete,self.export_complete], [self.srcfiles_matrix, self.export_matrix], [self.srcfiles_matrixj, self.export_matrix]]:
                if exp:
                    fn     = files[piece_num-1]
                    e      = os.path.exists(fn)
                    exists = exists and e
                    print "piece %d output file %s: " % (piece_num, fn), ("" if e else "does not"), "exists"
        
        if not exists:
            print "merge requested but not all files exists"
            exit(1)

        exists = False
        for ofile in self.ofiles:
            e      = os.path.exists(ofile)
            exists = exists or e
            print "merge output file %s: " % (ofile), ("" if e else "does not"), "exists"

        
        if exists:
            print "merging output file already exists."
            sys.exit(1)

        print "all input files exists. merging"
        if not self.dry_run:
            print self.out_file, self.srcfiles_complete, self.srcfiles_matrix, self.srcfiles_matrixj
            cnidariapy.merge_data(self.out_file, self.srcfiles_complete, self.srcfiles_matrix, self.srcfiles_matrixj, self.export_complete, self.export_matrix)
        print "merged"
 
    
    def gen_names(self):
        self.prefixes          = [None]*self.num_pieces
        self.srcfiles_complete = [None]*self.num_pieces
        self.srcfiles_matrix   = [None]*self.num_pieces
        self.srcfiles_matrixj  = [None]*self.num_pieces
        
        if self.num_pieces > 1:
            for j in xrange(1, self.num_pieces+1):
                i = j-1
                self.prefixes[          i ] = "%s_%04d_%04d" % (self.out_file, j, self.num_pieces)
                
                #if self.export_complete:
                self.srcfiles_complete[ i ] = self.prefixes[i] + cnidaria.EXT_COMPLETE
    
                #if self.export_matrix:
                self.srcfiles_matrix[   i ] = self.prefixes[i] + cnidaria.EXT_MATRIX
                self.srcfiles_matrixj[  i ] = self.prefixes[i] + cnidaria.EXT_MATRIXJ

            #if self.export_complete:
            self.ofiles.append( self.out_file + cnidaria.EXT_COMPLETE )
            
            #if self.export_matrix:
            self.ofiles.append( self.out_file + cnidaria.EXT_MATRIX   )
            self.ofiles.append( self.out_file + cnidaria.EXT_MATRIXJ  )

        else:
            self.prefixes[          0 ] = "%s" % (self.out_file)
            #if self.export_complete:
            self.srcfiles_complete[ 0 ] = self.prefixes[0] + cnidaria.EXT_COMPLETE

            #if self.export_matrix:
            self.srcfiles_matrix[   0 ] = self.prefixes[0] + cnidaria.EXT_MATRIX
            self.srcfiles_matrixj[  0 ] = self.prefixes[0] + cnidaria.EXT_MATRIXJ



def test():
    infiles = [
                "/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/Arabidopsis_lyrata.fasta.31.jf",
                "/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/Arabidopsis_thaliana_TAIR10_genome.fas.31.jf",
                "/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/Citrus_sinensis.fasta.31.jf"
            ]
    
    out_file        = "pytest"
    num_threads     = 1
    minVal          = 2
    save_every      = 1
    export_complete = True
    export_summary  = False
    export_matrix   = True
    num_pieces      = 2
    #piece_num       = 0

    cni = cnidaria(infiles, out_file, num_threads=num_threads, minVal=minVal, save_every=save_every, export_complete=export_complete, export_summary=export_summary, export_matrix=export_matrix, num_pieces=num_pieces)
    cni.run()


def validate_args(args):
    if len(args.infiles) < 2 and not args.dump_only:
        print "not enought input files. Cnidaria needs at least 2 databases"
        sys.exit(1)

    for infile in args.infiles:
        if not os.path.exists( infile ):
            print "input file %s does not exists" % infile
            sys.exit(1)
        
        if not (infile.endswith(cnidaria.EXT_JELLYFISH) or infile.endswith(cnidaria.EXT_COMPLETE)):
            print "input file %s is not a jellyfish database or does not ends in %s or %s" % (infile, cnidaria.EXT_JELLYFISH, cnidaria.EXT_COMPLETE)
            sys.exit(1)
    
    args.infiles = [os.path.abspath(x) for x in args.infiles]
    
    for ext, exp in [ [cnidaria.EXT_COMPLETE, args.export_complete], [cnidaria.EXT_MATRIX, args.export_matrix], [cnidaria.EXT_MATRIXJ, args.export_matrix] ]:
        out_file = args.out_file + ext
        if exp and os.path.exists( out_file ):
            print "output file %s already exists" % out_file
            sys.exit(1)
            
    if args.num_threads <=0:
        print "invalid number of threads: %d should be >=1" % args.num_threads
        sys.exit(1)
        
    if args.export_complete and args.num_threads > 1:
        print "export complete is incompatible with multiple threads. use multiple pieces"
        sys.exit(1)
            
    if args.minVal <=0:
        print "invalid minimum number of shared k-mers: %d should be >=1" % args.minVal
        sys.exit(1)
            
    if args.save_every <=0:
        print "invalid number of k-mers to skip: %d should be >=1" % args.save_every
        sys.exit(1)
            
    if args.num_pieces <=0:
        print "invalid number of pieces: %d should be >=1" % args.num_pieces
        sys.exit(1)

    if args.piece_num is not None:
        if args.piece_num <=0:
            print "invalid piece number: %d should be >=1" % args.piece_num
            sys.exit(1)
            
        if args.piece_num > args.num_pieces:
            print "invalid piece number: %d should be <= piece_num (%d)" % ( args.piece_num, args.num_pieces )
            sys.exit(1)

        if args.merge_only:
            print "merge only is not compatible with piece number"
            sys.exit(1)
            
    if args.merge_only and not args.do_merge:
        print "merge only and no merge options are mutually exclusive"
        sys.exit(1)

    print "all arguments are valid"

def main():
    parser = argparse.ArgumentParser( description='Cnidaria Merger', formatter_class=argparse.ArgumentDefaultsHelpFormatter )

    parser.add_argument('infiles', nargs='+', type=str, help='Input Jellyfish databases')

    parser.add_argument('-out'   , '--outfile'                      , dest='out_file'       , default='cnidaria_db', type=str , nargs='?', help='Prefix of output file')
    parser.add_argument('-thr'   , '--threads'                      , dest='num_threads'    , default=1            , type=int , nargs='?', help='Number of threads. Not compatible with COMPLETE')
    parser.add_argument('-min'   , '--min-val'                      , dest='minVal'         , default=2            , type=int , nargs='?', help='Minimum number of shared species to start counting')
    parser.add_argument('-se'    , '--save-every'                   , dest='save_every'     , default=1            , type=int , nargs='?', help='Count every N k-mers. Speeds analysis while skipping data')
    parser.add_argument('-np'    , '--num-pieces'                   , dest='num_pieces'     , default=1            , type=int , nargs='?', help='Number of pieces')
    parser.add_argument('-pn'    , '--piece-num'                    , dest='piece_num'      , default=None         , type=int , nargs='?', help='Piece number')

    parser.add_argument('-n'     , '-dry'     , '--dry-run'         , dest='dry_run'        ,                                              action='store_true' , help='Dry run')

    parser.add_argument('-d'     , '-dump'    , '--dump-only'       , dest='dump_only'      ,                                              action='store_true' , help='Dump only')
    parser.add_argument('-me'    , '-merge'   , '--merge-only'      , dest='merge_only'     ,                                              action='store_true' , help='Merge only')
    parser.add_argument('-nm'    , '-nomerge' , '--do-not-merge'    , dest='do_merge'       ,                                              action='store_false', help='Do not merge')
    parser.add_argument('-ec'    , '-complete', '--export-complete' , dest='export_complete',                                              action='store_true' , help='Export COMPLETE database')
    #parser.add_argument('-es'    , '-summary' , '--export_summary'  , dest='export_summary' ,                                              action='store_true' , help='Export SUMMARY  database. (default: False)')
    parser.add_argument('-nem'   , '-nomatrix', '--no-export-matrix', dest='export_matrix'  ,                                              action='store_false', help='DO NOT Export MATRIX database')
    
    args = parser.parse_args()
    
    #this is disabled
    args.export_summary = False
    
    #print args
    validate_args(args)

    #if args.piece_num is not None:
    #    #piece num is zero based
    #    args.piece_num -= 1

    print "running %d files" % len(args.infiles)
    
    cni = cnidaria(args.infiles, args.out_file, num_threads=args.num_threads, minVal=args.minVal, save_every=args.save_every, export_complete=args.export_complete, export_summary=args.export_summary, export_matrix=args.export_matrix, num_pieces=args.num_pieces, dry_run=args.dry_run)
    if args.dump_only:
        print "dumping"
        cni.dump()
        print "dump"
        
    elif args.merge_only:
        print "merging"
        cni.merge_pieces()
        print "merged"
    
    elif args.piece_num is not None:
        print "running piece %d/%d" % (args.piece_num, args.num_pieces)
        cni.run_piece(args.piece_num)
        print "runned  piece %d/%d" % (args.piece_num, args.num_pieces)
        
    else:
        print "running all %d pieces" % (args.num_pieces)
        cni.run(do_merge=args.do_merge)
        print "runned  all %d pieces" % (args.num_pieces)


    #/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/Arabidopsis_lyrata.fasta.31.jf /mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/Arabidopsis_thaliana_TAIR10_genome.fas.31.jf /mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/Citrus_sinensis.fasta.31.jf

    #test()


if __name__ == '__main__':
    main()



#def fact(*args):
#def openoutfile(*args):
#def openinfile(*args):
#def merge_complete(*args):
#def merge_complete_parallel(*args):
#def merge_complete_parallel_piece(*args):
#def merge_matrix(*args):
#def merge_matrixj(*args):
#class piece_data(_object):
#    __swig_setmethods__["srcfiles"] = _cnidariapy.piece_data_srcfiles_set
#    __swig_setmethods__["out_file"] = _cnidariapy.piece_data_out_file_set
#    __swig_setmethods__["num_threads"] = _cnidariapy.piece_data_num_threads_set
#    __swig_setmethods__["minVal"] = _cnidariapy.piece_data_minVal_set
#    __swig_setmethods__["save_every"] = _cnidariapy.piece_data_save_every_set
#    __swig_setmethods__["export_complete"] = _cnidariapy.piece_data_export_complete_set
#    __swig_setmethods__["export_summary"] = _cnidariapy.piece_data_export_summary_set
#    __swig_setmethods__["export_matrix"] = _cnidariapy.piece_data_export_matrix_set
#    __swig_setmethods__["num_pieces"] = _cnidariapy.piece_data_num_pieces_set
#    __swig_setmethods__["piece_num"] = _cnidariapy.piece_data_piece_num_set
#    __swig_setmethods__["merger"] = _cnidariapy.piece_data_merger_set
#    __swig_setmethods__["locker"] = _cnidariapy.piece_data_locker_set
#def send_data(*args):
#def merge_data(*args):
#def send_pieces(*args):
#def send_piece(*args):



#int fact(int n) {
#void openoutfile(    std::ofstream &outfile_, string_t     filename ) {
#void openinfile(     std::ifstream &infile_ , string_t     filename ) {
#void merge_complete( string_t       out_file, string_vec_t cfiles   ) {
#void merge_complete_parallel( string_t       out_file, string_vec_t cfiles, baseInt num_threads = 5 ) {
#void merge_complete_parallel_piece( string_t       out_file, baseInt numCFiles, baseInt fileCount, pos_type begin_pos, string_t infile ) {
#void merge_matrix(   string_t       out_file, string_vec_t cfiles   ) {
#void merge_matrixj(  string_t       out_file, string_vec_t cfiles   ) {
#struct piece_data {
#    string_vec_t srcfiles;
#    string_t     out_file;
#    baseInt      num_threads;
#    baseInt      minVal;
#    baseInt      save_every;
#    bool         export_complete;
#    bool         export_summary;
#    bool         export_matrix;
#    baseInt      num_pieces;
#    baseInt      piece_num;
#    merge_jfs   *merger;
#    boost::recursive_mutex *locker;
#    piece_data(
#            string_vec_t           &srcfiles_,
#            string_t               &out_file_,
#            baseInt                 num_threads_,
#            baseInt                 minVal_,
#            baseInt                 save_every_,
#            bool                    export_complete_,
#            bool                    export_summary_,
#            bool                    export_matrix_,
#            baseInt                 num_pieces_,
#            baseInt                 piece_num_,
#            merge_jfs              *merger_,
#            boost::recursive_mutex *locker_
#        ):
#            srcfiles(               srcfiles_),
#            out_file(               out_file_),
#            num_threads(            num_threads_),
#            minVal(                 minVal_),
#            save_every(             save_every_),
#            export_complete(        export_complete_),
#            export_summary(         export_summary_),
#            export_matrix(          export_matrix_),
#            num_pieces(             num_pieces_),
#            piece_num(              piece_num_),
#            merger(                 merger_),
#            locker(                 locker_)  {}
#};
#void send_data(
#            string_vec_t           &srcfiles,
#            string_t               &out_file,
#            baseInt                 num_threads,
#            baseInt                 minVal,
#            baseInt                 save_every,
#            bool                    export_complete,
#            bool                    export_summary,
#            bool                    export_matrix,
#            baseInt                 num_pieces,
#            baseInt                 piece_num
#        ) {
#void merge_data( string_t out_file, string_vec_t srcfiles_complete, string_vec_t srcfiles_matrix, string_vec_t srcfiles_matrixj ) {
#void send_pieces( piece_data_vec_t data ) {
#void send_piece(  piece_data       data ) {





##
## DEBUG
##
#void run_test_pieces(       string_vec_t srcfiles, string_t out_file, uint_t num_pieces, uint_t piece_num ) {
#    if ( piece_num == num_pieces+1 ) {
#        run_test_pieces_merge(           out_file, num_pieces );
#    } else {
#        run_test_pieces_split( srcfiles, out_file, num_pieces, piece_num );
#    }
#}
#
#void run_test_pieces_merge( string_t out_file, uint_t num_pieces ) {
#    std::cout << out_file << " merge" << std::endl;
#    
#    string_vec_t srcfiles_complete;
#    string_vec_t srcfiles_matrix;
#    string_vec_t srcfiles_matrixj;
#    
#    for ( uint_t piece_num = 0; piece_num < num_pieces; ++piece_num ) {
#        string_t name_complete = (boost::format("%s_%04d_%04d%s") % out_file % piece_num % num_pieces % EXT_COMPLETE).str();
#        std::cout << "adding " << name_complete << " to merging" << std::endl;
#        srcfiles_complete.push_back( name_complete );
#        
#        string_t name_matrix = (boost::format("%s_%04d_%04d%s") % out_file % piece_num % num_pieces % EXT_MATRIX    ).str();
#        std::cout << "adding " << name_matrix << " to merging" << std::endl;
#        srcfiles_matrix.push_back( name_matrix );
#        
#        string_t name_matrixj = (boost::format("%s_%04d_%04d%s") % out_file % piece_num % num_pieces % EXT_JMATRIX  ).str();
#        std::cout << "adding " << name_matrixj << " to merging" << std::endl;
#        srcfiles_matrixj.push_back( name_matrixj );
#    }
#    
#    merge_complete( out_file, srcfiles_complete );
#    //merge_complete_parallel( out_file, srcfiles_complete );
#    merge_matrix(   out_file, srcfiles_matrix   );
#    merge_matrixj(  out_file, srcfiles_matrixj  );
#}
#
#void run_test_pieces_split( string_vec_t srcfiles, string_t out_file, uint_t num_pieces, uint_t piece_num ) {
#    std::cout << out_file << std::endl;
#    std::cout << out_file << " :: reading jf test 2" << std::endl;
#    progressBar progressl1("read jf " + out_file, 0, 1000);
#    progressl1.print( 1 );
#
#    baseInt  num_threads     =   1;
#    baseInt  minVal          =   2;
#    baseInt  save_every      =   1;
#    //baseInt  save_every      =   100000;
#    bool     export_complete =  true;
#    bool     export_summary  = false;
#    bool     export_matrix   =  true;
#    boost::recursive_mutex g_guard_s;
#
#    
#    piece_data_vec_t pieces;
#    
#    string_t   name = (boost::format("%s_%04d_%04d") % out_file % piece_num % num_pieces).str();
#    
#    piece_data d    = piece_data( srcfiles, name, num_threads, minVal, save_every, export_complete, export_summary, export_matrix, num_pieces, piece_num, new merge_jfs( srcfiles, name ), &g_guard_s );
#    
#    send_piece( d );
#    
#    progressl1.print( 500 );
#
#    std::cout << out_file << " :: exporting" << std::endl;
#
#    d.merger->save_all( name );
#    
#    progressl1.print( 1000 );
#
#    std::cout << out_file << " :: read jf test 2 FINISHED" << std::endl;
#}
#
#void test1( uint_t num_pieces, uint_t piece_num ) {
#    string_vec_t srcfiles;
#    string_t     outfile = "test1";
#    
#    {
#        srcfiles.push_back( "/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/Arabidopsis_lyrata.fasta.31.jf" );
#        srcfiles.push_back( "/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/Arabidopsis_thaliana_TAIR10_genome.fas.31.jf" );
#        srcfiles.push_back( "/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/Citrus_sinensis.fasta.31.jf" );
#        srcfiles.push_back( "/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/Glycine_max.fasta.31.jf" );
#        srcfiles.push_back( "/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/Malus_domestica.fasta.31.jf" );
#        srcfiles.push_back( "/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/Nicotiana_benthamiana_Niben.genome.v0.4.4.scaffolds.nrcontigs.fasta.31.jf" );
#        srcfiles.push_back( "/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/Nicotiana_tabacum_tobacco_genome_sequences_assembly.fasta.31.jf" );
#        srcfiles.push_back( "/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/Oryza_brachyantha.fasta.31.jf" );
#        srcfiles.push_back( "/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/Oryza_sativa_build_5.00_IRGSPb5.fa.31.jf" );
#        srcfiles.push_back( "/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/Populus_trichocarpa.fasta.31.jf" );
#        srcfiles.push_back( "/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/S_lycopersicum_chromosomes.2.40.fa.31.jf" );
#        srcfiles.push_back( "/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/Solanum_peruvianum_Speru_denovo.fa.31.jf" );
#        srcfiles.push_back( "/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/Solanum_tuberosum_PGSC_DM_v3_superscaffolds.fasta.31.jf" );
#        srcfiles.push_back( "/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/Spimpinellifolium_genome.contigs.fasta.31.jf" );
#        srcfiles.push_back( "/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/Vitis_vinifera_Genoscope_12X_2010_02_12_scaffolds.fa.31.jf" );
#        srcfiles.push_back( "/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/Zea_mays.fasta.31.jf" );
#    }
#    
#    run_test_pieces( srcfiles, outfile, num_pieces, piece_num );
#    //run_test_single( srcfiles, outfile );
#}





