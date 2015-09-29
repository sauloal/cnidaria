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



def pearson_chi_squared(                      totalX, totalY, countX, countY, val, exclusiveXCount, exclusiveXTotal, exclusiveYCount, exclusiveYTotal, differenceExclusiveXYCount, sumSharedXY, differenceCountXY, differenceExclusiveXYTotal):
    #sqrt( 1-Jindex )

    try:
        s  = 0
        #( float( val ) / (( countX + countY ) - val ) )

    except ZeroDivisionError:
        print "jaccard_coefficient: DIVISION BY ZERO"
        print totalX, totalY, countX, countY, val
        sys.exit(0)

    r  = 1 - s

    return r


def pearson_I(                               totalX, totalY, countX, countY, val, exclusiveXCount, exclusiveXTotal, exclusiveYCount, exclusiveYTotal, differenceExclusiveXYCount, sumSharedXY, differenceCountXY, differenceExclusiveXYTotal):
    r = pearson_chi_squared(                 totalX, totalY, countX, countY, val, exclusiveXCount, exclusiveXTotal, exclusiveYCount, exclusiveYTotal, differenceExclusiveXYCount, sumSharedXY, differenceCountXY, differenceExclusiveXYTotal)

    return r


def pearson_II(                              totalX, totalY, countX, countY, val, exclusiveXCount, exclusiveXTotal, exclusiveYCount, exclusiveYTotal, differenceExclusiveXYCount, sumSharedXY, differenceCountXY, differenceExclusiveXYTotal):
    q2 = pearson_chi_squared(                totalX, totalY, countX, countY, val, exclusiveXCount, exclusiveXTotal, exclusiveYCount, exclusiveYTotal, differenceExclusiveXYCount, sumSharedXY, differenceCountXY, differenceExclusiveXYTotal)
    n  = exclusiveXCount + exclusiveYCount
    r  = r#q2 / 

    return r


def attachMethodName( methodName,  func ):
    print "attaching method", methodName
    if methodName not in methods_enabled:
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


def init( methods_to_apply ):
    for m in methods_to_apply:
        if m not in methods_available:
            print " unkknown method %s" % m
            sys.exit(1)

        print "enabling %s method" % m

        methods_enabled[m] = methods_available[m]

    for methodName in methods_enabled.keys():
        methods_enabled[ methodName ] = attachMethodName( methodName, methods_enabled[ methodName ] )


methods_available = {
    "jaccard_dissimilarity_sqrt": jaccard_dissimilarity_sqrt,
    "jaccard_dissimilarity"     : jaccard_dissimilarity
}

methods_enabled = {}

