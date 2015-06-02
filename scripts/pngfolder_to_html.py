#!/usr/bin/python
import sys, os
import math

import reloader

try:
	import Image
except ImportError:
	import PIL.Image as Image

numcols     = 3
numrows     = 2

dpi         = 1200

#./pngfolder_to_html.py trees/*_pimp_problems.lst.png; convert *_pimp_problems.lst.png*.png index_trees_short2.lst.vcf.gz.simplified.vcf.gz.filtered.vcf.gz.SL2.40ch06.0000_.vcf.gz.SL2.40ch06.fasta.tree_pimp_problems.lst.png.pdf
#./pngfolder_to_html.py trees/*_cherry.lst.png;        convert *_cherry.lst.png*.png        index_trees_short2.lst.vcf.gz.simplified.vcf.gz.filtered.vcf.gz.SL2.40ch06.0000_.vcf.gz.SL2.40ch06.fasta.cherry.lst.png.pdf

def getCommonSuffix( names ):
    minsize  = sys.maxint
    currsize = 0

    for name in names:
        nsize = len(name)
        if nsize < minsize:
            minsize = nsize

    currsize = minsize - 1
    print "minsize", minsize
    name1   = names[0]

    while currsize >= 0:
        sublen  = len(name1) - currsize - 1
        sub     = name1[sublen:]
        #print " currsize", currsize, "sub", sub
        present = True

        for name in names:
            #print "  name", name, "sub", sub
            if not name.endswith( sub ):
                present = False
                break

        if present:
            print "PRESENT"
            break

        else:
            #print "not present"
            currsize -= 1

    if currsize > 0:
        sublen  = len(name1) - currsize - 1
        sub     = name1[sublen:]
        return sub

    else:
        return ""


def main(infiles):
    cp = os.path.commonprefix( infiles )
    cs = getCommonSuffix(      infiles )

    print "cp", cp
    print "cs", cs

    outfile  = "index"

    if cp != "":
        outfile += "_" + cp.replace("/", "_")

    if cs != "":
        outfile += "_" + cs

    #outfile += ".html"

    numfiles    = len( infiles )
    width       = 0
    height      = 0

    for filename in infiles:
        img = Image.open( filename ).size
        #print "img", img
        if img[0] > width:
            width = img[0]

        if img[1] > height:
            height = img[1]

    print "width %d height %d" % ( width, height )
    #quit()



    widthTotal  = int( numcols * width  )
    heightTotal = int( numrows * height )
    #heightTotal = height


    html     = ["<html>"]
    html.append("<body>")
    html.append("<table>")
    html.append("<tr>")

    pngs = [[]]

    filecount = -1
    for filename in infiles:
        dn = filename.replace( cp, "" ).replace( cs, "" )
        print dn,

        filecount += 1

        print filecount,

        page = filecount / (numcols * numrows)
        print page

        if len( pngs ) <= page:
            pngs.append( [] )

        pngs[page].append( (filename, dn ) )

        if filecount % numcols == 0 and filecount > 0:
            html.append("</tr>")
            html.append("<tr>")

        html.append("<td>")
        html.append(dn)
        html.append('<img src="%s" height="%dpx" width="%dpx">' % (filename, height, width))
        html.append("</td>")


    for page in xrange(len(pngs)):
        pngin     = pngs[page]
        #filecount = -1

        png             = Image.new( 'RGBA', (widthTotal, heightTotal) )
        png.info["dpi"] = (dpi, dpi)

        for filecount in xrange(len(pngin)):
            filename, dn = pngin[ filecount ]
            rowpos = ( filecount % numcols ) * width
            colpos = ( filecount / numcols ) * height

            print filename, page+1, filecount, rowpos, colpos

            img  = Image.open( filename ).resize((width, height))
            img.info["dpi"] = (dpi, dpi)
            png.paste( img, ( rowpos, colpos ) )

        outfilepng = outfile+"_%03d.png" % (page+1)
        print "saving png", outfilepng
        png.save( outfilepng, optimize=True, dpi=(dpi,dpi) )
        #break


    html.append("</tr>")
    html.append("</table>")
    html.append("</body>")
    html.append("</html>")


    print "saving html", outfile+".html"
    with open( outfile+".html", 'w' ) as fhd:
        fhd.write( "\n".join( html ) )

    print "done"


if __name__ == '__main__':
    infiles = sys.argv[1:]
    main(infiles)
