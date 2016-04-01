import math

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
class statholder(object):
    def __init__(self, m):
        names = dir(self)
        
        #print "NAMES", names
        names = [ x for x in (set(names) - set(dir(object())))]
        
        #print "NAMES", names
        names = [ x for x in      names if x.startswith("D_") or x.startswith("S_") ]
        
        names.sort()
        print "NAMES", ", ".join(names)

        for n in names:
            m[n] = getattr(self, n)
    
    def S_jaccard(                self ):
        r  = float( self.a ) / ( self.a + self.b + self.c )
        return r
    
    def D_jaccard(                self ): #  1
        r  = 1 - self.S_jaccard()
        return r
    
    def D_jaccard_sqrt(           self ):
        r  = math.sqrt( self.D_jaccard() )
        return r
    
    def S_dice(                   self ): #  2
        r  = float( 2.0 * self.a ) / ( (2.0 * self.a) + self.b + self.c )
        return 1.0 - r
    
    #def S_czekanowski(            self ): #  3
    #    r  = float( 2.0 * self.a ) / ( (2.0 * self.a) + self.b + self.c )
    #    return 1.0 - r
    
    def S_jaccard3w(              self ): #  4
        r  = float( 3.0 * self.a ) / ( (3.0 * self.a) + self.b + self.c )
        return 1.0 - r
    
    def S_nei_li(                 self ): #  5
        r  = float( 2.0 * self.a ) / ( (self.aPb) + (self.aPc) )
        return 1.0 - r
    
    def S_sokal_sneath_I(         self ): #  6
        r  = float( self.a ) / ( self.a + (2.0*self.b) + (2.0 * self.c) )
        return 1.0 - r
    
    def S_sokal_michener(         self ): #  7
        r  = float( self.aPd ) / ( self.aPbPcPd )
        return 1.0 - r
    
    def S_sokal_sneath_II(        self ): #  8
        r  = float( 2.0 * self.aPd ) / ( (2.0*self.a) + self.b + self.c + (2.0 * self.d) )
        return 1.0 - r
    
    def S_roger_tanimoto(         self ): #  9
        r  = float( self.aPd ) / ( self.a + (2.0*(self.b + self.c)) + self.d )
        return 1.0 - r
    
    def S_faith(                  self ): # 10
        r  = float( self.a + (0.5*self.d) ) / ( self.aPbPcPd )
        return 1.0 - r
    
    def S_gower_legendre(         self ): # 11
        r  = float( self.aPd ) / ( self.a + (0.5 * (self.b + self.c)) + self.d )
        return 1.0 - r
    
    def S_intersection(           self ): # 12
        r  = float( self.a )
        return r
    
    def S_innerproduct(           self ): # 13
        r  = float( self.aPd )
        return r
    
    def S_russell_rao(            self ): # 14
        r  = float( self.a ) / ( self.aPbPcPd )
        return 1.0 - r
    
    def D_hamming(                self ): # 15
        r  = self.bPc
        return r
    
    def D_euclid(                 self ): # 16
        r  = math.sqrt(self.D_hamming())
        return r
    
    def D_squared_euclid(         self ): # 17
        r  = math.sqrt(self.D_hamming() ** 2)
        return r
    
    #def D_canberra(               self ): # 18
    #    r  = hamming(self) ** (2/2)
    #    return r
    
    #def D_manhattan(              self ): # 19
    #    r  = self.bPc
    #    return r
    
    def D_mean_manhattan(         self ): # 20
        r  = float(self.bPc) / (self.aPbPcPd)
        return r
    
    #def D_city_block(             self ): # 21
    #    r  = self.bPc
    #    return r
    
    #def D_minkowski(              self ): # 22
    #    r  = self.bPc ** (1/1)
    #    return r
    
    def D_vari(                   self ): # 23
        r  = float( self.bPc ) / (4.0*( self.aPbPcPd ))
        return r
    
    def D_sized_difference(       self ): # 24
        r  = float( self.bPc ** 2 ) / (( self.aPbPcPd ) ** 2)
        return r
    
    def D_shaped_difference(      self ): # 25
        t  = (self.n * self.bPc) - ((self.b - self.c) ** 2)
        b  = (self.aPbPcPd) ** 2
        r  = float( t ) / b
        return r
    
    def D_pattern_difference(     self ): # 26
        t  = 4 * self.bTc
        b  = (self.aPbPcPd) ** 2
        r  = float( t ) / b
        return r
    
    def D_lance_williams(         self ): # 27
        r  = float( (self.bPc) ) / (( 2.0 * self.a ) + self.b + self.c )
        return r
    
    def D_bray_curtis(            self ): # 28
        r  = float( (self.bPc) ) / (( 2.0 * self.a ) + self.b + self.c )
        return r
    
    def D_hellinger(              self ): # 29
        u  = float(self.a) / math.sqrt(self.aPb * self.aPc)
        v  = 1 - u
        r  = 2.0 * math.sqrt(v)
        return r
    
    def D_chord(                  self ): # 30
        u  = (float(self.a) / math.sqrt(self.aPb * self.aPc))
        v  = 2.0 * (1 - u)
        r  = math.sqrt(v)
        return r
    
    def S_cosine(                 self ): # 31
        r  = float(self.a) / (math.sqrt(self.aPb * self.aPc) ** 2.0)
        return 1.0 - r
    
    def S_gilbert_wells(          self ): # 32
        r  = math.log(self.a) - math.log(self.n) - math.log(float(self.aPb)/self.n) - math.log(float(self.aPc) / self.n)
        return 1.0 - r
    
    def S_ochiai_I(               self ): # 33
        r  = float(self.a) / (math.sqrt(self.aPb * self.aPc))
        return 1.0 - r
    
    def S_forbes_I(               self ): # 34
        r  = float( self.n * self.a ) / ( self.aPb * self.aPc )
        return 1.0 - r
    
    def S_fossum(                 self ): # 35
        o  = self.n * ((self.a - .5)**2)
        p  = self.aPb * self.aPc
        r  = float( o ) / p
        return 1.0 - r
    
    def S_sorgenfrei(             self ): # 36
        r  = float( self.a ** 2 ) / ( self.aPb * self.aPc )
        return 1.0 - r
    
    def S_mountford(              self ): # 37
        o  = float( self.a )
        p  = ( (0.5 * (self.aTb + self.aTc)) + self.bTc )
        r  = o / p
        return 1.0 - r
    
    def S_otsuka(                 self ): # 38
        r  = float( self.a ) / ((self.aPb * self.aPc)**.5)
        return 1.0 - r
    
    def S_mcconnaughey(           self ): # 39
        r  = float( ((self.a ** 2) - self.bTc ) ) / (self.aPb * self.aPc)
        return 1.0 - r
    
    def S_tarwid(                 self ): # 40
        aPb_T_aPc = ( self.aPb * self.aPc )
        t         = self.nTa - aPb_T_aPc
        b         = self.nTa + aPb_T_aPc
        r         = float(t) / b
        return 1.0 - r
    
    def S_kulczynski_II(          self ): # 41
        t  = (float(self.a) / 2) * ( (2*self.a) + self.b + self.c )
        b  = self.aPb * self.aPc
        r  = float(t) / b
        return 1.0 - r
    
    def S_driver_kroeber(         self ): # 42
        m  = (float(self.a) / 2.0)
        t  = ( 1.0 / self.aPb )
        b  = ( 1.0 / self.aPc )
        r  = m * (t + b)
        return 1.0 - r
    
    def S_johson(                 self ): # 43
        t  = float(self.a) / self.aPb
        b  = float(self.a) / self.aPc
        r  = t + b
        return 1.0 - r
    
    def S_dennis(                 self ): # 44
        o  = float(self.aTd - self.bTc)
        p  = self.n * self.aPb * self.aPc
        r  = o / (math.sqrt( p ))
        return 1.0 - r
    
    def S_simpson(                self ): # 45
        r  = float(self.a) / min( [self.aPb, self.aPc] )
        return 1.0 - r
    
    def S_braun_banquet(          self ): # 46
        r  = float(self.a) / max( [self.aPb, self.aPc] )
        return 1.0 - r
    
    def S_fager_mcgowan(          self ): # 47
        t  = float(self.a) / (math.sqrt(self.aPb * self.aPc))
        b  = max( [self.aPb, self.aPc] ) / 2.0
        r  = t - b
        return 1.0 - r
    
    def S_forbes_II(              self ): # 48
        p  = self.nTa - (self.aPb * self.aPc)
        q  = self.n * min([self.aPb,self.aPc])-(self.aPb*self.aPc)
        r  = float(p) / q
        return 1.0 - r
    
    def S_sokal_sneath_IV(        self ): # 49
        m  = float(self.a)  / self.aPb
        n  = float(self.a)  / self.aPc
        o  = float(self.a)  / self.bPc
        p  = float(self.a)  / self.bPd
        r  = float(m + n + o + p) / 4
        return 1.0 - r
    
    def S_sokal_sneath_IV2(       self ): # 49.2
        m  = float(self.a)  / self.aPb
        n  = float(self.a)  / self.aPc
        o  = float(self.a)  / self.bPd
        p  = float(self.a)  / self.bPd
        r  = float(m + n + o + p) / 4
        return 1.0 - r
    
    def S_gower(                  self ): # 50
        p  = self.aPd
        q  = math.sqrt(self.aPb * self.aPc * self.bPd * self.cPd)
        r  = float(p) / q
        return 1.0 - r
    
    def pearson_chi_squared(      self ):
        o   = float(self.n * ((self.aTd - self.bTc) ** 2))
        p   = (self.aPb * self.aPc * self.cPd * self.bPd)
        q2  = o / p
        return q2
    
    def pearson_phi(              self ):
        n   = (self.aTd - self.bTc)
        o   = math.sqrt(self.aPb * self.aPc * self.bPd * self.cPd)
        p   = n / o
        return p
    
    def S_pearson_I(              self ): # 51
        q2 = self.pearson_chi_squared()
        r  = q2
        return 1.0 - r
    
    def S_pearson_II(             self ): # 52
        q2 = self.pearson_chi_squared()
        r  = (q2 / (self.n + q2)) ** .5
        return 1.0 - r
    
    def S_pearson_III(            self ): # 53
        p  = self.pearson_phi()
        r  = ( p / ( self.n + p ) ) ** .5
        return 1.0 - r
    
    def S_pearson_heron_I(        self ): # 54
        r   = self.pearson_phi()
        return 1.0 - r
    
    def S_pearson_heron_II(       self ): # 55
        n  = math.pi * math.sqrt( self.bTc )
        o  = math.sqrt( self.aTd ) + math.sqrt(self.bTc )
        r  = math.cos( float(n) / o )
        return 1.0 - r
    
    def S_sokal_sneath_III(       self ): # 56
        r  = float(self.aPd) / self.bPc
        return 1.0 - r
    
    def S_sokal_sneath_V(         self ): # 57
        r  = float(self.aTd) / ((self.aPb * self.aPc * self.bPd * (self.cPd ** .5)))
        return 1.0 - r
    
    def S_cole(                   self ): # 58
        m  = math.sqrt(2) * ( (self.aTd) - (self.bTc) )
        n  = (( self.aTd) - (self.bTc)) ** 2
        o  = (self.aPb * self.aPc * self.bPd * self.cPd)
        p  = math.sqrt(n - o)
        r  = float(m) / p
        return 1.0 - r
    
    #def S_stiles(                 self ): # 59
    #    pass
    
    def S_ochiai_II(              self ): # 60
        r  = float(self.aTd) / (math.sqrt(self.aPb * self.aPc * self.bPd * self.cPd))
        return 1.0 - r
    
    def S_yuleq(                  self ): # 61
        n  = float( self.aTd - self.bTc )
        o  = float( self.aTd + self.bTc )
        r  = n / o
        return 1.0 - r
    
    def D_yuleq(                  self ): # 62
        r  = (2.0*self.bTc) / (self.aTd + self.bTc)
        return 1.0 - r
    
    def S_yulew(                  self ): # 63
        n  = float( math.sqrt(self.aTd) - math.sqrt(self.bTc) )
        o  = float( math.sqrt(self.aTd) + math.sqrt(self.bTc) )
        r  = n / o
        return 1.0 - r
    
    def S_kulczynski_I(           self ): # 64
        r  = self.a / self.bPc
        return 1.0 - r
    
    def S_tanimoto(               self ): # 65
        r  = self.a / (self.aPb + self.aPc - self.a)
        return 1.0 - r
    
    def S_dispersion(             self ): # 66
        o  = self.aTd - self.bTc
        p  = (self.a + self.b + self.c + self.d)**2
        r  = float(o) / p
        return 1.0 - r
    
    def S_hamann(                 self ): # 67
        o  = (self.aPd) - (self.bPc)
        p  = (self.a + self.b + self.c + self.d)
        r  = float(o) / p
        return 1.0 - r
    
    def S_michael(                self ): # 68
        o  = 4.0 * (self.aTd - self.bTc)
        p  = (self.aPb**2) + (self.bPc**2)
        r  = float(o) / p
        return 1.0 - r
    
    def sigma(                    self ):
        return max(self.a,self.b) + max(self.c,self.d) + max(self.a,self.c) + max(self.b,self.d)
    
    def sigma_prime(              self ):
        return max(self.aPc,self.bPd) + max(self.aPb,self.cPd)
    
    def S_goodman_kruskal(        self ): #69
        sig = self.sigma()
        sip = self.sigma_prime()
        o   = sig - sip
        p   = (2.0 * self.n) - sip
        r   = o / p
        return 1.0 - r
    
    def S_anderberg(              self ): #70
        sig = self.sigma()
        sip = self.sigma_prime()
        o   = sig - sip
        p   = (2.0 * self.n)
        r   = o / p
        return 1.0 - r
    
    def S_baroni_urbani_buser_I(  self ): #71
        sqrt_ab = math.sqrt(self.aTb)
        o       = sqrt_ab + self.a
        p       = sqrt_ab + self.a + self.b + self.c
        r       = float(o) / p
        return 1.0 - r
    
    def S_baroni_urbani_buser_II( self ): #72
        sqrt_ab = math.sqrt(self.aTb)
        o       = sqrt_ab + self.a - self.bPc
        p       = sqrt_ab + self.a + self.b + self.c
        r       = float(o) / p
        return 1.0 - r
    
    def S_pierce(                 self ): #73
        o  = self.aTb + self.bTc
        p  = self.aTb + (2*self.bTc) + self.cTd
        r  = float(o) / p
        return 1.0 - r
    
    def S_eyraud(                 self ): #74
        n2 = self.n**2
        o  = n2 * (self.nTa - (self.aPb*self.aPc))
        p  = self.aPb * self.aPc * self.bPd * self.cPd
        r  = float(o) / p
        return 1.0 - r
    
    #def S_tarantula(              self ): #75
    #    pass
    
    #def S_ample(                  self ): #76
    #    pass

    def print_stats(self):
        keys =  "a,b,B,c,C,d,D,"+\
                "aPb,aPB,aPc,aPC,aPd,aPD,bPc,BPC,bPd,BPD,cPd,CPD,"+\
                "aTb,aTB,aTc,aTC,aTd,aTD,bTc,BTC,bTd,BTD,cTd,CTD,"+\
                "aPbPcPd,n,N,"+\
                "nTa"
        
        keys = keys.split(",")
        
        for key in keys:
            v = getattr(self, key)
            print "%9s: %s" % (key, str(v))


def attachMethodName( methodName,  func ):
    print "attaching method", methodName
 
    if methodName not in methods_enabled:
        print "unknown method:", methodName
        #sys.exit(1)
        raise KeyError
        
    def ffunc(dissi, num_kmers, x, y, totalX, totalY, countX, countY, val):
        #print "running attached function", methodName
        
        #x\y 1   0
        #1   a   b    a+b
        #0   c   d    c+d
        #    a+c b+d  a+b+c+d
        
        stats_data.a  = val
        
        stats_data.b  = ( countX - val )
        stats_data.B  = ( totalX - val )
        
        stats_data.c  = ( countY - val )
        stats_data.C  = ( totalY - val )
        
        stats_data.d  = stats_data.a + stats_data.b + stats_data.c
        stats_data.D  = stats_data.a + stats_data.B + stats_data.C
        
        stats_data.aPb = stats_data.a + stats_data.b
        stats_data.aPB = stats_data.a + stats_data.B
        stats_data.aPc = stats_data.a + stats_data.c
        stats_data.aPC = stats_data.a + stats_data.C
        stats_data.aPd = stats_data.a + stats_data.d
        stats_data.aPD = stats_data.a + stats_data.D
        stats_data.bPc = stats_data.b + stats_data.c
        stats_data.BPC = stats_data.B + stats_data.C
        stats_data.bPd = stats_data.b + stats_data.d
        stats_data.BPD = stats_data.B + stats_data.D
        stats_data.cPd = stats_data.c + stats_data.d
        stats_data.CPD = stats_data.C + stats_data.D

        stats_data.aTb = float(stats_data.a) * stats_data.b
        stats_data.aTB = float(stats_data.a) * stats_data.B
        stats_data.aTc = float(stats_data.a) * stats_data.c
        stats_data.aTC = float(stats_data.a) * stats_data.C
        stats_data.aTd = float(stats_data.a) * stats_data.d
        stats_data.aTD = float(stats_data.a) * stats_data.D
        stats_data.bTc = float(stats_data.b) * stats_data.c
        stats_data.BTC = float(stats_data.B) * stats_data.C
        stats_data.bTd = float(stats_data.b) * stats_data.d
        stats_data.BTD = float(stats_data.B) * stats_data.D
        stats_data.cTd = float(stats_data.c) * stats_data.d
        stats_data.CTD = float(stats_data.C) * stats_data.D
        
        stats_data.aPbPcPd = stats_data.a + stats_data.b + stats_data.c + stats_data.d
        
        stats_data.n   = stats_data.a + stats_data.b + stats_data.c + stats_data.d
        stats_data.N   = stats_data.a + stats_data.B + stats_data.C + stats_data.D
        
        stats_data.nTa = float(stats_data.n) * stats_data.a
        
        try:
            r = func()

        except ZeroDivisionError:
            #print "DIVISION BY ZERO"
            #stats_data.print_stats()
            r = 1
        
        except ValueError:
            #print "MATH ERROR"
            #stats_data.print_stats()
            r = 1
        
        #print "dissi method %-30s x %3d y %3d r %.5f totalX %12d totalY %12d countX %12d countY %12d val %12d" % ( methodName, x, y, r, totalX, totalY, countX, countY, val )
        dissi[ methodName ][x][y] += r
    
    return ffunc


def init( methods_to_apply ):
    for m in methods_to_apply:
        if m not in methods_available:
            print " unkknown method %s" % m
            #sys.exit(1)
            raise KeyError

        print "enabling %s method" % m

        methods_enabled[m] = methods_available[m]

    for methodName in methods_enabled.keys():
        methods_enabled[ methodName ] = attachMethodName( methodName, methods_enabled[ methodName ] )

    print "methods_enabled", methods_enabled





methods_available = {}
methods_enabled   = {}
stats_data        = statholder(methods_available);

print "methods_available\n\t", "\n\t".join(sorted(methods_available.keys())), "\n"
