import os
import sys
import copy
import struct
import functools

print " cnidaria reader: importing simplejson"
import simplejson   
from bitarray import bitarray

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
    
    def __init__( self, filename, intype='filename', block_size=1 ):
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
            
        self.block_size = block_size

    def set_blok_size(self, block_size):
        self.block_size = block_size
    
    def Seek(self, pos):
        self.filehand.seek(pos, 0)
        self.filehand.flush()
    
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
    
    def Block(self):
        return self.filehand.read(self.block_size)

    def Pair(self, s1, s2):
        return self.filehand.read(s1), self.filehand.read(s2)

def memoize(obj):
    max_size  = 100000
    obj.cache = {}

    @functools.wraps(obj)
    def memoizer(*args, **kwargs):
        #key = str(args) + str(kwargs)
        key = args
        
        if key in obj.cache:
            return obj.cache[key]
        
        else:
            if len(obj.cache) > max_size:
                obj.cache = {}
                print "flushing"

            obj.cache[key] = obj(*args, **kwargs)
            
            return obj.cache[key]

        #if args not in obj.cache:
        #    obj.cache[args] = [ obj(*args, **kwargs), 1 ]
        #    #print "\n", len(obj.cache)
        #
        #else:
        #    obj.cache[args][ 1 ] += 1
        #    
        #return obj.cache[args][ 0 ]

    return memoizer

def memoize0(obj):
    max_size  = 100000
    obj.cache = {}

    @functools.wraps(obj)
    def memoizer(*args, **kwargs):
        #key = str(args) + str(kwargs)
        key = args[0]

        v   = obj.cache.get(key, None)
        
        if v is None:
            if len(obj.cache) > max_size:
                obj.cache = {}
                print "flushing"

            v = obj(*args, **kwargs)
            
            obj.cache[key] = v
            
            return v

        else:
            return v

        #if key in obj.cache:
        #    return obj.cache[key]
        #
        #else:
        #    if len(obj.cache) > max_size:
        #        obj.cache = {}
        #        print "flushing"
        #
        #    obj.cache[key] = obj(*args, **kwargs)
        #    
        #    return obj.cache[key]

        #if args not in obj.cache:
        #    obj.cache[args] = [ obj(*args, **kwargs), 1 ]
        #    #print "\n", len(obj.cache)
        #
        #else:
        #    obj.cache[args][ 1 ] += 1
        #    
        #return obj.cache[args][ 0 ]

    return memoizer


def memoize1(obj):
    max_size  = 100000
    obj.cache = {}

    @functools.wraps(obj)
    def memoizer(*args, **kwargs):
        #key = str(args) + str(kwargs)
        key = args[1]
        
        v   = obj.cache.get(key, None)
        
        if v is None:
            if len(obj.cache) > max_size:
                obj.cache = {}
                print "flushing"

            v = obj(*args, **kwargs)
            
            obj.cache[key] = v
            
            return v

        else:
            return v

        
        #if key in obj.cache:
        #    return obj.cache[key]
        #
        #else:
        #    if len(obj.cache) > max_size:
        #        obj.cache = {}
        #        print "flushing"
        #
        #    obj.cache[key] = obj(*args, **kwargs)
        #    
        #    return obj.cache[key]

        #if args not in obj.cache:
        #    obj.cache[args] = [ obj(*args, **kwargs), 1 ]
        #    #print "\n", len(obj.cache)
        #
        #else:
        #    obj.cache[args][ 1 ] += 1
        #    
        #return obj.cache[args][ 0 ]

    return memoizer

class reader(object):
    VALID_EXTENSIONS = [ [ 'cne', 'bin/end' ], [ 'cnm', 'bin/begin' ], [ 'cns', 'bin/begin' ], [ 'json', 'json' ] ]

    def __init__(self, infile, verbose=True, debug=False):
        print "starting"

        print "opening", infile
        
        self.infile            = infile
        self.filesize          = os.stat( infile ).st_size

        self.json              = None
        self.jsonPos           = None
        self.jsonSize          = None
        self.opts              = []
        self.currPos           = 0
        self.currReg           = 0
        
        self.verbose           = verbose
        self.debug             = debug
        
        self.conversionKeys    = {
                'A': bitarray('00'),
                'C': bitarray('01'),
                'G': bitarray('11'),
                'T': bitarray('10')
            }
        
        #self.conversionKeys = {}
        self.conversionKeys = []
        alpha = 'ACGT'
        for k1 in alpha:
            for k2 in alpha:
                k12 = k1 + k2
                for k3 in alpha:
                    k123 = k12 + k3
                    for k4 in alpha:
                        self.conversionKeys.append( k123 + k4 )
                        #self.conversionKeys[chr(len(self.conversionKeys))] = k123 + k4
        #print self.conversionKeys
        
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

        else:
            self.jsonPos  = self.readbin.Tell()
        
        self.jsonSize = self.readbin.Int()
        print "  json size  : ", self.jsonSize

        self.offset   = self.jsonSize + self.readbin.INT_SIZE

        jsonstr       = self.readbin.Str( self.jsonSize ).strip('\x00')
    
        self.lastByte = self.readbin.Tell()
    
        if data_type == 'bin/end': #rewind to begining of the file
            self.readbin.Seek( self.readbin.INT_SIZE )
        
        self.loadjsonstr( jsonstr )

    def loadjsonstr(self, jsonstr):
        #self.fhd.read(1) # null terminator

        if self.verbose:
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
            
        def mkfunc(k):
            def func(self):
                return self.json[ k ]
            return func
        
        for key in sorted( self.json ):
            if self.verbose:
                print "%-25s"%key
            #print "%-25s"%key, self.json[ key ]
            
            opt = "get_key_" + key
            fc  = mkfunc( key )
            
            setattr( self, opt, fc )
            
            self.opts.append( [ opt, key, fc ] )

        #self.Print()
        self.filetype = self.json["filetype"]
        if   self.filetype == "cnidaria/complete":
            self.getSizeBytes    = self.getSizeBytesComplete
            self.getNumRegisters = self.getNumRegistersComplete
            self.getAll          = self.getAllComplete
            self.next            = self.nextComplete
            
            self.block_bytes     = self.json['block_bytes'       ]
            self.kmer_size       = self.json['kmer_size'         ]
            self.kmer_bytes      = self.json['kmer_bytes'        ]
            self.num_infiles     = self.json['num_infiles'       ]
            self.data_bytes      = self.json['data_bytes'        ]
            self.numRegs         = self.json["complete_registers"]
            
            assert ((self.block_bytes * self.numRegs)+self.readbin.INT_SIZE) == self.jsonPos, "block bytes %12d * num regs %12d (%12d) != json pos %12d" % (self.block_bytes, self.numRegs, (self.block_bytes * self.numRegs), self.jsonPos)

            self.readbin.set_blok_size(self.block_bytes)

            #print self.json
            #print self.readbin.Tell()

        elif self.filetype == "cnidaria/summary" :
            self.getSizeBytes    = self.getSizeBytesSummary
            self.getAll          = self.getAllSummary
            self.next            = self.nextSummary
            print "file format", filetype, "not yet implemented"
            sys.exit(1)
            
        elif self.filetype == "cnidaria/matrix"  :
            self.getBytesSize    = self.getSizeBytesMatrix
            self.getNumRegisters = self.getNumRegistersMatrix
            self.getAll          = self.getAllMatrix
            self.next            = self.nextMatrix
        
        elif self.filetype == "cnidaria/json_matrix"  :
            self.getSize         = self.getSizeMatrix
            self.getAll          = self.getAllJsonMatrix
            self.next            = self.nextJsonMatrix
        
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
    
    def getSizeBytes(self):
        pass
    def getSizeBytesComplete(self):
        return self.json["complete_registers"]*self.block_bytes + self.readbin.INT_SIZE
    def getSizeBytesSummary(self):
        pass
    def getSizeBytesMatrix(self):
        numInFiles = self.json["num_infiles"]
        return numInFiles * numInFiles * numInFiles * self.readbin.INT_SIZE
    
    def getNumRegisters(self):
        pass
    def getNumRegistersComplete(self):
        return self.json["complete_registers"]
    def getNumSizeSummary(self):
        pass
    def getNumSizeMatrix(self):
        numInFiles = self.json["num_infiles"]
        return numInFiles * numInFiles * numInFiles
        
    def getHeader(self):
        return self.json
    
    def getAll(self):
        pass
    def getAllComplete(self):
        return None
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
    
    def parseCompleteRegisterKmer(self, reg):
        char_kmer_bytes = reg[:self.kmer_bytes]
        
        return self.parseCompleteRegisterKmerPiece( char_kmer_bytes )
    
    def parseCompleteRegisterKmerPiece(self, char_kmer_bytes):
        #if self.debug:
        #    print "char_kmer_bytes  ", repr(char_kmer_bytes), len(char_kmer_bytes)
        #    print "char_data_bytes  ", repr(char_data_bytes), len(char_data_bytes)
        
        assert len(char_kmer_bytes) == self.kmer_bytes
        #print '{:b}'.format(char_kmer_bytes)
        #b = bitarray()
        #conversionKeys    = {
        #        'A': bitarray('00'),
        #        'C': bitarray('01'),
        #        'G': bitarray('10'),
        #        'T': bitarray('11')
        #    }
        #b.frombytes(char_kmer_bytes)
        #str_kmer = b.decode(conversionKeys)
        ##str_kmer = b.decode(self.conversionKeys)
        #print "char_kmer_bytes", ''.join(format(ord(x), '08b') for x in char_kmer_bytes)
        #print "bytes          ", b.to01()
        #print "str_kmer bit   ", ''.join(str_kmer)
        
        #str_kmer = [ self.conversionKeys[char_kmer] for char_kmer in char_kmer_bytes ]
        str_kmer = [ self.conversionKeys[ord(char_kmer)] for char_kmer in char_kmer_bytes ]
        #print "str_kmer arr   ", ''.join(str_kmer)
        
        #if self.debug:
        #    print "str_kmer B       ", str_kmer, len(str_kmer)
        
        assert len(str_kmer) == self.kmer_bytes * 4
        str_kmer =          str_kmer[:self.kmer_size]
        str_kmer = "".join( str_kmer )
        
        #if self.debug:
        #    print "str_kmer A       ", str_kmer, len(str_kmer)
        
        assert len(str_kmer) == self.kmer_size
        
        return str_kmer
    
    def parseCompleteRegisterData(self, reg):
        char_data_bytes = reg[self.kmer_bytes:]
        
        return self.parseCompleteRegisterDataPiece(char_data_bytes)
    
    @memoize1
    def parseCompleteRegisterDataPiece(self, char_data_bytes):
        #assert len(char_data_bytes) == self.data_bytes
        
        #print repr(char_data_bytes)
        
        data_bool_array = bitarray()
        data_bool_array.frombytes(char_data_bytes)
        data_bool_array.reverse()
        
        #print data_bool_array
        
        #data_bin_str_lst = [ bin(ord(x)) for x in char_data_bytes ]
        #if dbg:
        #    print "data_bin_str_lst ", data_bin_str_lst
        #data_bool_array  = []
        #for data_bin_str in data_bin_str_lst:
        #    #print [x for x in data_bin_str[2:]]
        #    data_bool_array.extend( [x == '1' for x in data_bin_str[2:]] )
        
        #if self.debug:
        #    print "data_bool_array B", data_bool_array

        assert data_bool_array.length() == self.data_bytes * 8
        data_bool_array = data_bool_array[:self.num_infiles]
        
        #print data_bool_array
        #print
        
        #if self.debug:
        #    print "data_bool_array A", data_bool_array
        
        #assert len(data_bool_array) == num_infiles
        
        return data_bool_array
    
    def parseCompleteRegister(self, reg):
        str_kmer        = self.parseCompleteRegisterKmer(reg)
        data_bool_array = self.parseCompleteRegisterData(reg)
        return (str_kmer, data_bool_array)

    def nextCompleteRegisterKmer(self):
        for d in self:
            yield self.parseCompleteRegisterKmer( d )
    
    def nextCompleteRegisterData(self):
        for d in self:
            yield self.parseCompleteRegisterData( d )
    
    def nextCompleteRegister(self):
        for d in self:
            yield self.parseCompleteRegister( d )

    def goToCompleteRegister(self, reg_num):
        print " seeking register #: %12d" % reg_num
        print " file size         : %12d" % self.filesize
        print " last byte         : %12d" % self.lastByte
        print " JSON pos          : %12d" % self.jsonPos

        reg_coord    = self.block_bytes * reg_num + self.readbin.INT_SIZE

        print " seeking coordinate: %12d bytes" % reg_coord

        assert reg_coord < self.filesize, "register coordinate %12d > end of file %12d" % (reg_coord, self.filesize )
        assert reg_coord < self.jsonPos , "register coordinate %12d > end of data %12d" % (reg_coord, self.jsonPos  )

        print " registers left    : %12d" % ((self.jsonPos - reg_coord) / self.block_bytes)

        self.readbin.Seek(reg_coord)
        
        self.currReg = reg_num
        self.currPos = reg_coord

        print " done seeking.\ncurrent coordinate : %12d bytes" % self.readbin.Tell()
    

    def getAllJsonMatrix(self):
        return self.json['matrix']
    
    def hasFinishedMatrix(self):
        numRegs = self.getNumRegisters()
        if self.currReg >= numRegs:
            if self.currReg == numRegs:
                print "cheking file integrity"
                lastVal = self.readbin.Int()
                print " size %d == curr pos %5d == lastVal %5d" % ( self.currReg, numRegs, lastVal )
                assert(lastVal == size)
            return True
        return False

    def hasFinishedComplete(self):
        #if self.currReg >= self.jsonPos - self.block_bytes:
        if self.currReg >= self.numRegs:
            return False
        return True

    def __iter__(self):
        return self
    
    def nextComplete(self):
        if not self.hasFinishedComplete():
            raise StopIteration
        
        self.currPos += self.block_bytes
        self.currReg += 1
        
        reg         = self.readbin.Block()
        
        #if self.debug:
        #    print "reg              ", repr(reg), len(reg)
        #    print "block_bytes      ", block_bytes
        
        assert len(reg) == self.block_bytes, "register length %d != block bytes %d" % (len(reg), self.block_bytes)
        
        return reg
    
    def nextCompletePair(self):
        while self.hasFinishedComplete():
            self.currPos += self.block_bytes
            self.currReg += 1
            
            kmer, data  = self.readbin.Pair(self.kmer_bytes, self.data_bytes)
            
            if self.debug:
                print "kmer             ", repr(kmer), len(kmer), self.kmer_bytes
                print "data             ", repr(data), len(data), self.data_bytes
            
            #print self.currReg, self.numRegs, self.currReg >= self.numRegs, self.hasFinishedComplete(), self.readbin.Tell(), self.jsonPos, ( ["%3d"%ord(x) for x in kmer], ["%3d"%ord(x) for x in data] )

            assert len(kmer) == self.kmer_bytes, "kmer length %d != kmer bytes %d %s" % (len(kmer), self.kmer_bytes, repr(kmer))
            assert len(data) == self.data_bytes, "data length %d != data bytes %d %s" % (len(data), self.data_byte , repr(data))
            
            yield ( kmer, data )

        print "STOP"
        raise StopIteration

    def nextSummary(self):
        raise StopIteration
    def nextMatrix(self):
        if self.hasFinishedMatrix():
            raise StopIteration
        
        self.currPos += self.readbin.INT_SIZE
        self.currReg += 1
        
        return self.readbin.Int()
    
    def nextJsonMatrix(self):
        raise StopIteration

    def next(self):
        if   self.filetype == "cnidaria/complete":
            self.next = self.nextComplete
            return self.nextComplete()

        elif self.filetype == "cnidaria/summary" :
            self.next = self.nextSummary
            return self.nextSummary()
            
        elif self.filetype == "cnidaria/matrix"  :
            self.next = self.nextMatrix
            return self.nextMatrix()
            
        elif self.filetype == "cnidaria/json_matrix"  :
            self.next = self.nextJsonMatrix
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
