#!/usr/bin/python

import os
import sys

kmer_sizes = [ 11, 15, 17, 21, 31 ]


def main():
    try:
        ofile  = sys.argv[1 ]
    except:
        print "no output file given"
        sys.exit(1)
        
    try:
        ifiles = sys.argv[2:]
    except:
        print "no input files given"
        sys.exit(1)
        
    if len( ifiles ) < 2:
        print "only one input file given"
        sys.exit(1)
    
    if os.path.exists( ofile ):
        print "output file %s exists" % ofile
        sys.exit(1)
    
    
    
    for ifile in ifiles:
        if not os.path.exists( ifile ):
            print "input file %s does not exists" % ifile
            sys.exit(1)
    
    data = {}
    
    stats_keys  = {}
    jstats_keys = {}
    bstats_keys = {}
    count_keys  = {}
    for ifile in ifiles:
        print "reading", ifile
        
        if ifile.endswith( '.stats'):
            ifname       = ifile.replace('.stats', '')
            if ifname not in data:
                data[ifname] = {}
        
            with open(ifile, 'r') as fhd:
                for line in fhd:
                    line = line.strip()
                    cols = line.split(":")
                    cols = [ x.strip() for x in cols ]
                    stats_keys[cols[0]] = 1
                    try:
                        data[ifname][ cols[0] ] = cols[1]
                    except:
                        print "INVALID STATS LINE IN", ifile
                        print line
                        print cols
                        raise
        
        elif ifile.endswith( '.jstats'):
            found_k   = False
            kmer_size = "00"

            for ksize in kmer_sizes:
                kmer_size = "%02d" % ksize
                k_ext     = '.%s.jf.jstats' % kmer_size
                if   ifile.find(k_ext) != -1:
                    ifname       = ifile.replace(k_ext, '')
                    found_k      = True
                    break
                    
            if not found_k:
                print "jf with unknown kmer size"
                print ifile
                sys.exit(1)
            
            if ifname not in data:
                data[ifname] = {}
        
            with open(ifile, 'r') as fhd:
                for line in fhd:
                    line = line.strip()
                    cols = line.split(":")
                    cols = [ x.strip() for x in cols ]
                    
                    jstats_keys[  "j_" + kmer_size + '_' + cols[0] ] = 1
                    data[ifname][ "j_" + kmer_size + '_' + cols[0] ] = cols[1]
        
        elif ifile.endswith( '.bstats'):
            ifname       = ifile.replace('.bstats', '')
            if ifname not in data:
                data[ifname] = {}
        
            with open(ifile, 'r') as fhd:
                for line in fhd:
                    line = line.strip()
                    
                    if len(line) == 0:
                        continue
                    
                    if line[0] == "#":
                        continue
                    
                    col  = line.split()
                    cls  = col[0]
                    dta  = col[1:]
                    
                    if cls == "SN":
                        #print line
                        line = " ".join( dta )
                        cols = line.split(":")
                        cols = [ x.strip() for x in cols ]

                        col_name = 'b_' + cls + '_' + cols[0].replace(" ", "_")
                        val      = cols[1]
                        #print ' col_name "' + col_name + '" val "' + val + '"'
                        if val.find("#") != -1:
                            #print '  has #'
                            nval      = val[:val.index("#")].strip()
                            col_name += '_(' + val[val.index("#")+1:].strip().replace(" ", "_") + ')'
                            val       = nval
                            #print '   new val "' + val + '"'
                        #if col_name not in data[ifname]:
                        #    data[ifname][ col_name ] = []
                        #print ' col_name "' + col_name + '" val "' + val + '"'
                        #print ' val "' + val + '"'
                        
                        
                        bstats_keys[  col_name ] = 1
                        data[ifname][ col_name ] = val
                    
                    if cls == "RL":
                        pass
                        #print line
                        #line = " ".join( dta )
                        #cols = line.split()
                        #cols = [ x.strip() for x in cols ]
                        #
                        #col_name = 'b_' + cls + '_' + cols[0].replace(" ", "_")
                        #val      = cols[1]
                        #
                        #bstats_keys[  col_name       ] = 1
                        #data[ifname][ col_name       ] = val
                        #bstats_keys[  col_name+"_bp" ] = 1
                        #data[ifname][ col_name+"_bp" ] = str(int(cols[0]) * int(cols[1]))
                    
                    else:
                        pass
                        #if 'b_' + cls not in data[ifname]:
                        #    data[ifname][ 'b_' + cls ] = []
                        #    
                        ##cols = line.split()[1:]
                        #cols = [ x.strip() for x in dta ]
                        #
                        ##bstats_keys[  "j_" + cols[0] ] = 1
                        #data[ifname]["b_"+cls].append( cols )

        elif ifile.endswith( '.count'):
            ifname       = ifile.replace('.count', '')
            if ifname not in data:
                data[ifname] = {}
        
            with open(ifile, 'r') as fhd:
                for line in fhd:
                    line = line.strip()
                    cols = line.split(" ")
                    cols = [ x.strip() for x in cols ]
                    
                    count_keys[   "count" ] = 1
                    data[ifname][ "count" ] = cols[-1]

    
    titles = sorted(stats_keys.keys()) + sorted(jstats_keys.keys()) + sorted(count_keys.keys()) + sorted(bstats_keys.keys())
    
    with open(ofile, 'w') as fhd:
        fhd.write("filename\tgroup\tname\tformat\t%s\n" % "\t".join(titles))
        
        for ifile in sorted(data):
            try:
                vals = [ data[ifile][x] if x in data[ifile] else "-1" for x in titles ]

            except KeyError:
                print "ERROR IN FILE", ifile
                raise
            
            group = os.path.dirname( ifile)
            bn    = os.path.basename(ifile)
            fmt   = os.path.splitext(bn)[1]
            iname = bn.replace(fmt, '').replace('_', ' ').replace('.', ' ').replace('  ', ' ')
            
            try:
                fhd.write("%s\t%s\t%s\t%s\t%s\n" % (ifile, group, iname, fmt, "\t".join(vals)))
            except:
                print ifile, iname, group, fmt
                raise


if __name__ == '__main__':
    main()




#==> sa.fa.count <==
#./denovo/sa.fa 46594


#==> sp.fa.stats <==
#t: 0
#a: 0
#c: 0
#g: 0
#n: 0
#T: 237689078
#A: 237800256
#G: 122425398
#C: 122478882
#N: 7

#.jstats
#Unique:    279075509
#Distinct:  690553647
#Total:     1883972302
#Max_count: 255


#flagstats
#962048116 + 0 in total (QC-passed reads + QC-failed reads)
#0 + 0 duplicates
#962048116 + 0 mapped (100.00%:-nan%)
#962048116 + 0 paired in sequencing
#480989694 + 0 read1
#481058422 + 0 read2
#912321193 + 0 properly paired (94.83%:-nan%)
#962048116 + 0 with itself and mate mapped
#0 + 0 singletons (0.00%:-nan%)
#50636290 + 0 with mate mapped to a different chr
#50636290 + 0 with mate mapped to a different chr (mapQ>=5)



#bstats
## This file was produced by samtools stats (1.1+htslib-1.1) and can be plotted using plot-bamstats
## The command line was:  stats 711.cram
## CHK, Checksum	[2]Read Names	[3]Sequences	[4]Qualities
## CHK, CRC32 of reads which passed filtering followed by addition (32bit overflow)
#CHK	c88faf43	e930ecec	d95d83ce
## Summary Numbers. Use `grep ^SN | cut -f 2-` to extract this part.
#SN	raw total sequences:	88920975
#SN	filtered sequences:	0
#SN	sequences:	88920975
#SN	is sorted:	1
#SN	1st fragments:	44460540
#SN	last fragments:	44460435
#SN	reads mapped:	81366868
#SN	reads mapped and paired:	79901993	# paired-end technology bit set + both mates mapped
#SN	reads unmapped:	7554107
#SN	reads properly paired:	77268369	# proper-pair bit set
#SN	reads paired:	88920975	# paired-end technology bit set
#SN	reads duplicated:	0	# PCR or optical duplicate bit set
#SN	reads MQ0:	5450403	# mapped and MQ=0
#SN	reads QC failed:	0
#SN	non-primary alignments:	0
#SN	total length:	8981018475	# ignores clipping
#SN	bases mapped:	8218053668	# ignores clipping
#SN	bases mapped (cigar):	8182221239	# more accurate
#SN	bases trimmed:	0
#SN	bases duplicated:	0
#SN	mismatches:	80193947	# from NM fields
#SN	error rate:	9.800999e-03	# mismatches / bases mapped (cigar)
#SN	average length:	101
#SN	maximum length:	101
#SN	average quality:	35.7
#SN	insert size average:	305.4
#SN	insert size standard deviation:	85.2
#SN	inward oriented pairs:	38696344
#SN	outward oriented pairs:	58236
#SN	pairs with other orientation:	67710
#SN	pairs on different chromosomes:	1124846
## First Fragment Qualitites. Use `grep ^FFQ | cut -f 2-` to extract this part.
## Columns correspond to qualities and rows to cycles. First column is the cycle number.
#FFQ	1	0	0	369859	0	0	0	0	38928	0	0	99209	0	19287	0	0	17832	186962	0	19360	7382	23881	0	86665	115867	26513	166656	527324	449894	573087	73221	1530670	10989134	0	3375410	25763399	0	0	0	0	0	0	0	0
#FFQ	102	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0
## Last Fragment Qualitites. Use `grep ^LFQ | cut -f 2-` to extract this part.
## Columns correspond to qualities and rows to cycles. First column is the cycle number.
#LFQ	1	0	0	363916	0	0	0	0	0	0	0	580068	0	0	0	0	0	498650	0	0	1352	0	0	25675	284253	0	407002	484663	484614	641150	0	1703998	10963102	0	4617145	23404847	0	0	0	0	0	0	0	0
#LFQ	102	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0
## GC Content of first fragments. Use `grep ^GCF | cut -f 2-` to extract this part.
#GCF	0.25	445
#GCF	99.50	166
## GC Content of last fragments. Use `grep ^GCL | cut -f 2-` to extract this part.
#GCL	0.25	398
#GCL	99.50	26
## ACGT content per cycle. Use `grep ^GCC | cut -f 2-` to extract this part. The columns are: cycle, and A,C,G,T counts [%]
#GCC	1	26.73	23.14	23.68	26.46
#GCC	101	31.27	18.52	18.71	31.51
## Insert sizes. Use `grep ^IS | cut -f 2-` to extract this part. The columns are: pairs total, inward oriented pairs, outward oriented pairs, other pairs
#IS	0	2	0	1	1
#IS	611	3125	3117	4	4
## Read lengths. Use `grep ^RL | cut -f 2-` to extract this part. The columns are: read length, count
#RL	101	88920975
## Indel distribution. Use `grep ^ID | cut -f 2-` to extract this part. The columns are: length, number of insertions, number of deletions
#ID	1	1367502	1260352
#ID	56	0	5
## Indels per cycle. Use `grep ^IC | cut -f 2-` to extract this part. The columns are: cycle, number of insertions (fwd), .. (rev) , number of deletions (fwd), .. (rev)
#IC	1	0	0	1331	1257
#IC	100	142	170	159	159
## Coverage distribution. Use `grep ^COV | cut -f 2-` to extract this part.
#COV	[1-1]	1	6751204
#COV	[1000-1000]	1000	86
#COV	[1000<]	1000	186131
## GC-depth. Use `grep ^GCD | cut -f 2-` to extract this part. The columns are: GC%, unique sequence percentiles, 10th, 25th, 50th, 75th and 90th depth percentile
#GCD	0.0	0.005	0.000	0.000	0.000	0.000	0.000
#GCD	65.0	100.000	31.199	31.199	31.199	31.199	31.199
