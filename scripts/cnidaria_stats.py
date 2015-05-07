#!/usr/bin/python
import os, sys
import time
import copy
import math



import cnidaria_reader
from read_titles import readFilesTitles

print " cnidaria stats : importing pandas"
import pandas as pd
print " cnidaria stats : importing numpy"
import numpy  as np
print " cnidaria stats : importing pylab"
import pylab

print " cnidaria stats : importing maptlab"
from matplotlib.pyplot    import show
print " cnidaria stats : importing hcluster"
from hcluster             import pdist, dendrogram
from hcluster             import linkage, single, complete, average, weighted, centroid, median, ward

print " cnidaria stats : importing cogent"
from cogent.phylo         import distance, nj, least_squares, maximum_likelihood
from cogent.cluster.UPGMA import upgma
from cogent.draw          import dendrogram




###############
# DISTANCE METHODS
###############
#//Rand Index
#//          exclusive A + exclusive B
#//  ----------------------------------------
#//  exclusive A + 2x shared AB + exclusive B
#//
#//Jaccard Index
#//                shared AB
#//  -------------------------------------
#//  exclusive A + shared AB + exclusive B
#//
#//Fowlkes_mallows and Mallows
#//      shared AB
#//--------------------------------------------------------
#//sqrt(( shared AB * unique A ) * ( shared AB * unique B))
#//
#//Mirkin Metric
#//2 * ( unique A + unique B )
#//
#//Wallace
#//WAB =      Shared AB
#//      --------------------
#//      Unique A + Shared AB
#//WBA =      Shared AB
#//      --------------------
#//      Unique B + Shared AB


#    1  0
# 1  a  b
# 0  c  d
# n = a + b + c + d


def jaccard_coefficient(        totalX, totalY, countX, countY, val):
    #M11 / (M01 + M10 + M11)
    try:
        r  = ( float( val ) / (( countX + countY ) - val ) )
    except ZeroDivisionError:
        print "jaccard_coefficient: DIVISION BY ZERO"
        print totalX, totalY, countX, countY, val
        sys.exit(0)
    return r

def jaccard_dissimilarity_sqrt(               totalX, totalY, countX, countY, val, exclusiveXCount, exclusiveXTotal, exclusiveYCount, exclusiveYTotal, differenceExclusiveXYCount, sumSharedXY, differenceCountXY, differenceExclusiveXYTotal):
    #sqrt( 1-Jindex )
    r  = math.sqrt( jaccard_dissimilarity(    totalX, totalY, countX, countY, val, exclusiveXCount, exclusiveXTotal, exclusiveYCount, exclusiveYTotal, differenceExclusiveXYCount, sumSharedXY, differenceCountXY, differenceExclusiveXYTotal ) )
    return r

def jaccard_dissimilarity(                    totalX, totalY, countX, countY, val, exclusiveXCount, exclusiveXTotal, exclusiveYCount, exclusiveYTotal, differenceExclusiveXYCount, sumSharedXY, differenceCountXY, differenceExclusiveXYTotal):
    #sqrt( 1-Jindex )
    r  = 1 - jaccard_coefficient( totalX, totalY, countX, countY, val )
    return r


methods_available = {
    "jaccard_dissimilarity_sqrt": jaccard_dissimilarity_sqrt,
    "jaccard_dissimilarity"     : jaccard_dissimilarity,
}
    
def attachMethodName( methodName,  func ):
    print "attaching method", methodName
    if methodName not in methods_available:
        print "unknown method:", methodName
        sys.exit(1)
        
    def ffunc(dissi, x, y, totalX, totalY, countX, countY, val):
        #print "running attached function", methodName
        exclusiveXCount            = ( countX - val    )
        exclusiveYCount            = ( countY - val    )
        
        exclusiveXTotal            = ( totalX - val    )
        exclusiveYTotal            = ( totalY - val    )
        
        differenceExclusiveXYCount = exclusiveXCount + exclusiveYCount
        sumSharedXY                = ( totalX - countX ) + ( totalY - countY )
        
        differenceCountXY          = ( countX + countY )
        differenceExclusiveXYTotal = ( totalX + totalY )
        
        r = func(                               totalX, totalY, countX, countY, val, exclusiveXCount, exclusiveXTotal, exclusiveYCount, exclusiveYTotal, differenceExclusiveXYCount, sumSharedXY, differenceCountXY, differenceExclusiveXYTotal)
        
        #print "dissi method %-30s x %3d y %3d r %.5f totalX %12d totalY %12d countX %12d countY %12d val %12d" % ( methodName, x, y, r, totalX, totalY, countX, countY, val )
        dissi[ methodName ][x][y] += r
    
    return ffunc

for methodName in methods_available.keys():
    methods_available[ methodName ] = attachMethodName( methodName, methods_available[ methodName ] )
    


###############
# BASIC FUNCTIONS
###############
class statsfh(object):
    SCALE_NONE          = "no_scale"

    def __init__(self, infile, scaleType=SCALE_NONE, ignore_file=None):
    #def __init__(self, infile, scaleType=SCALE_FIBONNACCI):
        self.infile                             = infile
        self.ignore_file                        = ignore_file

        self.jfinst                             = cnidaria_reader.reader(infile)
        
        self.filetype                           = self.jfinst.getKey( "filetype"           )
        self.speciesNames                       = self.jfinst.getKey( "in_filenames"       )
        self.speciesPosition                    = {}
        
        self.speciesCount                       = {}
        self.speciesCount["Total"]              = {}
        self.speciesCount["Valid"]              = {}
        
        self.speciesCount["Total"]["Raw"     ]  = self.jfinst.getKey( "num_kmer_total_spp" )
        self.speciesCount["Valid"]["Raw"     ]  = self.jfinst.getKey( "num_kmer_valid_spp" )

        self.speciesCount["Total"]["Weighted"]  = copy.deepcopy( self.speciesCount["Total"]["Raw"] )
        self.speciesCount["Valid"]["Weighted"]  = copy.deepcopy( self.speciesCount["Valid"]["Raw"] )
        
        self.matrix                             = {}
        self.matrix["_original_"]               = None
        self.matrix["Raw"       ]               = None
        self.matrix["Weighted"  ]               = None
        
        

        #derived values
        #self.complex        = {}
        
        #const static string_t FMT_COMPLETE = "cnidaria/complete";
        #const static string_t FMT_SUMMARY  = "cnidaria/summary";
        #const static string_t FMT_MATRIX   = "cnidaria/matrix";
        if   ( self.filetype == "cnidaria/complete" ):
            #readifferenceExclusiveXYCountomplete()
            print "complete file not implemented"
            sys.exit(0)
            pass
        
        elif ( self.filetype == "cnidaria/summary"  ):
            #readSummary()
            print "summary file not implemented"
            sys.exit(0)
            pass
        
        elif ( self.filetype == "cnidaria/matrix"   ):
            self.readMatrix()
        
        elif ( self.filetype == "cnidaria/json_matrix"   ):
            self.readMatrix()
            
        else:
            print "unknown format:", self.filetype
            sys.exit(1)
            

        self.readIgnoreFile()

        for sppPos, sppName in enumerate( self.speciesNames ):
            self.speciesPosition[ sppName ] = sppPos

        self.numSpps                            = len( self.speciesNames )

        self.scaleType                          = scaleType
        self.scale                              = None

        self.genScale()
        self.applyMatrixWeight()

    def genScale(self):
        self.scale   = [None] * self.numSpps
        if   self.scaleType == self.SCALE_NONE:
            for x in xrange(len(self.scale)):
                self.scale[x]  = 1

        else:
            print "scale:", self.scaleType, "not implemented"

    def readMatrix(self):
        print "getting matrix",
        lst = self.jfinst.getAll()
        
        self.matrix["_original_"] = copy.deepcopy( lst )
        self.matrix["Raw"       ] = copy.deepcopy( lst )
        self.matrix["Weighted"  ] = copy.deepcopy( lst )
        
        #for x in xrange(len(self.matrix["Raw"]   )):
        #    print "%2d"%x, ''.join( [ "%7d" % y for y in self.matrix["Raw"]   [x] ] )
        
        print "done"

    def saveCSV(self):
        with open(self.infile + '.csv', 'w') as fhd:
            for spp_pos in xrange(len(self.speciesNames)):
                specie_name = self.speciesNames[ spp_pos ]
                fhd.write("\t%s" % specie_name)
            fhd.write("\n")

            for spp_pos in xrange(len(self.speciesNames)):
                specie_name = self.speciesNames[ spp_pos ]
                row         = self.matrix["_original_"][ spp_pos ]
                fhd.write(specie_name)

                for col in row:
                    val = sum(col)
                    fhd.write("\t%d" % val)
                
                fhd.write("\n")
                
        with open(self.infile + '.count.csv', 'w') as fhd:
            line          = "NAME\tTOTAL\tVALID\tPROP\n"
            print line.strip()
            fhd.write( line )

            for spp_pos in xrange(len(self.speciesNames)):
                specie_name   = self.speciesNames[ spp_pos ]
                species_total = self.speciesCount["Total"]["Raw"][ spp_pos ]
                species_valid = self.speciesCount["Valid"]["Raw"][ spp_pos ]
                
                try:
                    species_prop  = (species_valid * 100.0) / species_total
                except ZeroDivisionError:
                    sys.exit(0)
                    
                line          = "%s\t%d\t%d\t%6.2f\n" % ( specie_name, species_total, species_valid, species_prop )
                print line.strip()
                fhd.write( line )

    def applyMatrixWeight( self ):
        for x in xrange(len(self.speciesCount["Valid"]["Weighted"])):
            self.speciesCount["Valid"]["Weighted"][x] = 0
        
        for x in xrange(len(self.matrix["Raw"])):
            for y in xrange(len(self.matrix["Raw"])):
                #print "b x", x, "y", y, self.matrix["Weighted"][x][y]
                #print "x %3d y %3d ov %12d" % (x, y, sum( lst[x][y] )),

                #for z in xrange(len(self.matrix["Raw"])):
                #    ov = self.matrix["Raw"][x][y][z]
                #    sc = self.scale[z]
                #    nv = ov * sc
                #    
                #    #print "x %6d y %6d z %6d ov %6d sc %6d nv %12d w %12d" % (x, y, z, ov, sc, nv, nv*z)
                #    
                #    self.matrix["Weighted"][x][y][z] = nv
                #    
                #    if y < x:
                #        self.speciesCount["Valid"]["Weighted"][ x ] += nv
                #        self.speciesCount["Valid"]["Weighted"][ y ] += nv
                #    
                #print "a x", x, "y", y, self.matrix["Weighted"][x][y]

                self.matrix["Raw"     ][x][y] = sum( self.matrix["Raw"     ][x][y] )
                #print "c x", x, "y", y, self.matrix["Weighted"][x][y]
                self.matrix["Weighted"][x][y] = sum( self.matrix["Weighted"][x][y] )

                if self.scaleType == self.SCALE_NONE:
                    assert(self.matrix["Raw"][x][y] == self.matrix["Weighted"][x][y])

        if self.scaleType == self.SCALE_NONE:
            self.speciesCount["Valid"]["Weighted"][x] = self.speciesCount["Valid"]["Raw"][ x ]
            assert(self.speciesCount["Valid"]["Raw"][ x ] == self.speciesCount["Valid"]["Weighted"][ x ] )

                #print "s x", x, "y", y, self.matrix["Weighted"][x][y]
                #print

        #for x in xrange(len(self.matrix["Raw"]   )):
        #    for y in xrange(x, len(self.matrix["Raw"]   )):
        #        self.matrix["Raw"]   [y][x] = self.matrix["Raw"]   [x][y]


        print "upd total raw     ", ''.join( [ "%11d"%x for x in self.speciesCount["Total"]["Raw"     ] ] )
        print "upd total weighted", ''.join( [ "%11d"%x for x in self.speciesCount["Total"]["Weighted"] ] )
        print "upd valid raw     ", ''.join( [ "%11d"%x for x in self.speciesCount["Valid"]["Raw"     ] ] )
        print "upd valid weighted", ''.join( [ "%11d"%x for x in self.speciesCount["Valid"]["Weighted"] ] )

    def createDataFrame(self):
        print "CREATING DATA FRAME"
        self.df = pd.DataFrame(self.complex)
        print "CREATED"

    def readIgnoreFile(self):
        if self.ignore_file is None:
            return
        
        print "READING IGNORE FILE"
        
        excludedNames = []
        excludedIds   = []
        with open(self.ignore_file, 'r') as fhd:
            for line in fhd:
                line = line.strip()
                
                if len(line) == 0:
                    continue
                
                if line[0] == '#':
                    continue
                
                if line in self.speciesNames:
                    lid = self.speciesNames.index(line)
                    excludedNames.append( line )
                    excludedIds.append( lid )
                    print "READING IGNORE FILE :: adding '" + line + "' id", lid
                else:
                    print "READING IGNORE FILE :: failed adding '" + line + "' NOT IN TREE"
        
        excludedIds.sort()
        excludedIds.reverse()
        print "READING IGNORE FILE :: ids", excludedIds
        
        for excl in excludedIds:
            del self.speciesNames[ excl ]

            for matrixN in self.matrix:
                matrix = self.matrix[matrixN]
                for x in xrange(len(matrix)):
                    for y in xrange(len(matrix[x])):
                        del matrix[x][y][excl]
                    del matrix[x][excl]
                del matrix[excl]
            
            for countClass in self.speciesCount:
                cls = self.speciesCount[countClass]
                for countType in cls:
                    tpe = cls[countType]
                    del tpe[ excl ]
                    
        print self.speciesNames
        #sys.exit(0)


def calcDistance(stats, methods=methods_available.keys(), matrixValue="Valid", matrixType="Raw"):
    #part, maxNameLen, diss, data
    print "CALCULATING DISTANCE ... creating empty ... MATRIX VALUE", matrixValue,"... MATRIX TYPE", matrixType
    assert(matrixType in stats.matrix)

    names        = stats.speciesNames
    data         = stats.matrix[matrixType]
    analysisName = stats.scaleType
    numSpps      = stats.numSpps
    dissi        = {}


    print "CALCULATING DISTANCE ... creating empty"
    for methodName in methods:
        print "CALCULATING DISTANCE ... creating empty ... METHOD",methodName
        dissi[ methodName ] = [ None ] * numSpps
                
        for x in xrange( numSpps ):
            dissi[ methodName ][ x ] = [ None ] * numSpps
            
            for y in xrange( numSpps ):
                dissi[ methodName ][ x ][ y ] = 0.0

    #print dissi

    print "CALCULATING DISTANCE ... converting"
    print "CALCULATING DISTANCE ... converting ... ANALYSIS",analysisName,"... MATRIX VALUE", matrixValue,"... MATRIX TYPE", matrixType

    for x in xrange( numSpps ):
        totalX   = stats.speciesCount["Total"    ][matrixType][ x ]
        countX   = stats.speciesCount[matrixValue][matrixType][ x ]
        
        for y in xrange( numSpps ):
            totalY   = stats.speciesCount["Total"    ][matrixType][ y ]
            countY   = stats.speciesCount[matrixValue][matrixType][ y ]

            val      = stats.matrix[matrixType][x][y]
            
            for methodName in methods:
                methodFunc = methods_available[methodName]
                methodFunc(dissi, x, y, totalX, totalY, countX, countY, val)
    
    return dissi



def printDissi(stats, dissi, infile):
    #linkages    = []
    #dendrograms = []

    for analysisName in dissi:
        outfn = infile + "." + stats.scaleType + "." + analysisName
        
        print "PRINTING DISTANCE ... ANALYSIS:", analysisName, "SCALE", stats.scaleType, "FILE", outfn
        
        with open( outfn + ".matrix", "w" ) as fhd:
            printMatrix(  dissi[ analysisName ], stats.speciesNames, fhd )
            
            #L = linkage ( dissi[ method ][ analysisName ] )
            #S = single  ( dissi[ method ][ analysisName ] )
            #C = complete( dissi[ method ][ analysisName ] )
            #A = average ( dissi[ method ][ analysisName ] )
            #W = weighted( dissi[ method ][ analysisName ] )
            #E = centroid( dissi[ method ][ analysisName ] )
            #M = median  ( dissi[ method ][ analysisName ] )
            #W = ward    ( dissi[ method ][ analysisName ] )
            
            #linkages.append(    L )
            #print "   LINKAGE", L
            
            #D = dendrogram(     L , labels=[x[0] for x in stats.seiceps])
            #dendrograms.append( D )
            #print "   DENDROGRAM", D
            
            #show( D )
            #pylab.savefig( outfn + ".png" )
            #pylab.cla()



def printMatrix(matrix, names, mfh):
    #mfh.write( "spp\t" )
    mfh.write( "\t" )

    for x in xrange( len( matrix ) ):
        #self.seiceps.append( [ spp_name, spp_size ] )
        mfh.write( "%s\t" % names[ x ] )
        
    mfh.write("\n")
            
    for x in xrange( len( matrix ) ):
        mfh.write( "%s" % names[ x ] )
        
        for y in xrange( len( matrix ) ):
            diss = matrix[ x ][ y ]
            mfh.write( "\t%.10f" % diss )
            
        mfh.write( "\n" )
        
    mfh.write( "\n" )



def dissi2dissimatrix(dissi, stats):
    matrices = {}

    #print "dissi2dissimatrix", names
    for analysisName in dissi:
        #print "dissi2dissimatrix", analysisName
        matrix                   = dissi[ analysisName ]
        matrices[ analysisName ] = {}
        #print "dissi2dissimatrix", analysisName, "matrix", matrix
        
        for x in xrange( len( matrix ) ):
            xName = stats.speciesNames[ x ]
            
            for y in xrange( len( matrix ) ):
                if y > x: continue
                yName = stats.speciesNames[  y ]
                diss  = matrix[ x ][ y ]
                
                pairname = (xName, yName)
                emanriap = (xName, yName)
                #print "dissi2dissimatrix", analysisName, "pairname", pairname
                
                matrices[ analysisName ][ pairname ] = diss
                matrices[ analysisName ][ emanriap ] = diss

    return matrices




def fixTitles( titles, stats ):
    print sorted(stats.speciesPosition.keys())
    print titles
    for fname in stats.speciesPosition:
        for tname in titles:
            if tname in fname:
                fnewname = titles[ tname ]
                print " renaming", fname, "to", fnewname
                pos = stats.speciesPosition[ fname    ]
                stats.speciesNames[          pos      ] = fnewname
                stats.speciesPosition[       fnewname ] = pos
                del stats.speciesPosition[   fname    ]


def exportMatrices(infile, matrices, stats):
    trees = [
                [ "nj"   , nj.nj ],
                [ "upgma", upgma ]
                #[ "ml", maximum_likelihood. ], # http://pycogent.org/cookbook/using_likelihood_to_perform_evolutionary_analyses.html
            ]
    
    for analysisName in matrices:
        print "EXPORTING METHOD",analysisName

        matrix  = matrices[ analysisName ]
        
        for treeName, treeFunc in trees:
            print "EXPORTING METHOD",analysisName, " TREE ", treeName
    
            outbase  = infile  + "." + stats.scaleType + "." + analysisName
            treeBase = outbase + "." + treeName
            
            try:
                mytree   = treeFunc( matrix )
            except AssertionError:
                print "tree with all distances zero"
                sys.exit(0)
            mytree.writeToFile( treeBase , with_distances=True )
            
            with open(treeBase + ".tree", "w") as treeArt:
                treeArt.write( mytree.asciiArt() )
        
        ##for key in matrix:
        ##    print "%s = %.3f" % (str(key), matrix[key])
        #    
        #outbase = infile + "." + stats.scaleType + "." + analysisName
        #
        ##mycluster = upgma( matrix )
        ##mycluster.writeToFile( outbase + ".upgma" )
        ##
        ##with open(outbase + ".upgma.tree", "w") as upgmat:
        ##    upgmat.write( mycluster.asciiArt() )
        #
        ##myclusterden     = dendrogram.ContemporaneousDendrogram( mycluster )
        ##myclusterdendraw = myclusterden.draw()
        #
        #mytree = nj.nj( matrix )
        #mytree.writeToFile(outbase + ".nj", with_distances=True )
        
        #with open(outbase + ".nj.tree", "w") as njt:
        #    njt.write( mytree.asciiArt() )

        #myls = least_squares.WLS(matrix)
        
        #mymll = maximum_likelihood.ML(matrix)



def processBin( infile, filetitles=None, ignore_file=None, scaleType=statsfh.SCALE_NONE, methods=methods_available.keys(), matrixType="Raw" ):
    if not os.path.exists(infile):
        print "input file %s does not exists" % infile
        sys.exit(1)
    


    if ( filetitles is not None ) and ( not os.path.exists( filetitles ) ):
        print "input file titles given %s but file does not exists" % (filetitles)
        sys.exit(1)

    if ( ignore_file is not None ) and ( not os.path.exists( ignore_file ) ):
        print "input file titles given %s but file does not exists" % (ignore_file)
        sys.exit(1)


    print "READING FILE"
    stats = statsfh(infile, scaleType=scaleType, ignore_file=ignore_file)
    print "READING FILE ... done"



    print "PRINTING DISTANCE"
    if filetitles is not None:
        titles = readFilesTitles(filetitles)
        fixTitles( titles, stats )

    stats.saveCSV()


    
    print "CALCULATING DISTANCE"
    dissi = calcDistance( stats, methods=methods, matrixType=matrixType )
    print "CALCULATING DISTANCE ... done"
    
    

    printDissi( stats, dissi, infile )
    print "PRINTING DISTANCE .. done"



    print "CONVERTING MATRIX"
    matrices = dissi2dissimatrix(dissi, stats)
    print "CONVERTING MATRIX ... done"


    
    print "EXPORTING NJ"
    exportMatrices(infile, matrices, stats)
    print "EXPORTING NJ ... done"




def main():
    try:
        infile = sys.argv[1]
        
    except:
        print "no input file given"
        sys.exit(1)


    try:
        filetitles = sys.argv[2]
        print "input file titles given:", filetitles
        
    except:
        filetitles = None
        print "no input file titles given"


    try:
        ignore_file = sys.argv[3]
        print "ignore file given:", ignore_file
        
    except:
        ignore_file = None
        print "no ignore file given"


    methods = methods_available.keys()


    processBin( infile, filetitles=filetitles, ignore_file=ignore_file, scaleType=statsfh.SCALE_NONE       , methods=methods )


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
    
