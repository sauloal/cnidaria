#!/usr/bin/python

import os
import sys
import copy

class csv( object ):
    def __init__(self):
        self.col_names = []
        self.rows      = []
    
    def add_header(self, cols):
        self.col_names = cols
        #print "ADDING HEADER", cols

    def add_row(self, cols):
        #print "ADDING ROW", cols
        if cols[0] != self.col_names[ len(self.rows) ]:
            print "wrong row name: '%s' instead of '%s'" % ( cols[0], self.col_names[ len(self.rows) ] )
            sys.exit( 1 )

        self.rows.append( [ int(x) for x in cols[1:] ] )
    
    def check(self):
        if len(self.col_names) != len( self.rows ):
            print "number of columns (%d) != number of rows (%d)" % ( len(self.col_names), len( self.rows ) )
            sys.exit( 1 )
            
    def subtract(self, other):
        for k in xrange(len(self.col_names)):
            if self.col_names[k] != other.col_names[k]:
                print "column names differ. k %d %s != %s" % (k, self.col_names[k], other.col_names[k])
                sys.exit( 1 )
                
        for k in xrange(len(self.rows)):
            for l in xrange(len(self.rows)):
                self.rows[k][l] -= other.rows[k][l]
    
    def sum(self, other):
        for k in xrange(len(self.col_names)):
            if self.col_names[k] != other.col_names[k]:
                print "column names differ. k %d %s != %s" % (k, self.col_names[k], other.col_names[k])
                sys.exit( 1 )
                
        for k in xrange(len(self.rows)):
            for l in xrange(len(self.rows)):
                self.rows[k][l] += other.rows[k][l]    
    
    def zeroe(self):
        for k in xrange(len(self.rows)):
            for l in xrange(len(self.rows)):
                self.rows[k][l] = 0
    
    def check_zero(self):
        for k in xrange(len(self.rows)):
            for l in xrange(len(self.rows)):
                if self.rows[k][l] != 0:
                    print self.col_names[k], ' X ', self.col_names[l], '!= 0'
                    
    
    def get_pairs(self):
        pairs = {}
        for k in xrange(len(self.rows)):
            for l in xrange(len(self.rows)):
                #if self.rows[k][l] != 0:
                #    print self.col_names[k], ' X ', self.col_names[l], '!= 0'
                pair = self.col_names[k] + ' X ' + self.col_names[l]
                val  = self.rows[k][l]
                if pair not in pairs:
                    pairs[ pair ] = val
                else:
                    if pairs[ pair ] != val:
                        print "pair", pairs[ pair ], "has discrepancy"
                        sys.exit( 1 )
        return pairs

    def check_pairs(self, other, ish=0.001):
        ipairs = self.get_pairs()
        opairs = other.get_pairs()
        
        #print "ipairs", ipairs
        #print "opairs", opairs
        
        errors = []
        
        for pair in sorted(opairs):
            print "checking pair", pair,
            if pair in ipairs:
                opair_val = opairs[ pair ]
                ipair_val = ipairs[ pair ]
                
                if ipair_val != opair_val:
                    diff = opair_val - ipair_val
                    
                    if diff < 0:
                        msg = " !!! pair %s differ %d != %d diff %d !!!" % (pair, ipair_val, opair_val, diff)
                        print "BAD"
                        #print msg
                        errors.append( msg )
                        
                    else:
                        print  "okish"
                        #max_allowed = int( min(ipair_val * ish, opair_val * ish) )
                        #
                        #if max_allowed == 0:
                        #    max_allowed = 1
                        #
                        #if diff <= max_allowed:
                        #    print "OKish (%d out of %d and %d)" % (diff, ipair_val, opair_val)
                        #
                        #else:
                        #    msg = " !!! pair %s differ %d != %d diff %d !!!" % (pair, ipair_val, opair_val, diff)
                        #    print
                        #    #print msg
                        #    errors.append( msg )
                        
                else:
                    print "OK"
                    
            else:
                print
                print " pair", pair, "not in other database"
                sys.exit(1)

        if len(errors) > 0:
            print "SUMMARY OF ERRORS"
            for err in errors:
                print err
            #sys.exit(1)


def process_csv( infile ):
    if not os.path.exists( infile ):
        print "input file %s does not exists" % infile
        sys.exit( 1 )

    else:
        print "opening", infile
    
    csv_hdl = csv()
    
    with open(infile) as fhd:
        lc = 0
        
        for line in fhd:
            line = line.strip()
            #print "LINE", line
            cols  = line.split( "\t" )
            #print "COLS", cols
            lc   += 1
            
            if lc == 1: # header
                csv_hdl.add_header( cols )
            
            else:
                csv_hdl.add_row( cols )

        csv_hdl.check()

    return csv_hdl

RUN_TYPE_CSV='csv'
RUN_TYPE_MRG='merge'

def main():
    run_type = None
    exe_name = os.path.basename(sys.argv[0])

    if   exe_name == 'verify_csvs.py':
        run_type = RUN_TYPE_CSV
    elif exe_name == 'verify_merge.py':
        run_type = RUN_TYPE_MRG
    else:
        print "unkown executable name '%s'" % exe_name
        sys.exit(1)
    
    if len(sys.argv) < 2:
        print "no files given"
        print sys.argv[0], "<partial csv file 1> <partial csv file 2> <partial csv file n> <merged csv file>"
        sys.exit(1)
        
    infiles = sys.argv[1:]
    
    if len(infiles) < 3:
        print "needs at least 3 files"
        sys.exit(1)
    
    mergedfile = infiles[ -1]
    infiles    = infiles[:-1]
    
    print "merged file", mergedfile
    print "infiles    ", infiles

    mergedfile_csv = process_csv( mergedfile )
    infiles_csv    = []
    for infile in infiles:
        pcsv = process_csv( infile )
        infiles_csv.append( pcsv )

    
    if run_type == RUN_TYPE_CSV:
        subtr_csv      = copy.deepcopy( mergedfile_csv )

        for pcsv in infiles_csv:
            subtr_csv.subtract( pcsv )
    
        print "checking sizes"
        subtr_csv.check()
        print "checking sum"
        subtr_csv.check_zero()
        print "done"

    elif run_type == RUN_TYPE_MRG:
        in_pairs         = []
        
        for pcsv in infiles_csv:
            mergedfile_csv.check_pairs( pcsv )

if __name__ == '__main__':
    main()
