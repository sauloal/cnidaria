import os
import sys

curr_pwd = os.getcwd()

def readFilesTitles(filetitles, verbose=True):
    macros = {
        'CURR_PWD': curr_pwd
    }

    titles = {}

    with open(filetitles, 'r') as fhd:
        for line in fhd:
            line = line.strip()
            
            if len(line) == 0:
                continue
            
            if line[0] == '#':
                # MACRO:EXTS:.jf
                if 'MACRO' in line:
                    if verbose:
                        print "has macro"
                    cols       = [x.strip() for x in line[1:].split(":")]
                    macro_type = cols[1]
                    macro_name = cols[2]
                    macro_val  = cols[3]
                    if verbose:
                        print "name %s type %s val %s" % ( macro_name, macro_type, macro_val )
                    if macro_type == 'A':
                        if macro_name not in macros:
                            macros[ macro_name ] = []
                        macros[ macro_name ].append( macro_val )
                        
                    elif macro_type == 'H':
                        if macro_name not in macros:
                            macros[ macro_name ] = {}
                        macro_key = macro_val
                        macro_val = cols[4]
                        macros[ macro_name ][ macro_key ] = macro_val
                    
                    #exts = [    '.bam.11.jf', '.cram.11.jf', '.11.jf',
                    #            '.bam.21.jf', '.cram.21.jf', '.21.jf',
                    #            '.bam.31.jf', '.cram.31.jf', '.31.jf',
                    #            '.bam.jf'   , '.cram.jf'   , '.jf' ]
                    
                continue

            

            try:
                fname, fnewname = [ x.strip() for x in line.split("\t")[:2] ]
                titles[                  fname % macros   ] = fnewname
                titles[ os.path.abspath( fname % macros ) ] = fnewname
                #print "adding %s to %s" % ( fname, fnewname )
                
            except:
                print "error parsing line", line
                print line.split("\t")
                raise
                sys.exit(1)
            


            if 'EXTS' in macros:
                exts = macros['EXTS']
                for ext in exts:
                    fext         = fname + ext
                    titles[fext] = fnewname
                    #print "adding ext %s to %s" % ( fext, fnewname )

    return titles
