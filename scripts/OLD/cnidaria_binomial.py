#!/usr/bin/python
import copy
import math

#http://en.wikipedia.org/wiki/Combinatorial_number_system

class binomialCombination(object):
    def __init__(self, numFields, sampleSize, verbose=False):
        self.sampleSize  = sampleSize
        self.numFields = numFields
        self.binKeys    = []
        self.verbose    = verbose
        print "creating binomial keys"
        self.genBinKeys(verbose=self.verbose)
        print "binomial keys created"

    def genBinKeys(self, verbose=False):
        for nsize in xrange(self.sampleSize + 1):
            if verbose:
                print "nsize", nsize
                
            self.binKeys.append([0]*(self.numFields+2))
            for n in xrange(nsize, self.numFields+2):
                if verbose:
                    print "  n", n
                self.binKeys[nsize][n] = self.binomial(n, nsize)
                
        self.binKeys = self.binKeys[::-1]
    
    def binomial(self, numFields, sampleSize):
        up     = math.factorial(numFields             )
        fk     = math.factorial(sampleSize            )
        fnk    = math.factorial(numFields - sampleSize)
        bottom = fk * fnk
        res    = up / bottom
        
        return res

    def getSize(self):
        return self.binomial( self.numFields, self.sampleSize )

    def intFromSeq(self, seq):
        intRes = 0
        
        for pos in range(len(seq)):
            val     = seq[pos]
            brange  = self.binKeys[pos]
            
            bval    = self.binKeys[pos][val]
            intRes += bval
            
        return intRes
    
    def seqFromInt(self, desiredNum, verbose=False):
        desiredNumOrig = desiredNum
        seqRes         = [0]*self.sampleSize
        
        for pos in xrange(self.sampleSize):
            #print "%d => %d :: %s" % (pos, desiredNum, str(binKeys[pos]))
            
            for bpos in xrange(len(self.binKeys[pos])):
                bval = self.binKeys[pos][bpos]
                #print "%d => %d :: %s bpos %d bval %d" % (pos, desiredNum, str(binKeys[pos]), bpos, bval),
                
                if bval > desiredNum:
                    if bpos == 0:
                        seqRes[pos] = 0
                        print
                        break
                    
                    bprev       = self.binKeys[pos][bpos - 1]
                    seqRes[pos] = bpos - 1
                    desiredNum -= bprev
                    #print "* bprev %d bposprev %d rem desired %d" % (bprev, bpos-1, desiredNum)
                    break
                else:
                    #print
                    pass
    
        #print "%7d => %s => %7d" %( desiredNumOrig, str(seqRes), intFromSeq(seqRes) )
        if verbose:
            print "%7d => %s => %7d" % (desiredNumOrig, seqRes, self.intFromSeq(seqRes))
            
        return seqRes
    
    def genCombinations(self, verbose=False, func=None):
        binsize = self.getSize()
        print "bin size", binsize

        print "creating empty"
        combs   = [0]*binsize
        print "created empty"

        print "populating list"
        for pos in xrange( binsize ):
            comb = self.seqFromInt(pos, verbose=verbose)
            
            if func is not None:
                comb = func( comb )
                
            combs[ pos ] = comb
        print "populated list"

        return combs



def main():
    numFields    = 8
    sampleSize   = 5

    print "loading bin keys"
    bc = binomialCombination( numFields, sampleSize, verbose=True )
    print "bin keys loaded"

    for pos in xrange(56):
        seqRes = bc.seqFromInt(pos, verbose=True)
        #print "seqRes", seqRes

    print bc.genCombinations()



if __name__ == '__main__': main()

#T3
#MODE 5 reporting
#MODE 5 +num kmers    : 870325233
#MODE 5 +num val kmers: 86261335
#MODE 5 +num species  : 4
#MODE 5 +sample size  : 3
#MODE 5 +binomial size: (4, 3) = 4
#binomialSize 4
#
#real	5m28.906s
#user	11m18.306s
#sys	0m29.298s
#
#
#
#T1
#MODE 5 reporting
#MODE 5 +num kmers    : 888269592
#MODE 5 +num val kmers: 86592117
#MODE 5 +num species  : 4
#MODE 5 +sample size  : 3
#MODE 5 +binomial size: (4, 3) = 4
#binomialSize 4
#
#
#real	4m52.321s
#user	4m36.737s
#sys	0m13.933s
#
#
#========= BEGIN SPECIES NAMES =========
#out/102_TGRC_TR00026.jf                    : 0 : 2387253995
#out/103_TGRC_TR00027.jf                    : 1 : 2884177275
#out/104_S_galapagense_LA1044_TR00029.jf    : 2 : 2131850385
#out/105_LA1479_Cherry_TGRC_TR00028.jf      : 3 : 1671186440
#========= END SPECIES NAMES =========
#========= BEGIN SPECIES NAMES =========
#out/102_TGRC_TR00026.jf                    : 0 : 2391969230
#out/103_TGRC_TR00027.jf                    : 1 : 2891078540
#out/104_S_galapagense_LA1044_TR00029.jf    : 2 : 2135611975
#out/105_LA1479_Cherry_TGRC_TR00028.jf      : 3 : 1673512540
#========= END SPECIES NAMES =========
#
#
#========= BEGIN COUNT =========
#4
#out/102_TGRC_TR00026.jf                     1352098755   892973305   139686995           0
#out/103_TGRC_TR00027.jf                     1352098755   892973305           0   637599025
#out/104_S_galapagense_LA1044_TR00029.jf     1352098755           0   139686995   637599025
#out/105_LA1479_Cherry_TGRC_TR00028.jf                0   892973305   139686995   637599025
#========= END COUNT =========
#========= BEGIN COUNT =========
#4
#out/102_TGRC_TR00026.jf                     1357211555   895112120   139645555           0
#out/103_TGRC_TR00027.jf                     1357211555   895112120           0   638754865
#out/104_S_galapagense_LA1044_TR00029.jf     1357211555           0   139645555   638754865
#out/105_LA1479_Cherry_TGRC_TR00028.jf                0   895112120   139645555   638754865
#========= END COUNT =========
#
#
#========= BEGIN JACCARD =========
#4
#out/102_TGRC_TR00026.jf                       0.566382    0.374059    0.058514    0.000000
#out/103_TGRC_TR00027.jf                       0.468799    0.309611    0.000000    0.221068
#out/104_S_galapagense_LA1044_TR00029.jf       0.634237    0.000000    0.065524    0.299082
#out/105_LA1479_Cherry_TGRC_TR00028.jf         0.000000    0.534335    0.083586    0.381525
#========= END JACCARD =========
#========= BEGIN JACCARD =========
#4
#out/102_TGRC_TR00026.jf                       0.567403    0.374216    0.058381    0.000000
#out/103_TGRC_TR00027.jf                       0.469448    0.309612    0.000000    0.220940
#out/104_S_galapagense_LA1044_TR00029.jf       0.635514    0.000000    0.065389    0.299097
#out/105_LA1479_Cherry_TGRC_TR00028.jf         0.000000    0.534870    0.083445    0.381685
#========= END JACCARD =========
#
#
#========= BEGIN RUSSEL RAO =========
#4
#out/102_TGRC_TR00026.jf                       0.566382    0.374059    0.058514    0.000000
#out/103_TGRC_TR00027.jf                       0.468799    0.309611    0.000000    0.221068
#out/104_S_galapagense_LA1044_TR00029.jf       0.634237    0.000000    0.065524    0.299082
#out/105_LA1479_Cherry_TGRC_TR00028.jf         0.000000    0.534335    0.083586    0.381525
#========= END RUSSEL RAO =========
#========= BEGIN RUSSEL RAO =========
#4
#out/102_TGRC_TR00026.jf                       0.567403    0.374216    0.058381    0.000000
#out/103_TGRC_TR00027.jf                       0.469448    0.309612    0.000000    0.220940
#out/104_S_galapagense_LA1044_TR00029.jf       0.635514    0.000000    0.065389    0.299097
#out/105_LA1479_Cherry_TGRC_TR00028.jf         0.000000    0.534870    0.083445    0.381685
#========= END RUSSEL RAO =========
#
#
#========= BEGIN FOWLKES MALLOWS =========
#4
#out/102_TGRC_TR00026.jf                       0.752584    0.611603    0.241896    0.000000
#out/103_TGRC_TR00027.jf                       0.684689    0.556427    0.000000    0.470179
#out/104_S_galapagense_LA1044_TR00029.jf       0.796390    0.000000    0.255976    0.546884
#out/105_LA1479_Cherry_TGRC_TR00028.jf         0.000000    0.730982    0.289112    0.617677
#========= END FOWLKES MALLOWS =========
#========= BEGIN FOWLKES MALLOWS =========
#4
#out/102_TGRC_TR00026.jf                       0.753262    0.611732    0.241622    0.000000
#out/103_TGRC_TR00027.jf                       0.685163    0.556428    0.000000    0.470043
#out/104_S_galapagense_LA1044_TR00029.jf       0.797191    0.000000    0.255713    0.546897
#out/105_LA1479_Cherry_TGRC_TR00028.jf         0.000000    0.731348    0.288868    0.617807
#========= END FOWLKES MALLOWS =========
#
#
#========= BEGIN COLUMNS NAMES =========
#4
#         0: 1352098755 2.1.0
#         1:  892973305 3.1.0
#         2:  139686995 3.2.0
#         3:  637599025 3.2.1
#========= END COLUMNS NAMES =========
#========= BEGIN COLUMNS NAMES =========
#4
#         0: 1357211555 2.1.0
#         1:  895112120 3.1.0
#         2:  139645555 3.2.0
#         3:  638754865 3.2.1
#========= END COLUMNS NAMES =========
#Main program exiting.
#deleting binomial tree
#




##7x5
#data = [
#            [0,	1,	2,	3,	4],
#            [0,	1,	2,	3,	5],
#            [0,	1,	2,	3,	6],
#            [0,	1,	2,	4,	5],
#            [0,	1,	2,	4,	6],
#            [0,	1,	2,	5,	6],
#            [0,	1,	3,	4,	5],
#            [0,	1,	3,	4,	6],
#            [0,	1,	3,	5,	6],
#            [0,	1,	4,	5,	6],
#            [0,	2,	3,	4,	5],
#            [0,	2,	3,	4,	6],
#            [0,	2,	3,	5,	6],
#            [0,	2,	4,	5,	6],
#            [0,	3,	4,	5,	6],
#            [1,	2,	3,	4,	5],
#            [1,	2,	3,	4,	6],
#            [1,	2,	3,	5,	6],
#            [1,	2,	4,	5,	6],
#            [1,	3,	4,	5,	6],
#            [2,	3,	4,	5,	6]
#        ]

#8x5
#data = [
#            [0,	1,	2,	3,	4],
#            [0,	1,	2,	3,	5],
#            [0,	1,	2,	3,	6],
#            [0,	1,	2,	3,	7],
#            
#            [0,	1,	2,	4,	5],
#            [0,	1,	2,	4,	6],
#            [0,	1,	2,	4,	7],
#            
#            [0,	1,	2,	5,	6],
#            [0,	1,	2,	5,	7],
#            
#            [0,	1,	2,	6,	7],
#            
#            [0,	1,	3,	4,	5],
#            [0,	1,	3,	4,	6],
#            [0,	1,	3,	4,	7],
#
#            [0,	1,	3,	5,	6],
#            [0,	1,	3,	5,	7],
#            
#            [0,	1,	4,	5,	6],
#            
#            [0,	1,	4,	5,	7],
#
#            [0,	1,	4,	6,	7],
#            
#            [0,	1,	5,	6,	7],#19
#
#            [0,	2,	3,	4,	5],
#            [0,	2,	3,	4,	6],
#            [0,	2,	3,	4,	7],
#
#            [0,	2,	3,	5,	6],
#            [0,	2,	3,	5,	7],
#
#            [0,	2,	3,	6,	7],
#
#            [0,	2,	4,	5,	6],
#            [0,	2,	4,	5,	7],
#            [0,	2,	4,	6,	7],
#            
#            [0,	3,	4,	5,	6],
#            [0,	3,	4,	5,	7], #30
#
#            [0,	3,	4,	6,	7],
#
#            [1,	2,	3,	4,	5],
#            [1,	2,	3,	4,	6],
#            [1,	2,	3,	4,	7],
#
#            [1,	2,	3,	5,	6],
#            [1,	2,	3,	5,	7],
#            [1,	2,	3,	6,	7],
#
#            [1,	2,	4,	5,	6],
#            [1,	2,	4,	5,	7],
#            
#            [1,	2,	4,	6,	7],#40
#
#            [1,	2,	5,	6,	7],
#
#            [1,	3,	4,	5,	6],
#            [1,	3,	4,	5,	7],
#            [1,	3,	4,	6,	7],
#
#            [1,	3,	5,	6,	7],
#
#            [1,	4,	5,	6,	7],
#
#            [2,	3,	4,	5,	6],
#            [2,	3,	4,	5,	7],
#            
#            [2,	3,	5,	6,	7],
#            
#            [2,	4,	5,	6,	7],
#
#            [3,	4,	5,	6,	7],
#        ]
