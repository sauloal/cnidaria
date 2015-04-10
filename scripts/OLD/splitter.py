#!../../../pypy
#!/usr/bin/python
import sys,os

#http://www.evolgenius.info/evolview.html#app
#http://www.trex.uqam.ca/loadData.php

#bray curtis distance
# sumij(|Aij - Bij|) / (sum A + sum B)

#correction
#Gower's generalized coefficient of dissimilarity
#    n - avg
#g = -------
#       sd
#
#dist = sum(|g|) / N

validParts = ['JACCARD',
              'RUSSEL RAO',
              'FOWLKES MALLOWS']

names      = []


def main():
    if len(sys.argv) == 1:
        print "no input given"
        sys.exit(1)
    
    infile = sys.argv[1]
    
    if not os.path.exists(infile):
        print "input %s does not exists" % infile
        sys.exit(1)
        
    if os.path.getsize(infile) == 0:
        print "nice try. empty file"
        sys.exit(1)
    
    parts      = {}
    part       = None
    maxNameLen = 0
    currIndex  = 0
    diss       = None
    
    with open(infile, 'r') as inf:
        line = ""
        for line in inf:
            if len(line) > 3:            
                if part is not None:
                    if line[0] == "=":
                        print "  finished '%s' #%d" % ( part, parts[part] )
                        diss.close()
                        part = None

                    else:
                        if line != "\n":
                            diss.write(line)
                
                elif line[0] == "=":
                    beginPos  = line.find("= BEGIN")
                    print "BEGIN", beginPos, line
                    
                    if beginPos > -1:
                        beginPos += 8
                        endPos    = line.find(" =", beginPos)
                        print "END", endPos, line
                        
                        if endPos > -1:                            
                            part      = line[beginPos:endPos]
                            
                            if part not in validParts:
                                print "invalid part '" + part + "'"
                                part = None
                            
                            else:
                                if part in parts:
                                    parts[part] += 1
                                else:
                                    parts[part]  = 1
    
                                outFile = infile + "." + part + "." + "%03d" % parts[part] + ".matrix"
                                print "reading part '%s' #%03d -> %s" % ( part, parts[part], outFile )
                                
                                if diss is not None:
                                    diss.close()
                                
                                diss = open(outFile, 'w')

    
if __name__ == '__main__': main()
