import os
import sys
import copy
import struct

print " cnidaria reader: importing simplejson"
import simplejson   


#FILE FORMATS:
#    cne - cnidaria extended
#        8 bytes           -> JSON BEGIN POSITION IN BYTES
#        <registers>       -> total length = <JSON BEGIN POSITION IN BYTES> - 8 bytes
#           k/4 bytes      -> kmer sequence of size k (defined in json) divided by 4 with 1 bits per nucleotide
#           n bytes        -> binary combination of size ((#species / 8) + (#species % 8))
#        8 bytes           -> @<JSON BEGIN POSITION IN BYTES> json size in bytes
#        <json size> bytes -> json string
#
#   cns - cnidaria summary
#        8 bytes           -> json size in bytes
#        <json size> bytes -> json string
#       <summary>
#           n bytes        -> binary combination of size ((#species / 8) + (#species % 8))
#           8 bytes        -> count
#        8 bytes           -> num combinations
#
#   cnm - cnidaria matrix
#        8 bytes           -> json size in bytes
#        <json size> bytes -> json string
#       <matrix>
#           8 bytes * (<#species> ^ 3) -> <#species> defined in json

#{"num_infiles":16,"num_combinations":0,"extended_registers":663292544,"min_val":2,"max_val":16,"save_every":1,"num_pieces":10,"piece_num":0,"kmerSize":31,"version":2,"filetype":"cnidaria/complete","filenames":["/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/Arabidopsis_lyrata.fasta.jf","/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/Arabidopsis_thaliana_TAIR10_genome.fas.jf","/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/Citrus_sinensis.fasta.jf","/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/Glycine_max.fasta.jf","/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/Nicotiana_benthamiana_Niben.genome.v0.4.4.scaffolds.nrcontigs.fasta.jf","/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/Nicotiana_tabacum_tobacco_genome_sequences_assembly.fasta.jf","/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/Oryza_brachyantha.fasta.jf","/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/Oryza_sativa_build_5.00_IRGSPb5.fa.jf","/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/Populus_trichocarpa.fasta.jf","/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/S_lycopersicum_chromosomes.2.40.fa.jf","/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/Solanum_peruvianum_CSH_transcriptome.fasta.jf","/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/Solanum_peruvianum_Speru_denovo.fa.jf","/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/Solanum_tuberosum_PGSC_DM_v3_superscaffolds.fasta.jf","/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/Spimpinellifolium_genome.contigs.fasta.jf","/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/Vitis_vinifera_Genoscope_12X_2010_02_12_scaffolds.fa.jf","/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/Zea_mays.fasta.jf"],"num_kmer_total_spp":[14348170,11191356,23450061,67748213,194503738,29386103,22744214,29667325,26269014,62734646,2753697,2407154,54653650,60799987,37266124,81363815],"num_kmer_valid_spp":[1061041,1068334,96095,149042,4830934,4210387,516760,549894,94130,51280756,6998415,6342016,7706158,51193202,138678,171844]}



class readBin(object):
    INT_SIZE    = 8
    DOUBLE_SIZE = 8
    
    def __init__( self, filename, intype='filename' ):
        if   intype == 'filename':
            self.filename = filename
            try:
                self.filehand = open(filename, "rb")
            except:
                sys.exit(1)
        
        elif intype == 'filehandle':
            self.filename = 'filehandle'
            self.filehand = filename
        
        else:
            print "unknown in type:", intype, ". acceptable values are filename and filehandle"
            sys.exit(1)

    
    def Seek(self, pos):
        self.filehand.seek(pos)
    
    def Tell(self):
        return self.filehand.tell()
    
    def Double( self ):
        num = self.filehand.read(self.DOUBLE_SIZE)
        return struct.unpack("d", num)[0]
    
    def Int( self ):
        num = self.filehand.read(self.INT_SIZE)
        return struct.unpack("Q", num)[0]
    
    def Raw( self, siz ):
        name = self.filehand.read(siz)
        return "".join( struct.unpack("c"*siz, name) )
    
    def Name( self, siz ):
        size = self.Int()
        name = self.Raw(siz)
        return name[:siz]
    
    def Str(self, siz):
        name = self.Raw(siz)
        return name[:siz]
    


class reader(object):
    VALID_EXTENSIONS = [ [ 'cne', 'bin/end' ], [ 'cnm', 'bin/begin' ], [ 'cns', 'bin/begin' ], [ 'json', 'json' ] ]

    def __init__(self, infile, verbosiy=5):
        print "starting"

        print "opening", infile
        
        self.infile            = infile
        self.filesize          = os.stat( infile ).st_size

        self.json              = None
        self.jsonPos           = None
        self.jsonSize          = None
        self.opts              = []
        self.currPos           = 0
        
        self.verbosiy          = verbosiy
        
        if not any( [ infile.endswith(x[0]) for x in self.VALID_EXTENSIONS ] ):
            print "input file %s does not have a valid extension" % ( infile )
            print "options are:", ", ".join( [x[0] for x in self.VALID_EXTENSIONS] )
            sys.exit( 1 )
        
        for data in self.VALID_EXTENSIONS:
            if infile.endswith( data[0] ):
                self.reader( data )
                self.load()
                break
        

    def reader(self, data):
        if data[1] in [ 'bin/begin', 'bin/end' ]:
            self.loadbin( data[1] )
            
        elif data[1] == 'json':
            self.loadjsonfile( self.infile )
            
        else:
            print "data type %s not implemented" % data[1]
            sys.exit(1)

    def loadbin(self, data_type):
        self.fhd               = open(    self.infile, 'rb' )
        self.readbin           = readBin( self.fhd, intype='filehandle' )

        if data_type == 'bin/end': #seek end
            self.jsonPos = self.readbin.Int()
            print "  json pos   : ", self.jsonPos
            
            self.readbin.Seek( self.jsonPos )

        self.jsonPos  = self.readbin.Tell()
        self.jsonSize = self.readbin.Int()
        print "  json size  : ", self.jsonSize

        self.offset   = self.jsonSize + self.readbin.INT_SIZE

        jsonstr       = self.readbin.Str( self.jsonSize ).strip('\x00')
    
        if data_type == 'bin/end': #rewind to begining of the file
            self.readbin.Seek( self.readbin.INT_SIZE )
        
        self.loadjsonstr( jsonstr )

    def loadjsonstr(self, jsonstr):
        #self.fhd.read(1) # null terminator

        if self.verbosiy <= 1:
            print "  json string: '%s'" % jsonstr

        try:
            self.json = simplejson.loads( jsonstr )

        except Exception as inst:
            print type(inst)     # the exception instance
            print inst.args      # arguments stored in .args
            print inst           # __str__ allows args to be printed directly:
            print "ERROR PARSING JSON STRING"
            print len(jsonstr)
            print repr(jsonstr)
            print "'"+jsonstr+"'"
            sys.exit( 1 )

    def loadjsonfile(self, jsonfile):
        self.json = simplejson.load( open(jsonfile, 'r') )
    
    def load(self):
        print " opening"

        #o.AddMember( "num_infiles"         , (uint64_t) hd.infiles->size()      , a );
        #o.AddMember( "num_combinations"  , (uint64_t) hd.hash_table->size()   , a );
        #o.AddMember( "extended_registers", (uint64_t) hd.extended_registers   , a );
        #o.AddMember( "min_val"           , (uint64_t) hd.min_val              , a );
        #o.AddMember( "max_val"           , (uint64_t) hd.max_val              , a );
        #o.AddMember( "save_every"        , (uint64_t) hd.save_every           , a );
        #o.AddMember( "num_pieces"        , (uint64_t) hd.num_pieces           , a );
        #o.AddMember( "piece_num"         , (uint64_t) hd.piece_num            , a );
        #o.AddMember( "version"           , (uint_t  ) __CNIDARIA_VERSION__    , a );
        #o.AddMember( "filetype"          ,            filetype                , a );
        #o.AddMember( "filenames"         ,            filenames_j             , a );
        #o.AddMember( "num_kmer_total_spp",            num_kmer_total_spp_j    , a );

        for key in sorted( self.json ):
            print "%-25s"%key
            #print "%-25s"%key, self.json[ key ]
            
            def mkfunc(k):
                def func(self):
                    return self.json[ k ]
                return func
            
            opt = "get_key_" + key
            fc  = mkfunc( key )
            setattr( self, opt, fc )
            self.opts.append( [ opt, key, fc ] )

        #self.Print()

        filetype = self.json["filetype"]
        if   filetype == "cnidaria/complete":
             self.getSize = self.getSizeComplete
             self.getAll  = self.getAllComplete
             self.next    = self.nextComplete
             print "file format", filetype, "not yet implemented"
             sys.exit(1)

        elif filetype == "cnidaria/summary" :
             self.getSize = self.getSizeSummary
             self.getAll  = self.getAllSummary
             self.next    = self.nextSummary
             print "file format", filetype, "not yet implemented"
             sys.exit(1)
            
        elif filetype == "cnidaria/matrix"  :
             self.getSize = self.getSizeMatrix
             self.getAll  = self.getAllMatrix
             self.next    = self.nextMatrix
        
        elif filetype == "cnidaria/json_matrix"  :
             self.getSize = self.getSizeMatrix
             self.getAll  = self.getAllJsonMatrix
             self.next    = self.nextJsonMatrix
        
        else:
            print "unknown file format:", filetype
            sys.exit(1)

        print " opened"

    def getOpts(self):
        return self.opts

    def getKey(self, key):
        if key in self.json:
            return self.json[key]
        
        else:
            return None
        
    def Print(self):
        for opt, key, func in self.opts:
            print " ", "%-25s"%key, func(self)
    
    def getSizeComplete(self):
        pass
    def getSizeSummary(self):
        pass
    def getSizeMatrix(self):
        numInFiles = self.json["num_infiles"]
        return numInFiles * numInFiles * numInFiles
    
    def getHeader(self):
        return self.json
    
    def getAllComplete(self):
        pass
    def getAllSummary(self):
        pass
    def getAllMatrix(self):
        numInFiles = self.json["num_infiles"]
        lst        = [None]*numInFiles
        pos        = 0
        
        for x in xrange(numInFiles):
            lst[x] = [None]*numInFiles
            for y in xrange(numInFiles):
                lst[x][y] = [None]*numInFiles
        
        #for x in xrange(numInFiles):
        #    print x, "c", len(lst[x])
        #    for y in xrange(numInFiles):
        #        print x, y, "c", len(lst[x][y])
        #        for z in xrange(numInFiles):
        #            print x, y, z, "v", lst[x][y][z]

        
        for val in self:
            x = int( ( pos / ( (numInFiles) * (numInFiles) ) ) % numInFiles )
            y = int( ( pos / ( (numInFiles)              )   ) % numInFiles )
            z = int( ( pos                                   ) % numInFiles )

            #print "x %3d y %3d z %3d v %6d p %8d" % ( x, y, z, val, pos + 1 )

            lst[x][y][z] = val
            
            pos += 1

        print "pos      ", pos
        print "max size ", self.getSize()
        
        return lst
        
    def getAllJsonMatrix(self):
        return self.json['matrix']
    
    def hasFinished(self):
        size = self.getSize()
        if self.currPos >= size:
            if self.currPos == size:
                print "cheking file integrity"
                lastVal = self.readbin.Int()
                print " size %d == curr pos %5d == lastVal %5d" % ( self.currPos, size, lastVal )
                assert(lastVal == size)
            return True
        return False

    def __iter__(self):
        return self
    
    def nextComplete(self):
        raise StopIteration
    def nextSummary(self):
        raise StopIteration
    def nextMatrix(self):
        if self.hasFinished():
            raise StopIteration
        
        self.currPos += 1
        
        return self.readbin.Int()
    
    def nextJsonMatrix(self):
        raise StopIteration

    def next(self):
        if   self.json["filetype"] == "cnidaria/complete":
            return self.nextComplete()

        elif self.json["filetype"] == "cnidaria/summary" :
            return self.nextSummary()
            
        elif self.json["filetype"] == "cnidaria/matrix"  :
            return self.nextMatrix()
            
        elif self.json["filetype"] == "cnidaria/json_matrix"  :
            return self.nextJsonMatrix()


def main():
    if len( sys.argv ) != 2:
        print "no input file given"
        sys.exit(1)
    
    infile = sys.argv[1]

    if not os.path.exists( infile ):
        print "input file %s does not exists" % infile
        sys.exit(1)
    
    r = reader( infile )
    r.Print()

if __name__ == '__main__':
    main()
