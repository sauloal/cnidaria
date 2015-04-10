#!/usr/bin/python
import os, sys
import time
import copy
import math


print " cnidaria stats : importing cnidaria_binomial"
from cnidaria_binomial import binomialCombination
print " cnidaria stats : importing cnidaria_reader"
import cnidaria_reader



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

    
#http://en.wikipedia.org/wiki/Jaccard_index
def adaptive_jaccard_dissimilarity(totalX, totalY, countX, countY, val, a, bC, bT, cC, cT, dC, dT, nC, nT):
    #r  = float( b + c ) / (a + b + c )
    aP = float( a       ) / ( bC + cC )
    bP = float( bC      ) / countX
    cP = float( cC      ) / countY
    r  = float( bP + cP ) / (aP + bP + cP )
    return r

def jaccard_coefficient(        totalX, totalY, countX, countY, val):
    #M11 / (M01 + M10 + M11)
    r  = ( float( val ) / (( countX + countY ) - val ) )
    return r

def jaccard_similarity(         totalX, totalY, countX, countY, val, a, bC, bT, cC, cT, dC, dT, nC, nT):
    r  = 1 - jaccard_dissimilarity(  totalX, totalY, countX, countY, val )
    return r

def jaccard_dissimilarity(      totalX, totalY, countX, countY, val, a, bC, bT, cC, cT, dC, dT, nC, nT):
    r  = float((countX - val)+(countY - val)) / (( countX + countY ) - val )
    return r

def jaccard_similarity2(        totalX, totalY, countX, countY, val, a, bC, bT, cC, cT, dC, dT, nC, nT):
    r  = 1 - jaccard_dissimilarity2( totalX, totalY, countX, countY, val )
    return r

def jaccard_dissimilarity2(     totalX, totalY, countX, countY, val, a, bC, bT, cC, cT, dC, dT, nC, nT):
    #sqrt( 1-Jindex )
    r  = math.sqrt( 1 - jaccard_coefficient( totalX, totalY, countX, countY, val ) )
    return r

def dice_coefficient(           totalX, totalY, countX, countY, val, a, bC, bT, cC, cT, dC, dT, nC, nT):
    #M11 / (M01 + M10 + M11)
    r  = float( 2*val ) / ( countX + countY )
    return r

def jaccard3w_coefficient(      totalX, totalY, countX, countY, val, a, bC, bT, cC, cT, dC, dT, nC, nT):
    #M11 / (M01 + M10 + M11)
    r  = float( 3*val ) / ( countX + countY + val )
    return r

def lance_williams_coefficient( totalX, totalY, countX, countY, val, a, bC, bT, cC, cT, dC, dT, nC, nT):
    #M11 / (M01 + M10 + M11)
    r  = ( countX + countY - val ) / float( countX + countY + val ) 
    return r

def cosine_coefficient(         totalX, totalY, countX, countY, val, a, bC, bT, cC, cT, dC, dT, nC, nT):
    #M11 / (M01 + M10 + M11)
    r  = val / float( countX + countY + val )
    return r

def sorgenfrei_coefficient(     totalX, totalY, countX, countY, val, a, bC, bT, cC, cT, dC, dT, nC, nT):
    #M11 / (M01 + M10 + M11)
    r  = ( val ** 2 ) / float( countX + countY + val )
    return r

def simpson_coefficient(        totalX, totalY, countX, countY, val, a, bC, bT, cC, cT, dC, dT, nC, nT):
    #M11 / (M01 + M10 + M11)
    r  = val / float( min(countX, countY) )
    return r

def braun_banquet_coefficient(  totalX, totalY, countX, countY, val, a, bC, bT, cC, cT, dC, dT, nC, nT):
    #M11 / (M01 + M10 + M11)
    r  = val / float( max(countX, countY) )
    return r

def tanimoto_coefficient(       totalX, totalY, countX, countY, val, a, bC, bT, cC, cT, dC, dT, nC, nT):
    #M11 / (M01 + M10 + M11)
    r  = val / float( countX + countY - val )
    return r

def disperson_coefficient(      totalX, totalY, countX, countY, val, a, bC, bT, cC, cT, dC, dT, nC, nT):
    #M11 / (M01 + M10 + M11)
    r  = ((a*dC)-(bC*cC)) / float( (a+bC+cC+dC)**2 )
    return r

def hamman_coefficient(         totalX, totalY, countX, countY, val, a, bC, bT, cC, cT, dC, dT, nC, nT):
    #M11 / (M01 + M10 + M11)
    r  = ((a+dC)-(bC+cC)) / float( (a+bC+cC+dC) )
    return r

def michael_coefficient(        totalX, totalY, countX, countY, val, a, bC, bT, cC, cT, dC, dT, nC, nT):
    #M11 / (M01 + M10 + M11)
    r  = (4*((a*dC)-(bC*cC))) / float( (((a+dC)**2)+((bC+cC)**2)) )
    return r

def pierce_coefficient(         totalX, totalY, countX, countY, val, a, bC, bT, cC, cT, dC, dT, nC, nT):
    #M11 / (M01 + M10 + M11)
    r  = ( (a*bC) + (bC*cC) ) / float( (a*bC) + (2*(bC*cC)) + (cC*dC) )
    return r

def yule_coefficient(           totalX, totalY, countX, countY, val, a, bC, bT, cC, cT, dC, dT, nC, nT):
    print "yule_coefficient totalX %d totalY %d countX %d countY %d" % (totalX, totalY, countX, countY)
    print "yule_coefficient X %d Y %d" % (totalX-countX, totalY-countY)
    print "yule_coefficient a %d b %d c %d d %d" % (a,bC,cC,dC)
    #M11 / (M01 + M10 + M11)
    r  = (math.sqrt(a*dC) - math.sqrt(bC*cC)) / float((math.sqrt(a*dC) + math.sqrt(bC*cC)))
    return r

def russell_rao_coefficient(    totalX, totalY, countX, countY, val, a, bC, bT, cC, cT, dC, dT, nC, nT):
    #M11 / (M01 + M10 + M11)
    r  = float( a ) / ( a + bC + cC + dC )
    return r

def euclidean_distance(         totalX, totalY, countX, countY, val):
    #http://ramet.elte.hu/~ICF/papers/Jako-BOOL-AN_A_method_for_comparative_sequence_analysis.pdf
    #sqrt( M01 + M10 )
    r  = math.sqrt( ( countX - val ) + ( countY - val ) )
    return r


methods_available = {
    "jaccard_dissimilarity"     : jaccard_dissimilarity,
    "jaccard_dissimilarity2"    : jaccard_dissimilarity2,
    "lance_williams_coefficient": lance_williams_coefficient,
    "disperson_coefficient"     : disperson_coefficient,
    "russell_rao_coefficient"   : russell_rao_coefficient,
    "adaptive_jaccard_dissimilarity": adaptive_jaccard_dissimilarity,
    #"hamman_coefficient"        : hamman_coefficient,
    #"michael_coefficient"       : michael_coefficient,
    #"euclidean_distance"        : euclidean_distance,
    #"jaccard_coefficient"       : jaccard_coefficient,
    #"jaccard_similarity"        : jaccard_similarity,
    #"jaccard_similarity2"       : jaccard_similarity2,
    #"dice_coefficient"          : dice_coefficient,
    #"jaccard3w_coefficient"     : jaccard3w_coefficient,
    #"cosine_coefficient"        : cosine_coefficient,
    #"sorgenfrei_coefficient"    : sorgenfrei_coefficient,
    #"simpson_coefficient"       : simpson_coefficient,
    #"braun_banquet_coefficient" : braun_banquet_coefficient,
    #"tanimoto_coefficient"      : tanimoto_coefficient,
    #"pierce_coefficient"        : pierce_coefficient,
    #"yule_coefficient"          : yule_coefficient,
}
    
def attachMethodName( methodName,  func ):
    print "attaching method", methodName
    if methodName not in methods_available:
        print "unknown method:", methodName
        sys.exit(1)
        
    def ffunc(dissi, x, y, totalX, totalY, countX, countY, val):
        #print "running attached function", methodName
        a  = val
        
        bC = ( countX - val    )
        cC = ( countY - val    )
        
        bT = ( totalX - val    )
        cT = ( totalY - val    )
        
        dC = ( countX - val    ) + ( countY - val    )
        dT = ( totalX - countX ) + ( totalY - countY )
        
        nC = ( countX + countY )
        nT = ( totalX + totalY )
        
        r = func(totalX, totalY, countX, countY, val, a, bC, bT, cC, cT, dC, dT, nC, nT)
        
        dissi[ methodName ][x][y] += r
    
    return ffunc

for methodName in methods_available.keys():
    methods_available[ methodName ] = attachMethodName( methodName, methods_available[ methodName ] )
    


###############
# BASIC FUNCTIONS
###############
class statsfh(object):
    SCALE_NONE          = "no_scale"
    SCALE_FIBONNACCI    = "fibonnacci_scale"
    SCALE_PROPORTIONAL  = "proportional_scale"

    SCALE_BASE_1_1      = "base_1_1_scale"
    SCALE_BASE_1_2      = "base_1_2_scale"
    SCALE_BASE_1_4      = "base_1_4_scale"
    SCALE_BASE_1_6      = "base_1_6_scale"
    SCALE_BASE_1_8      = "base_1_8_scale"
    SCALE_BASE_2_0      = "base_2_0_scale"

    SCALE_POWER_1_1     = "power_1_1_scale"
    SCALE_POWER_1_2     = "power_1_2_scale"
    SCALE_POWER_1_4     = "power_1_4_scale"
    SCALE_POWER_1_6     = "power_1_6_scale"
    SCALE_POWER_1_8     = "power_1_8_scale"
    SCALE_POWER_2_0     = "power_2_0_scale"
    #http://en.wikipedia.org/wiki/Mathematical_constant
    #euler/2 = 2.71828/2 = 1.35914
    #apery's 1.2020569
    #golden
    #Euler Mascheroni  1.61803398874
    #conway 1.30357
    #Khinchin's 2.6854520010
    #sqrt(3)
    #plastic constant 1.32471 79572 44746 02596 09088 54478 09734

    def __init__(self, infile, scaleType=SCALE_NONE):
    #def __init__(self, infile, scaleType=SCALE_FIBONNACCI):
        self.infile                             = infile
        
        self.jfinst                             = cnidaria_reader.reader(infile)
        
        self.filetype                           = self.jfinst.getKey( "filetype"           )
        self.speciesNames                       = self.jfinst.getKey( "filenames"          )
        self.speciesPosition                    = {}
        for sppPos, sppName in enumerate( self.speciesNames ):
            self.speciesPosition[ sppName ] = sppPos
        
        self.speciesCount                       = {}
        self.speciesCount["Total"]              = {}
        self.speciesCount["Valid"]              = {}
        
        self.speciesCount["Total"]["Raw"]       = self.jfinst.getKey( "num_kmer_total_spp" )
        self.speciesCount["Valid"]["Raw"]       = self.jfinst.getKey( "num_kmer_valid_spp" )

        self.speciesCount["Total"]["Weighted"]  = copy.deepcopy( self.speciesCount["Total"]["Raw"] )
        self.speciesCount["Valid"]["Weighted"]  = copy.deepcopy( self.speciesCount["Valid"]["Raw"] )

        self.numSpps                            = len( self.speciesNames )
        
        self.scaleType                          = scaleType
        self.scale                              = None

        self.genScale()
        
        self.matrix                             = {}
        self.matrix["_original_"]               = None
        self.matrix["Raw"]                      = None
        self.matrix["Weighted"]                 = None
        
        

        
        #derived values
        #self.complex        = {}
        
        #const static string_t FMT_COMPLETE = "cnidaria/complete";
        #const static string_t FMT_SUMMARY  = "cnidaria/summary";
        #const static string_t FMT_MATRIX   = "cnidaria/matrix";
        if   ( self.filetype == "cnidaria/complete" ):
            #readComplete()
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
            
            
            
        self.applyMatrixWeight()

    def genScale(self):
        self.scale   = [None] * self.numSpps
        if   self.scaleType == self.SCALE_NONE:
            for x in xrange(len(self.scale)):
                self.scale[x]  = 1



        elif self.scaleType == self.SCALE_FIBONNACCI:
            lastVal = 1
            for x in xrange(len(self.scale)):
                self.scale[x]  = lastVal
                lastVal       += lastVal
            
            self.scale.reverse()
            print "SCALE FIBONNACCI", self.scale


        elif self.scaleType == self.SCALE_BASE_1_1:
            for x in xrange(len(self.scale)):
                self.scale[x]  = int( 1.1 ** x )

            self.scale.reverse()
            print "SCALE BASE_1_1", self.scale

        elif self.scaleType == self.SCALE_BASE_1_2:
            for x in xrange(len(self.scale)):
                self.scale[x]  = int( 1.2 ** x )

            self.scale.reverse()
            print "SCALE BASE_1_2", self.scale
        
        elif self.scaleType == self.SCALE_BASE_1_4:
            for x in xrange(len(self.scale)):
                self.scale[x]  = int( 1.4 ** x )

            self.scale.reverse()
            print "SCALE BASE_1_4", self.scale
        
        elif self.scaleType == self.SCALE_BASE_1_6:
            for x in xrange(len(self.scale)):
                self.scale[x]  = int( 1.6 ** x )

            self.scale.reverse()
            print "SCALE BASE_1_6", self.scale
            
        
        elif self.scaleType == self.SCALE_BASE_1_8:
            for x in xrange(len(self.scale)):
                self.scale[x]  = int( 1.8 ** x )

            self.scale.reverse()
            print "SCALE BASE_1_8", self.scale
            
        
        elif self.scaleType == self.SCALE_BASE_2_0:
            for x in xrange(len(self.scale)):
                self.scale[x]  = int( 2.0 ** x )

            self.scale.reverse()
            print "SCALE BASE_2_0", self.scale




        elif self.scaleType == self.SCALE_POWER_1_1:
            for x in xrange(len(self.scale)):
                self.scale[x]  = int( x ** 1.1 )

            self.scale.reverse()
            print "SCALE POWER_1_1", self.scale
            
        elif self.scaleType == self.SCALE_POWER_1_2:
            for x in xrange(len(self.scale)):
                self.scale[x]  = int( x ** 1.2 )

            self.scale.reverse()
            print "SCALE POWER_1_2", self.scale
        
        elif self.scaleType == self.SCALE_POWER_1_4:
            for x in xrange(len(self.scale)):
                self.scale[x]  = int( x ** 1.4 )

            self.scale.reverse()
            print "SCALE POWER_1_4", self.scale
        
        elif self.scaleType == self.SCALE_POWER_1_6:
            for x in xrange(len(self.scale)):
                self.scale[x]  = int( x ** 1.6 )

            self.scale.reverse()
            print "SCALE POWER_1_6", self.scale
        
        elif self.scaleType == self.SCALE_POWER_1_8:
            for x in xrange(len(self.scale)):
                self.scale[x]  = int( x ** 1.8 )

            self.scale.reverse()
            print "SCALE POWER_1_8", self.scale
        
        elif self.scaleType == self.SCALE_POWER_2_0:
            for x in xrange(len(self.scale)):
                self.scale[x]  = int( x ** 2.0 )

            self.scale.reverse()
            print "SCALE POWER_2_0", self.scale


            
        elif self.scaleType == self.SCALE_PROPORTIONAL:
            #prop = float(31) / self.numSpps
            prop = (2 ** 31) / self.numSpps
            for x in xrange(len(self.scale)):
                #ind = (x*prop)
                #self.scale[x]  = int(2 ** ind)
                self.scale[x]  = x * prop

            self.scale.reverse()
            print "SCALE PROPORTIONAL", self.scale
            
        else:
            print "scale:", self.scaleType, "not implemented"

    def readMatrix(self):
        print "getting matrix",
        lst = self.jfinst.getAll()
        
        self.matrix["_original_"] = copy.deepcopy( lst )
        self.matrix["Raw"]        = copy.deepcopy( lst )
        self.matrix["Weighted"]   = copy.deepcopy( lst )
        
        #for x in xrange(len(self.matrix["Raw"]   )):
        #    print "%2d"%x, ''.join( [ "%7d" % y for y in self.matrix["Raw"]   [x] ] )
        
        print "done"

    def applyMatrixWeight( self ):
        for x in xrange(len(self.speciesCount["Valid"]["Weighted"])):
            self.speciesCount["Valid"]["Weighted"][x] = 0
        
        for x in xrange(len(self.matrix["Raw"])):
            for y in xrange(len(self.matrix["Raw"])):
                #print "b x", x, "y", y, self.matrix["Weighted"][x][y]
                #print "x %3d y %3d ov %12d" % (x, y, sum( lst[x][y] )),

                for z in xrange(len(self.matrix["Raw"])):
                    ov = self.matrix["Raw"][x][y][z]
                    sc = self.scale[z]
                    nv = ov * sc
                    
                    #print "x %6d y %6d z %6d ov %6d sc %6d nv %12d w %12d" % (x, y, z, ov, sc, nv, nv*z)
                    
                    self.matrix["Weighted"][x][y][z] = nv
                    
                    if y < x:
                        self.speciesCount["Valid"]["Weighted"][ x ] += nv
                        self.speciesCount["Valid"]["Weighted"][ y ] += nv
                    
                #print "a x", x, "y", y, self.matrix["Weighted"][x][y]

                self.matrix["Raw"]     [x][y] = sum( self.matrix["Raw"]     [x][y] )
                #print "c x", x, "y", y, self.matrix["Weighted"][x][y]
                self.matrix["Weighted"][x][y] = sum( self.matrix["Weighted"][x][y] )

                #print "s x", x, "y", y, self.matrix["Weighted"][x][y]
                #print

        #for x in xrange(len(self.matrix["Raw"]   )):
        #    for y in xrange(x, len(self.matrix["Raw"]   )):
        #        self.matrix["Raw"]   [y][x] = self.matrix["Raw"]   [x][y]


        print "upd total raw     ", ''.join( [ "%11d"%x for x in self.speciesCount["Total"]["Raw"]      ] )
        print "upd total weighted", ''.join( [ "%11d"%x for x in self.speciesCount["Total"]["Weighted"] ] )
        print "upd valid raw     ", ''.join( [ "%11d"%x for x in self.speciesCount["Valid"]["Raw"]      ] )
        print "upd valid weighted", ''.join( [ "%11d"%x for x in self.speciesCount["Valid"]["Weighted"] ] )

    def createDataFrame(self):
        print "CREATING DATA FRAME"
        self.df = pd.DataFrame(self.complex)
        print "CREATED"



def calcDistance(stats, methods=methods_available.keys(), matrixValue="Valid", matrixType="Weighted"):
    #part, maxNameLen, diss, data
    print "CALCULATING DISTANCE ... creating empty"
    

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
    print "CALCULATING DISTANCE ... converting ... ANALYSIS",analysisName

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
        
        print "PRINTING DISTANCE ... ANALYSIS:", analysisName, "FILE", outfn
        
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
        mfh.write( "%s\t" % names[ x ] )
        
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



def readFilesTitles(filetitles, stats):
    with open(filetitles, 'r') as fhd:
        for line in fhd:
            line = line.strip()
            
            if len(line) == 0:
                continue
            
            if line[0] == '#':
                continue
            
            try:
                fname, fnewname = line.split("\t")[:2]
                fname    = fname.strip()
                fnewname = fnewname.strip()
            
            except:
                print "error parsing line", line
                sys.exit(1)
            
            if fname in stats.speciesPosition:
                print "renaming", fname, "to", fnewname
                pos = stats.speciesPosition[ fname ]
                stats.speciesNames[ pos ] = fnewname
                stats.speciesPosition[ fnewname ] = pos
                del stats.speciesPosition[ fname ]
                
            else:
                #print "name %s not present" % fname
                pass



def exportMatrices(infile, matrices, stats):
    trees = [
                [ "nj"   , nj.nj ],
                #[ "upgma", upgma ],
                #[ "ml", maximum_likelihood. ], # http://pycogent.org/cookbook/using_likelihood_to_perform_evolutionary_analyses.html
            ]
    
    for analysisName in matrices:
        print "EXPORTING METHOD",analysisName

        matrix  = matrices[ analysisName ]
        
        for treeName, treeFunc in trees:
            print "EXPORTING METHOD",analysisName, " TREE ", treeName
    
            outbase  = infile  + "." + stats.scaleType + "." + analysisName
            treeBase = outbase + "." + treeName
            
            mytree   = treeFunc( matrix )
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




def main():
    try:
        infile = sys.argv[1]
        
    except:
        print "no input file given"
        sys.exit(1)


    try:
        filetitles = sys.argv[2]
        
    except:
        filetitles = None
        print "no input file titles given"

    methods = methods_available.keys()

    processBin( infile, filetitles=filetitles, scaleType=statsfh.SCALE_NONE       , methods=methods )
    #processBin( infile, filetitles=filetitles, scaleType=statsfh.SCALE_FIBONNACCI , methods=methods )
    #processBin( infile, filetitles=filetitles, scaleType=statsfh.SCALE_POWER2     , methods=methods )
    
    processBin( infile, filetitles=filetitles, scaleType=statsfh.SCALE_POWER_1_1  , methods=methods )
    #processBin( infile, filetitles=filetitles, scaleType=statsfh.SCALE_POWER_1_2  , methods=methods )
    #processBin( infile, filetitles=filetitles, scaleType=statsfh.SCALE_POWER_1_4  , methods=methods )
    #processBin( infile, filetitles=filetitles, scaleType=statsfh.SCALE_POWER_1_6  , methods=methods )
    #processBin( infile, filetitles=filetitles, scaleType=statsfh.SCALE_POWER_1_8  , methods=methods )
    processBin( infile, filetitles=filetitles, scaleType=statsfh.SCALE_POWER_2_0  , methods=methods )
    
    #processBin( infile, filetitles=filetitles, scaleType=statsfh.SCALE_BASE_1_1   , methods=methods )
    #processBin( infile, filetitles=filetitles, scaleType=statsfh.SCALE_BASE_1_2   , methods=methods )
    #processBin( infile, filetitles=filetitles, scaleType=statsfh.SCALE_BASE_1_4   , methods=methods )
    #processBin( infile, filetitles=filetitles, scaleType=statsfh.SCALE_BASE_1_6   , methods=methods )
    #processBin( infile, filetitles=filetitles, scaleType=statsfh.SCALE_BASE_1_8   , methods=methods )
    #processBin( infile, filetitles=filetitles, scaleType=statsfh.SCALE_BASE_2_0   , methods=methods )
    
    #processBin( infile, filetitles=filetitles, scaleType=statsfh.SCALE_PROPORTIONAL )


def processBin( infile, filetitles=None, scaleType=statsfh.SCALE_NONE, methods=methods_available.keys() ):
    if not os.path.exists(infile):
        print "input file %s does not exists" % infile
    

    if ( filetitles is not None ) and ( not os.path.exists( filetitles ) ):
        print "input file titles given %s but file does not exists" % (filetitles)
        sys.exit(1)

    print "READING FILE"
    stats = statsfh(infile, scaleType=scaleType)
    print "READING FILE ... done"

    

    print "CALCULATING DISTANCE"
    dissi = calcDistance( stats, methods=methods )
   
    print "CALCULATING DISTANCE ... done"
    


    print "PRINTING DISTANCE"
    if filetitles is not None:
        newFilesTitles = readFilesTitles(filetitles, stats)

    printDissi( stats, dissi, infile )
    print "PRINTING DISTANCE .. done"


    print "CONVERTING MATRIX"

    matrices = dissi2dissimatrix(dissi, stats)
    print "CONVERTING MATRIX ... done"

    #print matrices
    #sys.exit(0)
    
    print "EXPORTING NJ"
    exportMatrices(infile, matrices, stats)

    print "EXPORTING NJ ... done"

if __name__ == '__main__':
    main()


